"""
GGNewsAR Bot — Filters Module
Called from bot.py as: should_send(title, summary, tier) -> (bool, reason)

Returned reason is used in stats[f"drop_{reason}"], so reasons should be
short snake_case strings, no spaces.

Logic:
  1. Drop spam/off-topic (gambling, casino, betting predictions, etc).
  2. Tier 1 sources (primary game-specific): pass through (trusted).
  3. Tier 2 sources (aggregators): require an esports keyword in title/summary.
  4. Pure match scoreline-only posts (no editorial words): dropped.
"""

import re

# ---------------------------------------------------------------------------
# Esports keyword whitelist
# ---------------------------------------------------------------------------
ESPORTS_KEYWORDS = [
    # Generic
    "esports", "esport", "e-sports",
    # CS / CS2
    "cs2", "counter-strike", "counterstrike", "csgo", "cs:go",
    "hltv", "iem", "blast", "pgl", "esl pro league", "esl one",
    # VALORANT
    "valorant", "vct", "masters", "champions tour",
    # LoL
    "league of legends", "lol esports", "lck", "lec", "lpl", "lcs",
    "worlds 20", "world championship", "msi", "mid-season invitational",
    # Dota 2
    "dota 2", "dota2", "the international", "dpc", "blast slam",
    # R6
    "rainbow six", "siege", "six invitational", "siegegg",
    # Rocket League
    "rocket league", "rlcs", "octane",
    # Mobile esports
    "mobile legends", "mlbb", "mpl", "m series", "msc",
    "honor of kings", "kpl", "king pro league",
    "pubg mobile", "pmgc", "pmsl", "pubg",
    # Apex
    "apex legends", "algs",
    # Overwatch
    "overwatch", "owcs", "ow2",
    # FGC
    "tekken", "street fighter", "mortal kombat", "guilty gear",
    "evo", "evolution championship", "capcom cup", "fgc",
    # EA FC / FIFA
    "ea fc", "ea sports fc", "fifa esports", "fc pro",
    "fifae", "eworld cup",
    # CoD
    "call of duty", "cdl", "cod league", "warzone",
    # Tournament organizers and big events
    "esports world cup", "ewc 2026", "gamers8",
    "dreamhack", "iesf", "olympic esports",
    # Roster/business actions
    "roster move", "lineup change", "signs ", "signing", "transfers to",
    "joins ", "leaves ", "released by", "benched", "stand-in",
    "qualifies for", "qualifier", "eliminated", "wins ",
    "grand final", "playoff", "group stage", "prize pool",
    "champion", "trophy",
    # Arab orgs (always relevant for GGNewsAR)
    "falcons", "twisted minds", "nigma galaxy", "geekay", "fate esports",
    "saudi esports", "ksa esports", "mena esports",
]

# ---------------------------------------------------------------------------
# Drop list (spam / off-topic / regulated content)
# ---------------------------------------------------------------------------
DROP_KEYWORDS = [
    # Gambling content
    "betting tips", "best odds", "predictions and odds", "betting predictions",
    "best esports betting", "casino bonus", "deposit bonus", "free spins",
    "slot machine", "online casino", "promo code", "sportsbook review",
    # Off-topic
    "horoscope", "celebrity gossip", "weight loss",
    # Hardware reviews (not esports news)
    "best gaming chair", "best gaming mouse review",
]

# Patterns that indicate a pure scoreline-only post
# (we want news, not match results spam)
SCORELINE_RE = re.compile(r"\b\d{1,2}\s*[-:]\s*\d{1,2}\b")

# News-y words that justify keeping a scoreline post (it's a recap, not a score)
NEWSY_WORDS = [
    "news", "report", "announcement", "interview", "analysis",
    "recap", "review", "controversy", "scandal", "ban", "penalty",
    "comeback", "upset", "stuns", "claims title", "lifts trophy",
    "advance", "advances", "secure", "secures",
]


def should_send(title: str, summary: str, tier: int = 2) -> tuple[bool, str]:
    """
    Decide whether an RSS entry should be sent to Telegram.

    Returns:
        (decision, reason). The reason is used in stats[f"drop_{reason}"]
        so keep it short snake_case.
    """
    title = (title or "").strip()
    summary = (summary or "").strip()

    if not title:
        return False, "no_title"

    full_text = (title + " " + summary).lower()

    # Drop spam first (applies to all tiers)
    for kw in DROP_KEYWORDS:
        if kw in full_text:
            return False, "spam_keyword"

    # Tier 1: trusted primary game sites
    if tier == 1:
        # Even tier 1: drop scoreline-only short titles with no editorial framing
        if len(title) < 60 and SCORELINE_RE.search(title):
            if not any(w in full_text for w in NEWSY_WORDS):
                return False, "scoreline_only"
        return True, "tier1_pass"

    # Tier 2+: require at least one esports keyword
    if not any(kw in full_text for kw in ESPORTS_KEYWORDS):
        return False, "no_esports_match"

    # Tier 2 scoreline guard (same as tier 1)
    if len(title) < 60 and SCORELINE_RE.search(title):
        if not any(w in full_text for w in NEWSY_WORDS):
            return False, "scoreline_only"

    return True, "ok"
