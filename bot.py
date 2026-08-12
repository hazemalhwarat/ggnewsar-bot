"""
GGNewsAR Telegram Bot — unified RSS + Liquipedia pipeline.

Pipeline (per cycle):
  1. RSS phase: fetch all feeds in feeds.py, filter freshness + dedup, send.
  2. Liquipedia phase: poll watchlist pages, filter bot/minor/tiny edits, send.

State is unified in state.json with three collections:
  - urls: seen RSS URLs (ring of last 8000)
  - title_hashes: normalized title hashes (ring of last 8000)
  - liquipedia: per-page seen revids + last seen size

No keyword filter: trust the source. Only:
  - 24h freshness window for RSS
  - URL + title dedup for RSS
  - Structural filter for Liquipedia (bot/minor/<100 bytes)

Configuration sources: feeds.py (RSS_FEEDS), watchlist.py (WATCHLIST).
Secrets: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID in environment.
"""

import os
import re
import json
import time
import hashlib
import logging
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

import feedparser
import requests

from feeds import RSS_FEEDS
from watchlist import WATCHLIST

# ============================================================
# Configuration
# ============================================================
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

STATE_FILE = Path("state.json")

# Cap to prevent flooding if many fresh items appear at once
MAX_MESSAGES_PER_RUN = 50

# Telegram bot API rate limit: ~1 msg/sec per chat
MESSAGE_DELAY_SECONDS = 1.0

# RSS freshness window: ignore items older than this
MAX_AGE_HOURS = 24

# State ring sizes
SEEN_URLS_RING = 8000
SEEN_TITLES_RING = 8000
SEEN_REVS_PER_PAGE = 20

# Liquipedia API
LIQUIPEDIA_USER_AGENT = "GGNewsAR Bot/2.0 (https://ggnewsar.com; hazem@ggnewsar.com)"
LIQUIPEDIA_RATE_LIMIT_SEC = 2.5
LIQUIPEDIA_BATCH_SIZE = 50
LIQUIPEDIA_MIN_BYTES_CHANGE = 100  # ignore edits smaller than this

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage" if TELEGRAM_BOT_TOKEN else None

# Strip "Source - Article Title" patterns from RSS titles for dedup
SOURCE_SUFFIX_RE = re.compile(r"\s*[\-\|\u2013\u2014:]\s*[^\-\|\u2013\u2014:]{1,40}$")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("ggnewsar")


# ============================================================
# State persistence
# ============================================================
def load_state() -> dict:
    if not STATE_FILE.exists():
        return {
            "urls": [],
            "title_hashes": [],
            "liquipedia": {},  # "wiki:page" -> {"revids": [...], "size": int}
        }
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        log.error(f"state.json corrupted, starting fresh: {e}")
        return {"urls": [], "title_hashes": [], "liquipedia": {}}

    data.setdefault("urls", [])
    data.setdefault("title_hashes", [])
    data.setdefault("liquipedia", {})
    return data


def save_state(state: dict) -> None:
    state["urls"] = state["urls"][-SEEN_URLS_RING:]
    state["title_hashes"] = state["title_hashes"][-SEEN_TITLES_RING:]
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


# ============================================================
# Telegram
# ============================================================
def send_telegram(text: str) -> bool:
    if not TELEGRAM_API or not TELEGRAM_CHAT_ID:
        log.error("Telegram credentials missing")
        return False

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    try:
        r = requests.post(TELEGRAM_API, data=payload, timeout=15)
        if r.status_code == 200:
            return True
        log.error(f"Telegram {r.status_code}: {r.text[:200]}")
        return False
    except requests.RequestException as e:
        log.error(f"Telegram request failed: {e}")
        return False


