"""
GGNewsAR Bot — Feed Configuration (Verified Working Only)
Cleaned after live test on 2026-06-27.

Removed 26 dead/incorrect endpoints. Will reintroduce verified replacements
in a future session. For now, FEEDS contains only confirmed-working sources.
"""

TYPE_PRIMARY = "rss_primary"
TYPE_AGGREGATOR = "rss_aggregator"
TYPE_LIQUIPEDIA = "liquipedia_rss"
TYPE_REDDIT = "reddit"
TYPE_SCRAPE = "scrape"


# ============================================================
# Verified working RSS feeds (confirmed in live test)
# ============================================================
RSS_FEEDS = [
    # Primary game-specific (tier 1)
    {"name": "HLTV", "url": "https://www.hltv.org/rss/news",
     "game": "cs2", "type": TYPE_PRIMARY, "verified": True},
    {"name": "VLR.gg", "url": "https://vlr.gg/rss",
     "game": "valorant", "type": TYPE_PRIMARY, "verified": True},
    {"name": "Dotabuff Blog", "url": "https://www.dotabuff.com/blog.rss",
     "game": "dota2", "type": TYPE_PRIMARY, "verified": True},

    # Multi-game aggregators (tier 2)
    {"name": "Dot Esports", "url": "https://dotesports.com/feed",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": True},
    {"name": "Esports Insider", "url": "https://esportsinsider.com/feed",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": True},
    {"name": "ESTNN", "url": "https://estnn.com/feed",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": True},
    {"name": "Esports News UK", "url": "https://esports-news.co.uk/feed",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": True},
    {"name": "Insider Gaming", "url": "https://insider-gaming.com/feed",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": True},
    {"name": "The Esports Radar", "url": "https://esportsradar.gg/feed",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": True},
    {"name": "Esports.gg", "url": "https://esports.gg/feed",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": True},
    {"name": "The Loadout", "url": "https://www.theloadout.com/feed",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": True},
]


# ============================================================
# Liquipedia per-wiki RSS (not used by bot.py, kept for reference)
# ============================================================
LIQUIPEDIA_WIKIS = [
    ("counterstrike", "cs2"),
    ("valorant", "valorant"),
    ("leagueoflegends", "lol"),
    ("dota2", "dota2"),
    ("rainbowsix", "r6"),
    ("rocketleague", "rl"),
    ("mobilelegends", "ml"),
    ("honorofkings", "hok"),
    ("pubgmobile", "pubgm"),
    ("apexlegends", "apex"),
    ("overwatch", "ow2"),
    ("fighters", "fgc"),
    ("easportsfc", "eafc"),
    ("callofduty", "cod"),
]


def liquipedia_rss_url(wiki: str, days: int = 1, limit: int = 50) -> str:
    return (
        f"https://liquipedia.net/{wiki}/api.php"
        f"?hidebots=1&days={days}&limit={limit}"
        f"&action=feedrecentchanges&feedformat=atom"
    )


LIQUIPEDIA_RSS_FEEDS = [
    {
        "name": f"Liquipedia {game.upper()} RC",
        "url": liquipedia_rss_url(wiki, days=1, limit=50),
        "game": game, "type": TYPE_LIQUIPEDIA, "verified": True, "wiki": wiki,
    }
    for wiki, game in LIQUIPEDIA_WIKIS
]


# ============================================================
# Reddit subreddits (not used by bot.py, kept for reference)
# ============================================================
REDDIT_MIN_UPVOTES = 200

REDDIT_SUBREDDITS = [
    ("GlobalOffensive", "cs2"),
    ("VALORANT", "valorant"),
    ("ValorantCompetitive", "valorant"),
    ("leagueoflegends", "lol"),
    ("DotA2", "dota2"),
    ("Rainbow6", "r6"),
    ("RocketLeagueEsports", "rl"),
    ("MobileLegendsGame", "ml"),
    ("StreetFighter", "fgc"),
    ("Tekken", "fgc"),
    ("apexlegends", "apex"),
    ("Competitiveoverwatch", "ow2"),
    ("EASportsFC", "eafc"),
    ("CompetitiveCoD", "cod"),
    ("esports", "multi"),
]


def reddit_rss_url(subreddit: str) -> str:
    return f"https://www.reddit.com/r/{subreddit}/.rss"


REDDIT_FEEDS = [
    {
        "name": f"r/{sub}", "url": reddit_rss_url(sub),
        "game": game, "type": TYPE_REDDIT,
        "min_upvotes": REDDIT_MIN_UPVOTES, "verified": True,
    }
    for sub, game in REDDIT_SUBREDDITS
]


# ============================================================
# Helpers + stats
# ============================================================
def all_feeds() -> list[dict]:
    return RSS_FEEDS + LIQUIPEDIA_RSS_FEEDS + REDDIT_FEEDS


def stats() -> dict:
    feeds = all_feeds()
    return {
        "total": len(feeds),
        "rss_primary": sum(1 for f in feeds if f["type"] == TYPE_PRIMARY),
        "rss_aggregator": sum(1 for f in feeds if f["type"] == TYPE_AGGREGATOR),
        "liquipedia_rss": sum(1 for f in feeds if f["type"] == TYPE_LIQUIPEDIA),
        "reddit": sum(1 for f in feeds if f["type"] == TYPE_REDDIT),
    }


# ============================================================
# Backward compatibility for bot.py v7
# Tier 1 = primary game-specific. Tier 2 = aggregators.
# ============================================================
def _tier_from_type(t: str) -> int:
    return 1 if t == TYPE_PRIMARY else 2


FEEDS = [
    {"name": f["name"], "url": f["url"], "tier": _tier_from_type(f["type"])}
    for f in RSS_FEEDS
]


if __name__ == "__main__":
    import json
    print(json.dumps(stats(), indent=2))
    print(f"\nFEEDS exposed to bot.py: {len(FEEDS)}")
    print(f"  Tier 1: {sum(1 for f in FEEDS if f['tier'] == 1)}")
    print(f"  Tier 2: {sum(1 for f in FEEDS if f['tier'] == 2)}")
