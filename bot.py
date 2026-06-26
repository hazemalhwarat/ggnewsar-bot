"""
GGNewsAR Telegram bot — v5
Pure RSS forwarder with:
  • smart deduplication (URL + normalized title hash, source suffix stripped)
  • STRICT esports relevance: an item must be about one of your titles / the
    esports scene (scope) AND about the competitive scene (context). Game
    content (skins, patches, guides, lore) and non listed games are dropped.
  • match result suppression (drops live scores / routine results,
    keeps finals, titles and championship moments)
  • 12 hour freshness window (sized for a fast schedule, never delays)
  • cap protection (overflow items not marked seen, picked up next run)
  • detailed run statistics in logs
"""

import os
import re
import json
import hashlib
import time
from datetime import datetime, timezone, timedelta

import feedparser
import requests

from feeds import FEEDS, TITLE_SCOPE, CONTEXT_SIGNALS, BLACKLIST_KEYWORDS

# Configuration
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

SEEN_FILE = "seen.json"
MAX_MESSAGES_PER_RUN = 200          # raised from 100 for safety margin
MESSAGE_DELAY_SECONDS = 0.8
MAX_AGE_HOURS = 12                  # only ignore items older than this. NOT a delay.
SEEN_RING_SIZE = 8000               # raised from 5000 to fit volume

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

# Some sites (Cloudflare / WordPress) return an empty page to the default
# feedparser agent. A normal browser User-Agent fixes most of those.
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)

# Explicit esports words. If one of these is present, the traditional sports
# guard is skipped (e.g. "esports nations cup" near "nations" is fine).
ESPORTS_WORDS = ["esports", "esport", "e-sports", "e-sport"]

# Source suffix patterns that Google News and other aggregators append
SOURCE_SUFFIX_RE = re.compile(
    r"\s*[\-\|\u2013\u2014:]\s*[^\-\|\u2013\u2014:]{1,40}$"
)

# Match result suppression
# RESULT_PATTERNS flag a routine / live score (candidate to drop).
# CHAMPION_PATTERNS override the drop, so finals and titles always pass.
RESULT_PATTERNS = re.compile(
    r"\blive\b[: ]|\blive blog\b|\bresults?\b|\brecap\b|\bround-?up\b|\bstandings\b|"
    r"\b\d{1,2}\s?[-\u2013:]\s?\d{1,2}\b|"
    r"\b(beat|beats|defeat|defeats|def\.|downs|edge|edges|topple|overcome)\b|"
    r"\bvs\.?\b|\bhead to head\b",
    re.I,
)
CHAMPION_PATTERNS = re.compile(
    r"\bgrand final\b|\bworld champion|\bchampions\b|\bchampionship\b|"
    r"\bwins? the (major|championship|cup|title|world)|\bcrowned\b|"
    r"\blift(s)? the trophy\b|\bclaim(s)? the title\b|\bfirst (ever )?major\b|"
    r"\bwins? (iem|esl|blast|ewc|rlcs|vct|the international|worlds|msi)\b|"
    r"\btitle\b|\btrophy\b",
    re.I,
)

