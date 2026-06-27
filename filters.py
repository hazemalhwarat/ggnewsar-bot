"""
GGNewsAR Bot — Filters Module
Decides which feed entries should be sent to Telegram.

Minimal implementation to keep the legacy bot.py running after
we replaced feeds.py. If the original filters.py had additional rules
(drop keywords, source-specific logic), drop them into the lists below.
"""

import re


# Patterns in the article title that mark it as noise (case-insensitive regex)
DROP_TITLE_PATTERNS = [
    # Add patterns here as you spot noise. Examples:
    # r'\bsponsored\b',
    # r'\bgiveaway\b',
    # r'\bpromo code\b',
]

# Patterns in the article URL that mark the source as noise
DROP_URL_PATTERNS = [
    # Examples:
    # r'/sponsored/',
    # r'/promo/',
]

# Minimum title length to consider an entry valid
MIN_TITLE_LENGTH = 10


def should_send(entry) -> bool:
    """
    Return True if the feed entry should be sent to Telegram.
    Called by bot.py inside the main feed loop.
    
    Accepts feedparser entry objects (which support both .attr and ['key']).
    """
    # Extract title and link defensively
    if hasattr(entry, 'get'):
        title = entry.get('title', '') or ''
        link = entry.get('link', '') or ''
    else:
        title = getattr(entry, 'title', '') or ''
        link = getattr(entry, 'link', '') or ''
    
    title = title.strip()
    link = link.strip()
    
    # Must have both
    if not title or not link:
        return False
    
    # Title must be meaningful
    if len(title) < MIN_TITLE_LENGTH:
        return False
    
    # Apply drop patterns
    title_lower = title.lower()
    link_lower = link.lower()
    
    for pattern in DROP_TITLE_PATTERNS:
        if re.search(pattern, title_lower, re.IGNORECASE):
            return False
    
    for pattern in DROP_URL_PATTERNS:
        if re.search(pattern, link_lower, re.IGNORECASE):
            return False
    
    return True
