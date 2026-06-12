"""
GGNewsAR Telegram bot — v2
Pure RSS forwarder with:
  - smart deduplication (URL + normalized title hash)
  - esports relevance filter (whitelist + blacklist, word boundary)
  - per source tier classification (Tier 1 bypasses filter, Tier 2 must pass it)
  - 48 hour freshness window
  - detailed run statistics in logs
"""

import os
import re
import json
import hashlib
import time
from datetime import datetime, timezone, timedelta

import feedparser
import requests

from feeds import FEEDS, ESPORTS_KEYWORDS, BLACKLIST_KEYWORDS

# Configuration

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

SEEN_FILE = "seen.json"
MAX_MESSAGES_PER_RUN = 100
MESSAGE_DELAY_SECONDS = 0.8
MAX_AGE_HOURS = 48
SEEN_RING_SIZE = 5000  # cap for seen.json to prevent unbounded growth

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

# Helpers

def normalize_title(title: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace."""
    t = title.lower()
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


def is_esports_relevant(title: str, summary: str, tier: int) -> bool:
    """
    Tier 1 sources are esports dedicated, always pass.
    Tier 2 sources must contain at least one esports keyword.
    Whitelist wins over blacklist (e.g. PSG Talon esports beats PSG FC blacklist).
    """
    if tier == 1:
        return True
    text = (title + " " + strip_html(summary)).lower()
    has_esports = any(re.search(r"\b" + re.escape(kw) + r"\b", text) for kw in ESPORTS_KEYWORDS)
    if has_esports:
        return True
    return False


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
        "sent": 0,
        "send_failures": 0,
    }

    failed_sources = []

    for feed_info in FEEDS:
        source_name = feed_info["name"]
        url = feed_info["url"]
        tier = feed_info.get("tier", 2)

        try:
            d = feedparser.parse(url)
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

            if not is_recent(entry, MAX_AGE_HOURS):
                stats["skip_old"] += 1
                seen_urls.add(link)
                new_urls.append(link)
                continue

            t_hash = title_hash(title)
            if t_hash in seen_titles:
                stats["skip_dup_title"] += 1
                seen_urls.add(link)
                new_urls.append(link)
                continue

            if not is_esports_relevant(title, summary, tier):
                stats["skip_irrelevant"] += 1
                seen_urls.add(link)
                new_urls.append(link)
                continue

            # Passed all checks
            seen_urls.add(link)
            seen_titles.add(t_hash)
            new_urls.append(link)
            new_titles.append(t_hash)

            if first_run:
                continue

            if sent_count >= MAX_MESSAGES_PER_RUN:
                continue

            message = format_message(source_name, title, summary, link)
            if send_to_telegram(message):
                sent_count += 1
                stats["sent"] += 1
            else:
                stats["send_failures"] += 1
            time.sleep(MESSAGE_DELAY_SECONDS)

    # Persist state
    seen["urls"] = list({*seen["urls"], *new_urls})
    seen["titles"] = list({*seen["titles"], *new_titles})
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