# Helpers
def normalize_title(title: str) -> str:
    """Lowercase, strip source suffix, strip punctuation, collapse whitespace."""
    t = title.lower().strip()
    # strip trailing " — Source" / " | Source" / " : Source" (once)
    t = SOURCE_SUFFIX_RE.sub("", t).strip()
    # strip punctuation
    t = re.sub(r"[^\w\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def title_hash(title: str) -> str:
    return hashlib.md5(normalize_title(title).encode("utf-8")).hexdigest()


def strip_html(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def is_recent(entry, max_age_hours: int) -> bool:
    """Reject items older than max_age_hours. If no date, accept (RSS quirk)."""
    pub = getattr(entry, "published_parsed", None) or getattr(entry, "updated_parsed", None)
    if not pub:
        return True
    pub_time = datetime(*pub[:6], tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - pub_time) <= timedelta(hours=max_age_hours)


def has_any(text: str, keywords) -> bool:
    return any(re.search(r"\b" + re.escape(kw.strip()) + r"\b", text) for kw in keywords)


def is_esports_relevant(title: str, summary: str, tier: int) -> bool:
    """
    STRICT. Keep an item only if:
      1) it mentions one of your titles / circuits / orgs / the esports scene
         (TITLE_SCOPE), AND
      2) it is about the competitive scene, not game content (CONTEXT_SIGNALS).
    A traditional sports / entertainment guard blocks items that hit the
    blacklist without any explicit esports word. Tier does not relax the two
    gates; it only keeps the guard a touch softer for trusted esports outlets.
    """
    text = (title + " " + strip_html(summary)).lower()

    # Gate 1: is it about one of your titles / the esports scene?
    if not has_any(text, TITLE_SCOPE):
        return False

    # Gate 2: is it about the competitive scene (not skins / patches / guides)?
    if not has_any(text, CONTEXT_SIGNALS):
        return False

    # Guard: traditional sports / entertainment, unless an esports word is present
    if has_any(text, BLACKLIST_KEYWORDS) and not has_any(text, ESPORTS_WORDS):
        return False

    return True


def is_match_result_spam(title: str, summary: str) -> bool:
    """
    True  = looks like a live / routine match result -> drop it.
    False = keep it.
    Finals, titles and championship moments are protected and always kept.
    """
    text = (title + " " + strip_html(summary)).lower()
    if CHAMPION_PATTERNS.search(text):
        return False                      # title moment -> keep
    return bool(RESULT_PATTERNS.search(text))


def load_seen() -> dict:
    """Load seen state. Supports old format (list of urls) for backward compat."""
    if not os.path.exists(SEEN_FILE):
        return {"urls": [], "titles": []}
    try:
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"urls": [], "titles": []}
    if isinstance(data, list):
        return {"urls": data, "titles": []}
    return {
        "urls": data.get("urls", []),
        "titles": data.get("titles", []),
    }


def merge_preserve_order(existing: list, new_items: list) -> list:
    """Append new items to existing in order, deduped, keeping oldest first."""
    seen_set = set(existing)
    out = list(existing)
    for item in new_items:
        if item not in seen_set:
            out.append(item)
            seen_set.add(item)
    return out


def save_seen(seen: dict) -> None:
    seen["urls"] = seen["urls"][-SEEN_RING_SIZE:]
    seen["titles"] = seen["titles"][-SEEN_RING_SIZE:]
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(seen, f, ensure_ascii=False, indent=2)


def format_message(source_name: str, title: str, summary: str, link: str) -> str:
    summary_clean = strip_html(summary)[:280]
    parts = [f"<b>{source_name}</b>", "", title]
    if summary_clean:
        parts.extend(["", summary_clean])
    parts.extend(["", link])
    return "\n".join(parts)


def send_to_telegram(text: str) -> bool:
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    try:
        r = requests.post(TELEGRAM_API, data=payload, timeout=15)
        if r.status_code != 200:
            print(f"  Telegram error {r.status_code}: {r.text[:200]}")
            return False
        return True
    except Exception as e:
        print(f"  Telegram exception: {e}")
        return False


# Main
def main() -> None:
    seen = load_seen()
    seen_urls = set(seen["urls"])
    seen_titles = set(seen["titles"])

    first_run = len(seen_urls) == 0
    if first_run:
        print("First run detected. Indexing existing items silently, no messages sent.")

    sent_count = 0
    new_urls = []
    new_titles = []

    stats = {
        "sources_ok": 0,
        "sources_failed": 0,
        "entries_seen_total": 0,
        "skip_seen_url": 0,
        "skip_old": 0,
        "skip_dup_title": 0,
        "skip_irrelevant": 0,
        "skip_result": 0,
        "skip_cap": 0,
        "sent": 0,
        "send_failures": 0,
    }

    failed_sources = []

    for feed_info in FEEDS:
        source_name = feed_info["name"]
        url = feed_info["url"]
        tier = feed_info.get("tier", 2)

        try:
            d = feedparser.parse(url, agent=USER_AGENT)
            if not d.entries:
                raise RuntimeError(f"no entries (bozo={d.bozo})")
            stats["sources_ok"] += 1
        except Exception as e:
            stats["sources_failed"] += 1
            failed_sources.append(f"{source_name}: {e}")
            continue

        for entry in d.entries:
            stats["entries_seen_total"] += 1
            link = (entry.get("link") or "").strip()
            title = (entry.get("title") or "").strip()
            summary = entry.get("summary") or entry.get("description") or ""

            if not link or not title:
                continue

            if link in seen_urls:
                stats["skip_seen_url"] += 1
                continue

            t_hash = title_hash(title)

            if not is_recent(entry, MAX_AGE_HOURS):
                stats["skip_old"] += 1
                seen_urls.add(link)
                seen_titles.add(t_hash)
                new_urls.append(link)
                new_titles.append(t_hash)
                continue

            if t_hash in seen_titles:
                stats["skip_dup_title"] += 1
                seen_urls.add(link)
                new_urls.append(link)
                continue

            if not is_esports_relevant(title, summary, tier):
                stats["skip_irrelevant"] += 1
                seen_urls.add(link)
                seen_titles.add(t_hash)
                new_urls.append(link)
                new_titles.append(t_hash)
                continue

            if is_match_result_spam(title, summary):
                stats["skip_result"] += 1
                seen_urls.add(link)
                seen_titles.add(t_hash)
                new_urls.append(link)
                new_titles.append(t_hash)
                continue

            # Cap check BEFORE marking as seen
            # Overflow items stay unseen so the next run picks them up.
            if not first_run and sent_count >= MAX_MESSAGES_PER_RUN:
                stats["skip_cap"] += 1
                continue

            # Passed all checks AND under cap
            seen_urls.add(link)
            seen_titles.add(t_hash)
            new_urls.append(link)
            new_titles.append(t_hash)

            if first_run:
                continue

            message = format_message(source_name, title, summary, link)
            if send_to_telegram(message):
                sent_count += 1
                stats["sent"] += 1
            else:
                stats["send_failures"] += 1
            time.sleep(MESSAGE_DELAY_SECONDS)

    # Persist state, preserving insertion order (oldest first)
    seen["urls"] = merge_preserve_order(seen["urls"], new_urls)
    seen["titles"] = merge_preserve_order(seen["titles"], new_titles)
    save_seen(seen)

    # Logs
    print("\n=== Run Summary ===")
    for k, v in stats.items():
        print(f"  {k:25s} {v}")

    if failed_sources:
        print(f"\n=== Failed Sources ({len(failed_sources)}) ===")
        for line in failed_sources:
            print(f"  - {line}")


if __name__ == "__main__":
    main()
