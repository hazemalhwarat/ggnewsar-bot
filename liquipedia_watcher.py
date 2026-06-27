"""
GGNewsAR Bot — Liquipedia Watcher
Monitors edits to important esports pages on Liquipedia via MediaWiki API.
Respects Liquipedia's strict rate limits and Terms of Use.
"""

import time
import logging
from typing import Optional
import requests

logger = logging.getLogger(__name__)

# Liquipedia API requires custom User-Agent identifying the client
# https://liquipedia.net/api-terms-of-use
USER_AGENT = "GGNewsAR Bot/1.0 (https://ggnewsar.com; hazem@ggnewsar.com)"

# Liquipedia hard limit: 1 request per 2 seconds on action=query
# We use 2.5s to be safe
QUERY_RATE_LIMIT = 2.5

# MediaWiki accepts up to 50 page titles per query (500 for bots, we don't have that)
MAX_TITLES_PER_QUERY = 50

# Sections in edit summaries that signal real news
SIGNIFICANT_KEYWORDS = [
    "roster", "lineup", "transfer", "signing", "signed",
    "release", "released", "departure", "leave", "left",
    "result", "champion", "winner", "qualif", "eliminat",
    "achievement", "trophy", "title",
    "history", "career", "join", "joining",
    "ban", "suspended", "penalty",
]

# Edit summary patterns that are noise
TRIVIAL_KEYWORDS = [
    "typo", "fix", "spelling", "grammar",
    "infobox", "template", "category",
    "image", "logo", "flag",
    "stub", "wikilink", "format",
    "ref", "reference", "source",
    "navbox", "redirect",
]


class LiquipediaError(Exception):
    """Raised when Liquipedia API behaves unexpectedly."""