def html_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ============================================================
# RSS phase
# ============================================================
def normalize_title(title: str) -> str:
    t = title.lower().strip()
    t = SOURCE_SUFFIX_RE.sub("", t).strip()
    t = re.sub(r"[^\w\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def title_hash(title: str) -> str:
    return hashlib.md5(normalize_title(title).encode("utf-8")).hexdigest()


def is_fresh(entry, max_age_hours: int) -> bool:
    """True if entry has no timestamp or is within freshness window."""
    pub = getattr(entry, "published_parsed", None) or getattr(entry, "updated_parsed", None)
    if not pub:
        return True
    try:
        pub_time = datetime(*pub[:6], tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return True
    return (datetime.now(timezone.utc) - pub_time) <= timedelta(hours=max_age_hours)


def strip_html(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def format_rss_message(source: str, title: str, summary: str, link: str) -> str:
    summary = strip_html(summary)[:280]
    parts = [
        f"<b>{html_escape(source)}</b>",
        "",
        html_escape(title),
    ]
    if summary:
        parts.extend(["", html_escape(summary)])
    parts.extend(["", link])
    return "\n".join(parts)


def rss_phase(state: dict, first_run: bool, sent_budget: int) -> int:
    """Run RSS collection. Returns number of messages sent."""
    seen_urls = set(state["urls"])
    seen_titles = set(state["title_hashes"])

    stats = defaultdict(int)
    failed = []
    sent = 0

    log.info(f"RSS phase: {len(RSS_FEEDS)} sources, freshness={MAX_AGE_HOURS}h")

    for feed_info in RSS_FEEDS:
        name = feed_info["name"]
        url = feed_info["url"]

        try:
            # feedparser.parse(url) has NO built-in timeout and can hang
            # indefinitely if a server is slow or never closes the connection.
            # Fetch via requests with an explicit timeout first, then hand the
            # raw bytes to feedparser — this guarantees we never hang on a
            # single dead/slow source.
            resp = requests.get(
                url,
                timeout=15,
                headers={"User-Agent": "Mozilla/5.0 (compatible; GGNewsARBot/1.0)"},
            )
            resp.raise_for_status()
            d = feedparser.parse(resp.content)
            if d.bozo and not d.entries:
                raise RuntimeError(f"bozo={d.bozo_exception or d.bozo}")
            if not d.entries:
                raise RuntimeError("no entries")
            stats["sources_ok"] += 1
        except Exception as e:
            stats["sources_failed"] += 1
            failed.append(f"{name}: {e}")
            continue

        for entry in d.entries:
            stats["entries_total"] += 1

            link = (entry.get("link") or "").strip()
            title = (entry.get("title") or "").strip()
            summary = entry.get("summary") or entry.get("description") or ""

            if not link or not title:
                stats["skip_no_link_or_title"] += 1
                continue

            if link in seen_urls:
                stats["skip_seen_url"] += 1
                continue

            t_hash = title_hash(title)

            if not is_fresh(entry, MAX_AGE_HOURS):
                stats["skip_old"] += 1
                seen_urls.add(link); state["urls"].append(link)
                seen_titles.add(t_hash); state["title_hashes"].append(t_hash)
                continue

            if t_hash in seen_titles:
                stats["skip_dup_title"] += 1
                seen_urls.add(link); state["urls"].append(link)
                continue

            # Passes all gates. Mark seen regardless of send outcome.
            seen_urls.add(link); state["urls"].append(link)
            seen_titles.add(t_hash); state["title_hashes"].append(t_hash)

            if first_run:
                stats["baseline_recorded"] += 1
                continue

            if sent >= sent_budget:
                stats["skip_cap"] += 1
                # Roll back the marks so next run picks it up
                state["urls"].pop()
                state["title_hashes"].pop()
                seen_urls.discard(link)
                seen_titles.discard(t_hash)
                continue

            msg = format_rss_message(name, title, summary, link)
            if send_telegram(msg):
                sent += 1
                stats["sent"] += 1
                time.sleep(MESSAGE_DELAY_SECONDS)
            else:
                stats["send_failures"] += 1

    log.info("--- RSS Summary ---")
    for k in sorted(stats.keys()):
        log.info(f"  {k:30s} {stats[k]}")
    if failed:
        log.info(f"--- Failed Sources ({len(failed)}) ---")
        for line in failed:
            log.info(f"  - {line}")

    return sent


# ============================================================
# Liquipedia phase
# ============================================================
def fetch_liquipedia_revisions(wiki: str, pages: list, session: requests.Session) -> list:
    """Fetch latest revision for each page on a Liquipedia wiki."""
    if not pages:
        return []

    url = f"https://liquipedia.net/{wiki}/api.php"
    all_revs = []

    for i in range(0, len(pages), LIQUIPEDIA_BATCH_SIZE):
        batch = pages[i:i + LIQUIPEDIA_BATCH_SIZE]

        params = {
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "titles": "|".join(batch),
            "rvprop": "ids|timestamp|user|comment|size|flags",
            # NOTE: no rvlimit — incompatible with multi-title queries
            "maxlag": 5,
            "redirects": 1,
        }

        try:
            time.sleep(LIQUIPEDIA_RATE_LIMIT_SEC)
            r = session.get(url, params=params, timeout=30)

            if r.status_code == 503 or "X-Database-Lag" in r.headers:
                wait = int(r.headers.get("Retry-After", 60))
                log.warning(f"Liquipedia maxlag on {wiki}, waiting {wait}s")
                time.sleep(wait)
                continue

            r.raise_for_status()
            data = r.json()

            if "error" in data:
                log.error(f"Liquipedia API error on {wiki}: {data['error']}")
                continue

            for page_id, page_info in data.get("query", {}).get("pages", {}).items():
                if page_id == "-1" or "missing" in page_info:
                    continue

                page_title = page_info.get("title", "")
                slug = page_title.replace(" ", "_")

                for rev in page_info.get("revisions", []):
                    rev["page_title"] = page_title
                    rev["wiki"] = wiki
                    rev["page_url"] = f"https://liquipedia.net/{wiki}/{slug}"
                    rev["diff_url"] = (
                        f"https://liquipedia.net/{wiki}/index.php?"
                        f"title={slug}&diff={rev['revid']}&oldid={rev.get('parentid', 0)}"
                    )
                    all_revs.append(rev)

        except requests.RequestException as e:
            log.error(f"Liquipedia fetch failed on {wiki}: {e}")
        except ValueError as e:
            log.error(f"Liquipedia JSON parse failed on {wiki}: {e}")

    return all_revs


def is_meaningful_edit(rev: dict, prev_size: int) -> tuple[bool, str]:
    """Structural filter only — no keyword check. Drops bot/minor/tiny edits."""
    user = (rev.get("user") or "").lower()
    new_size = rev.get("size", 0)
    delta = abs(new_size - prev_size) if prev_size else new_size

    if "bot" in user:
        return False, "bot edit"
    if rev.get("minor"):
        return False, "marked minor"
    if delta < LIQUIPEDIA_MIN_BYTES_CHANGE:
        return False, f"tiny change ({delta} bytes)"
    return True, f"{delta} bytes changed"


def format_liquipedia_message(rev: dict, reason: str) -> str:
    game_emojis = {
        "counterstrike": "🔫", "valorant": "🎯", "leagueoflegends": "⚔️",
        "dota2": "🐉", "rainbowsix": "🛡️", "rocketleague": "🚀",
        "mobilelegends": "📱", "honorofkings": "👑", "pubgmobile": "🪂",
        "fighters": "🥊", "easportsfc": "⚽",
        "overwatch": "🧡", "pubg": "🪂", "apexlegends": "🅰️",
        "fortnite": "🌀", "teamfighttactics": "♟️", "callofduty": "🎖️",
    }
    game_names = {
        "counterstrike": "Counter Strike 2", "valorant": "VALORANT",
        "leagueoflegends": "League of Legends", "dota2": "Dota 2",
        "rainbowsix": "Rainbow Six Siege", "rocketleague": "Rocket League",
        "mobilelegends": "Mobile Legends", "honorofkings": "Honor of Kings",
        "pubgmobile": "PUBG Mobile", "fighters": "Fighting Games",
        "easportsfc": "EA Sports FC",
        "overwatch": "Overwatch", "pubg": "PUBG: BATTLEGROUNDS",
        "apexlegends": "Apex Legends", "fortnite": "Fortnite",
        "teamfighttactics": "Teamfight Tactics", "callofduty": "Call of Duty",
    }
    wiki = rev["wiki"]
    emoji = game_emojis.get(wiki, "🎮")
    game = game_names.get(wiki, wiki)

    page = html_escape(rev["page_title"])
    user = html_escape(rev.get("user") or "?")
    comment = html_escape((rev.get("comment") or "").strip()[:200] or "بدون ملاحظة")

    return (
        f"{emoji} <b>تحديث Liquipedia</b>\n\n"
        f"📄 <b>{page}</b>\n"
        f"🎮 {game}\n"
        f"👤 المحرر: <code>{user}</code>\n"
        f"💬 <i>{comment}</i>\n\n"
        f"🔗 <a href=\"{rev['page_url']}\">الصفحة</a>  |  "
        f"<a href=\"{rev['diff_url']}\">التعديل</a>"
    )


def liquipedia_phase(state: dict, first_run: bool, sent_budget: int) -> int:
    """Run Liquipedia collection. Returns number of messages sent."""
    lp_state = state["liquipedia"]
    sent = 0
    stats = defaultdict(int)

    total_pages = sum(len(p) for p in WATCHLIST.values())
    log.info(f"Liquipedia phase: {total_pages} pages across {len(WATCHLIST)} wikis")

    session = requests.Session()
    session.headers.update({
        "User-Agent": LIQUIPEDIA_USER_AGENT,
        "Accept-Encoding": "gzip",
    })

    for wiki, pages in WATCHLIST.items():
        if not pages:
            continue

        revisions = fetch_liquipedia_revisions(wiki, pages, session)
        stats[f"fetched_{wiki}"] = len(revisions)

        for rev in revisions:
            page_key = f"{wiki}:{rev['page_title']}"
            revid = str(rev.get("revid"))

            # A page never seen before (e.g. just added to watchlist.py) has
            # no recorded size yet. Without this check, prev_size defaults to
            # 0 below and the page's entire existing content gets treated as
            # a fresh "edit" — flooding the channel with false updates the
            # first time a new page is picked up. Treat it like first_run:
            # record the baseline silently, don't send.
            is_new_page = page_key not in lp_state

            page_state = lp_state.setdefault(page_key, {"revids": [], "size": 0})

            if revid in page_state["revids"]:
                stats["skip_seen_rev"] += 1
                continue

            page_state["revids"].append(revid)
            page_state["revids"] = page_state["revids"][-SEEN_REVS_PER_PAGE:]

            if first_run or is_new_page:
                page_state["size"] = rev.get("size", 0)
                stats["baseline_recorded"] += 1
                continue

            prev_size = page_state.get("size", 0)
            keep, reason = is_meaningful_edit(rev, prev_size)
            page_state["size"] = rev.get("size", 0)

            if not keep:
                stats[f"drop_{reason.split()[0]}"] += 1
                continue

            if sent >= sent_budget:
                stats["skip_cap"] += 1
                # Don't mark as seen so next run picks it up
                page_state["revids"].pop()
                continue

            msg = format_liquipedia_message(rev, reason)
            if send_telegram(msg):
                sent += 1
                stats["sent"] += 1
                time.sleep(MESSAGE_DELAY_SECONDS)
            else:
                stats["send_failures"] += 1

    log.info("--- Liquipedia Summary ---")
    for k in sorted(stats.keys()):
        log.info(f"  {k:30s} {stats[k]}")

    return sent


# ============================================================
# Main
# ============================================================
def main():
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        log.error("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID env vars")
        return

    state = load_state()

    # First run: no urls and no liquipedia entries means we haven't recorded
    # any baseline yet. Skip sending; just index everything.
    first_run = (
        len(state["urls"]) == 0
        and len(state["title_hashes"]) == 0
        and len(state["liquipedia"]) == 0
    )

    if first_run:
        log.info("FIRST RUN: indexing baseline, no messages will be sent.")

    rss_sent = rss_phase(state, first_run, MAX_MESSAGES_PER_RUN)
    remaining = MAX_MESSAGES_PER_RUN - rss_sent
    lp_sent = liquipedia_phase(state, first_run, remaining)

    save_state(state)

    log.info(f"=== Done. RSS sent: {rss_sent}, Liquipedia sent: {lp_sent} ===")


if __name__ == "__main__":
    main()
