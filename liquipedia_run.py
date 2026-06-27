"""
GGNewsAR Bot — Liquipedia Runner
Entry point that orchestrates the Liquipedia watcher.
Run from GitHub Actions or cron: python liquipedia_run.py
"""

import os
import json
import time
import logging
from pathlib import Path

import requests

from liquipedia_watcher import (
    fetch_page_revisions,
    is_significant_change,
    format_for_telegram,
    USER_AGENT,
)
from watchlist import WATCHLIST, total_pages, all_wikis

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

STATE_FILE = Path("liquipedia_state.json")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def load_state() -> dict:
    """Load persisted state (seen revisions, page sizes)."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            logger.error("State file corrupted, starting fresh")
    return {"seen_revids": {}, "page_sizes": {}, "first_run": True}


def save_state(state: dict):
    """Persist state to disk."""
    STATE_FILE.write_text(
        json.dumps(state, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def send_to_telegram(message: str) -> bool:
    """Send an HTML message to the configured Telegram chat."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.error("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        if not response.ok:
            logger.error(f"Telegram error {response.status_code}: {response.text}")
            return False
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Telegram request failed: {e}")
        return False


def run_once():
    """Single pass: fetch revisions for all wikis, post significant ones."""
    state = load_state()
    seen = state.get("seen_revids", {})
    sizes = state.get("page_sizes", {})
    first_run = state.get("first_run", False)
    
    if first_run:
        logger.info("First run detected. Will record baseline, no posts sent.")
    
    logger.info(f"Watching {total_pages()} pages across {len(all_wikis())} wikis")
    
    posted = 0
    skipped_seen = 0
    skipped_insig = 0
    
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept-Encoding": "gzip"})
    
    for wiki, pages in WATCHLIST.items():
        if not pages:
            continue
        
        logger.info(f"  → {wiki}: {len(pages)} pages")
        
        revisions = fetch_page_revisions(wiki, pages, session=session)
        logger.info(f"    fetched {len(revisions)} revisions")
        
        for rev in revisions:
            page_key = f"{wiki}:{rev['page_title']}"
            revid = str(rev.get("revid"))
            
            # Skip seen revisions
            seen_for_page = seen.setdefault(page_key, [])
            if revid in seen_for_page:
                skipped_seen += 1
                continue
            
            # Always update state, even if we don't post
            seen_for_page.append(revid)
            # Keep only the last 20 revids per page
            seen[page_key] = seen_for_page[-20:]
            
            # On first run, just record everything without posting
            if first_run:
                sizes[page_key] = rev.get("size", 0)
                continue
            
            # Check significance
            prev_size = sizes.get(page_key)
            is_sig, reason = is_significant_change(rev, prev_size)
            
            sizes[page_key] = rev.get("size", 0)
            
            if not is_sig:
                skipped_insig += 1
                logger.debug(f"    SKIP {page_key}: {reason}")
                continue
            
            # Post to Telegram
            message = format_for_telegram(rev, reason)
            if send_to_telegram(message):
                posted += 1
                logger.info(f"    POSTED {page_key}: {reason}")
                time.sleep(1.5)  # Telegram chat rate limit
            else:
                logger.error(f"    FAILED to post {page_key}")
    
    # Clear first_run flag after baseline
    if first_run:
        state["first_run"] = False
        logger.info("Baseline recorded. Next run will start posting.")
    
    state["seen_revids"] = seen
    state["page_sizes"] = sizes
    save_state(state)
    
    logger.info(
        f"Done. Posted: {posted} | Skipped (seen): {skipped_seen} | "
        f"Skipped (insignificant): {skipped_insig}"
    )


if __name__ == "__main__":
    run_once()