def fetch_page_revisions(wiki: str, pages: list[str], session: Optional[requests.Session] = None) -> list[dict]:
    """
    Fetch the latest revisions for a batch of pages on a Liquipedia wiki.
    
    Args:
        wiki: subdomain like "counterstrike", "valorant", "leagueoflegends"
        pages: page titles (use underscores, not spaces)
        session: optional requests.Session for connection reuse
    
    Returns:
        List of revision dicts with: page_title, revid, parentid, timestamp,
        user, comment, size, url, diff_url, wiki
    """
    if not pages:
        return []
    
    if session is None:
        session = requests.Session()
        session.headers.update({"User-Agent": USER_AGENT, "Accept-Encoding": "gzip"})
    
    url = f"https://liquipedia.net/{wiki}/api.php"
    
    all_revisions = []
    
    # Batch pages (50 per query)
    for i in range(0, len(pages), MAX_TITLES_PER_QUERY):
        batch = pages[i:i + MAX_TITLES_PER_QUERY]
        
        params = {
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "titles": "|".join(batch),
            "rvprop": "ids|timestamp|user|comment|size|flags",
            # NOTE: rvlimit is NOT compatible with multi-title queries.
            # MediaWiki returns the latest revision per title automatically.
            "maxlag": 5,
            "redirects": 1,
        }
        
        try:
            time.sleep(QUERY_RATE_LIMIT)
            response = session.get(url, params=params, timeout=30)
            
            # maxlag tells us the server is overloaded; back off
            if response.status_code == 503 or "X-Database-Lag" in response.headers:
                wait = int(response.headers.get("Retry-After", 60))
                logger.warning(f"Liquipedia maxlag on {wiki}, waiting {wait}s")
                time.sleep(wait)
                continue
            
            response.raise_for_status()
            data = response.json()
            
            if "error" in data:
                logger.error(f"API error on {wiki}: {data['error']}")
                continue
            
            pages_data = data.get("query", {}).get("pages", {})
            
            for page_id, page_info in pages_data.items():
                # page_id == "-1" means the page does not exist
                if page_id == "-1" or "missing" in page_info:
                    logger.debug(f"Page missing: {page_info.get('title')}")
                    continue
                
                page_title = page_info.get("title", "")
                page_url_slug = page_title.replace(" ", "_")
                
                for rev in page_info.get("revisions", []):
                    rev["page_title"] = page_title
                    rev["wiki"] = wiki
                    rev["url"] = f"https://liquipedia.net/{wiki}/{page_url_slug}"
                    rev["diff_url"] = (
                        f"https://liquipedia.net/{wiki}/index.php?"
                        f"title={page_url_slug}&diff={rev['revid']}&oldid={rev.get('parentid', 0)}"
                    )
                    all_revisions.append(rev)
        
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout on {wiki} batch {i // MAX_TITLES_PER_QUERY}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed on {wiki}: {e}")
        except ValueError as e:
            logger.error(f"JSON parse failed on {wiki}: {e}")
    
    return all_revisions


def is_significant_change(revision: dict, prev_size: Optional[int] = None) -> tuple[bool, str]:
    """
    Decide whether a revision is news worthy.
    
    Returns:
        (is_significant, reason)
    """
    
    user = revision.get("user", "").lower()
    comment = revision.get("comment", "").lower()
    new_size = revision.get("size", 0)
    delta = abs(new_size - prev_size) if prev_size else new_size
    
    # Bot edits are template updates, formatting, etc.
    if "bot" in user or revision.get("flags", {}).get("bot"):
        return (False, "bot edit")
    
    # Editor flagged it as minor
    if revision.get("minor"):
        return (False, "marked as minor")
    
    # Tiny changes are almost always typos or formatting
    if delta < 80:
        return (False, f"trivial size change ({delta} bytes)")
    
    # Trivial keywords in edit comment
    for trivial in TRIVIAL_KEYWORDS:
        if trivial in comment:
            return (False, f"trivial: '{trivial}' in comment")
    
    # Significant keywords win immediately
    for sig in SIGNIFICANT_KEYWORDS:
        if sig in comment:
            return (True, f"keyword: '{sig}' in comment")
    
    # Big changes without a clear signal are still worth flagging
    if delta >= 500:
        return (True, f"large change ({delta} bytes)")
    
    if delta >= 200:
        return (True, f"medium change ({delta} bytes)")
    
    return (False, f"unclear change ({delta} bytes, no keywords)")


def format_for_telegram(revision: dict, reason: str) -> str:
    """Format a revision as a Telegram HTML message."""
    
    game_emojis = {
        "counterstrike": "🔫",
        "valorant": "🎯",
        "leagueoflegends": "⚔️",
        "dota2": "🐉",
        "rainbowsix": "🛡️",
        "rocketleague": "🚀",
        "mobilelegends": "📱",
        "honorofkings": "👑",
        "pubgmobile": "🪂",
    }
    
    game_names_ar = {
        "counterstrike": "Counter Strike 2",
        "valorant": "VALORANT",
        "leagueoflegends": "League of Legends",
        "dota2": "Dota 2",
        "rainbowsix": "Rainbow Six Siege",
        "rocketleague": "Rocket League",
        "mobilelegends": "Mobile Legends",
        "honorofkings": "Honor of Kings",
        "pubgmobile": "PUBG Mobile",
    }
    
    wiki = revision["wiki"]
    emoji = game_emojis.get(wiki, "🎮")
    game_name = game_names_ar.get(wiki, wiki)
    
    page = revision["page_title"]
    user = revision.get("user", "Unknown")
    comment = revision.get("comment", "بدون ملاحظة")[:200]
    size = revision.get("size", 0)
    timestamp = revision.get("timestamp", "")
    
    # Escape HTML chars in user content
    page_safe = page.replace("<", "&lt;").replace(">", "&gt;")
    comment_safe = comment.replace("<", "&lt;").replace(">", "&gt;")
    user_safe = user.replace("<", "&lt;").replace(">", "&gt;")
    
    return (
        f"{emoji} <b>تحديث Liquipedia</b>\n\n"
        f"📄 <b>{page_safe}</b>\n"
        f"🎮 {game_name}\n"
        f"👤 المحرر: <code>{user_safe}</code>\n"
        f"💬 <i>{comment_safe}</i>\n"
        f"📊 السبب: {reason}\n"
        f"📦 الحجم الحالي: {size:,} بايت\n\n"
        f"🔗 <a href=\"{revision['url']}\">الصفحة</a>  |  "
        f"<a href=\"{revision['diff_url']}\">التعديل</a>"
    )
