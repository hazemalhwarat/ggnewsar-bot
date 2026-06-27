"""
GGNewsAR Telegram bot — v7 (rebuilt from scratch)

Pipeline (per entry):
  freshness (12h)  ->  url dedup  ->  title dedup  ->  filters.should_send  ->  cap  ->  send

Statistics:
  Every drop reason from filters.py is counted separately, so the Actions
  log shows you exactly why each item didn't make it through. Failed
  feeds are listed at the bottom.

Configuration (top of file): freshness window, cap, message format.
All relevance logic lives in filters.py; all sources in feeds.py.
"""

import os
import re
import json
import hashlib
import time
from collections import defaultdict
from datetime import datetime, timezone, timedelta

import feedparser
import requests

from feeds import FEEDS
from filters import should_send

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

SEEN_FILE = "seen.json"
MAX_MESSAGES_PER_RUN = 40            # per user spec
MESSAGE_DELAY_SECONDS = 0.8
MAX_AGE_HOURS = 12                   # ignore items older than this; not a delay
SEEN_RING_SIZE = 8000

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

# Source suffix Google News and aggregators append to titles
SOURCE_SUFFIX_RE = re.compile(r"\s*[\-\|\u2013\u2014:]\s*[^\-\|\u2013\u2014:]{1,40}$")


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def normalize_title(title: str) -> str:
    t = title.lower().strip()
    t = SOURCE_SUFFIX_RE.sub("", t).strip()
    t = re.sub(r"[^\w\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def title_hash(title: str) -> str:
    return hashlib.md5(normalize_title(title).encode("utf-8")).hexdigest()


def strip_html(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def is_recent(entry, max_age_hours: int) -> bool:
    pub = getattr(entry, "published_parsed", None) or getattr(entry, "updated_parsed", None)
    if not pub:
        return True
    pub_time = datetime(*pub[:6], tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - pub_time) <= timedelta(hours=max_age_hours)


# ----------------------------------------------------------------------------
# State (seen URLs and titles, persisted across runs)
# ----------------------------------------------------------------------------
def load_seen() -> dict:
    if not os.path.exists(SEEN_FILE):
        return {"urls": [], "titles": []}
    try:
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"urls": [], "titles": []}
    if isinstance(data, list):
        return {"urls": data, "titles": []}
    return {"urls": data.get("urls", []), "titles": data.get("titles", [])}


def merge_preserve_order(existing: list, new_items: list) -> list:
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


# ----------------------------------------------------------------------------
# Telegram
# ----------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main() -> None:
    seen = load_seen()
    seen_urls = set(seen["urls"])
    seen_titles = set(seen["titles"])

    first_run = len(seen_urls) == 0
    if first_run:
        print("First run detected. Indexing existing items silently, no messages sent.")

    sent_count = 0
    new_urls: list = []
    new_titles: list = []

    stats = defaultdict(int)
    failed_sources: list = []

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

            # url dedup
            if link in seen_urls:
                stats["skip_seen_url"] += 1
                continue

            t_hash = title_hash(title)

            # freshness
            if not is_recent(entry, MAX_AGE_HOURS):
                stats["skip_old"] += 1
                seen_urls.add(link); new_urls.append(link)
                seen_titles.add(t_hash); new_titles.append(t_hash)
                continue

            # title dedup
            if t_hash in seen_titles:
                stats["skip_dup_title"] += 1
                seen_urls.add(link); new_urls.append(link)
                continue

            # relevance + match-result guard (filters.py)
            send, reason = should_send(title, summary, tier)
            if not send:
                stats[f"drop_{reason}"] += 1
                seen_urls.add(link); new_urls.append(link)
                seen_titles.add(t_hash); new_titles.append(t_hash)
                continue

            # cap (do NOT mark as seen, so next run picks them up)
            if not first_run and sent_count >= MAX_MESSAGES_PER_RUN:
                stats["skip_cap"] += 1
                continue

            # passed everything
            seen_urls.add(link); new_urls.append(link)
            seen_titles.add(t_hash); new_titles.append(t_hash)

            if first_run:
                continue

            message = format_message(source_name, title, summary, link)
            if send_to_telegram(message):
                sent_count += 1
                stats["sent"] += 1
            else:
                stats["send_failures"] += 1
            time.sleep(MESSAGE_DELAY_SECONDS)

    # persist state
    seen["urls"] = merge_preserve_order(seen["urls"], new_urls)
    seen["titles"] = merge_preserve_order(seen["titles"], new_titles)
    save_seen(seen)

    # logs
    print("\n=== Run Summary ===")
    for k in sorted(stats.keys()):
        print(f"  {k:30s} {stats[k]}")

    if failed_sources:
        print(f"\n=== Failed Sources ({len(failed_sources)}) ===")
        for line in failed_sources:
            print(f"  - {line}")


if __name__ == "__main__":
    main()
