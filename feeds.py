"""
GGNewsAR Bot — Feed Configuration (Comprehensive)
All news sources organized by type and game.

Structure:
- RSS_FEEDS: standard RSS endpoints (Tier 1 + Tier 2 + Arabic)
- LIQUIPEDIA_RSS_FEEDS: per-wiki Recent Changes feeds
- REDDIT_FEEDS: subreddit RSS with upvote filter
- SCRAPE_TARGETS: HTML scraping (see scrape_targets.py)

Note: All sources are English/international. Arab teams are TRACKED as subjects
of news (via Liquipedia Watcher and scrape_targets.py) but no Arabic news
sources are aggregated. GGNewsAR produces its own Arabic content from these
international sources.

Game codes:
  cs2, valorant, lol, dota2, r6, rl, ml, hok, pubgm,
  apex, ow2, fgc, eafc, cod, multi
"""

# Source type constants
TYPE_PRIMARY = "rss_primary"
TYPE_AGGREGATOR = "rss_aggregator"
TYPE_LIQUIPEDIA = "liquipedia_rss"
TYPE_REDDIT = "reddit"
TYPE_SCRAPE = "scrape"


# ============================================================
# Tier 1: Game-specific primary sites
# ============================================================

RSS_FEEDS = [
    # ============ Counter Strike 2 ============
    {"name": "HLTV", "url": "https://www.hltv.org/rss/news",
     "game": "cs2", "type": TYPE_PRIMARY, "verified": True},
    {"name": "Dot Esports CS", "url": "https://dotesports.com/counter-strike/feed",
     "game": "cs2", "type": TYPE_PRIMARY, "verified": True},
    {"name": "Escorenews CS2", "url": "https://escorenews.com/en/cs2/rss",
     "game": "cs2", "type": TYPE_PRIMARY, "verified": False},

    # ============ VALORANT ============
    {"name": "VLR.gg", "url": "https://vlr.gg/rss",
     "game": "valorant", "type": TYPE_PRIMARY, "verified": True},
    {"name": "Dot Esports VALORANT", "url": "https://dotesports.com/valorant/feed",
     "game": "valorant", "type": TYPE_PRIMARY, "verified": True},
    {"name": "Esports.net VALORANT", "url": "https://www.esports.net/news/valorant/feed",
     "game": "valorant", "type": TYPE_PRIMARY, "verified": False},

    # ============ League of Legends ============
    {"name": "Dot Esports LoL", "url": "https://dotesports.com/league-of-legends/feed",
     "game": "lol", "type": TYPE_PRIMARY, "verified": True},
    {"name": "Inven Global", "url": "https://www.invenglobal.com/feed",
     "game": "lol", "type": TYPE_PRIMARY, "verified": False},

    # ============ Dota 2 ============
    {"name": "Dot Esports Dota 2", "url": "https://dotesports.com/dota-2/feed",
     "game": "dota2", "type": TYPE_PRIMARY, "verified": True},
    {"name": "ONE Esports Dota 2", "url": "https://oneesports.gg/dota2/feed",
     "game": "dota2", "type": TYPE_PRIMARY, "verified": False},
    {"name": "Dotabuff Blog", "url": "https://www.dotabuff.com/blog.rss",
     "game": "dota2", "type": TYPE_PRIMARY, "verified": True},

    # ============ Rainbow Six Siege ============
    {"name": "Dot Esports R6", "url": "https://dotesports.com/rainbow-six/feed",
     "game": "r6", "type": TYPE_PRIMARY, "verified": False},

    # ============ Rocket League ============
    {"name": "Dot Esports RL", "url": "https://dotesports.com/rocket-league/feed",
     "game": "rl", "type": TYPE_PRIMARY, "verified": False},

    # ============ Mobile Legends ============
    {"name": "ONE Esports MLBB", "url": "https://oneesports.gg/mlbb/feed",
     "game": "ml", "type": TYPE_PRIMARY, "verified": False},
    {"name": "Dot Esports MLBB", "url": "https://dotesports.com/mobile-legends/feed",
     "game": "ml", "type": TYPE_PRIMARY, "verified": False},

    # ============ PUBG Mobile ============
    {"name": "Dot Esports PUBGM", "url": "https://dotesports.com/pubg-mobile/feed",
     "game": "pubgm", "type": TYPE_PRIMARY, "verified": False},

    # ============ Apex Legends ============
    {"name": "Dot Esports Apex", "url": "https://dotesports.com/apex/feed",
     "game": "apex", "type": TYPE_PRIMARY, "verified": False},

    # ============ Overwatch 2 ============
    {"name": "Dot Esports Overwatch", "url": "https://dotesports.com/overwatch/feed",
     "game": "ow2", "type": TYPE_PRIMARY, "verified": False},

    # ============ Fighting Games ============
    {"name": "EventHubs", "url": "https://www.eventhubs.com/feed/",
     "game": "fgc", "type": TYPE_PRIMARY, "verified": True},
    {"name": "Dot Esports FGC", "url": "https://dotesports.com/fgc/feed",
     "game": "fgc", "type": TYPE_PRIMARY, "verified": False},

    # ============ EA FC ============
    {"name": "Dot Esports FIFA", "url": "https://dotesports.com/fifa/feed",
     "game": "eafc", "type": TYPE_PRIMARY, "verified": False},

    # ============ Call of Duty ============
    {"name": "Dot Esports CoD", "url": "https://dotesports.com/call-of-duty/feed",
     "game": "cod", "type": TYPE_PRIMARY, "verified": False},

    # ============================================================
    # Tier 2: Multi-game aggregators
    # ============================================================
    {"name": "Dot Esports General", "url": "https://dotesports.com/feed",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": True},
    {"name": "Esports Insider", "url": "https://esportsinsider.com/feed",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": True},
    {"name": "ESTNN", "url": "https://estnn.com/feed",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": True},
    {"name": "Esports News UK", "url": "https://esports-news.co.uk/feed",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": False},
    {"name": "Insider Gaming", "url": "https://insider-gaming.com/feed",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": False},
    {"name": "Sheep Esports", "url": "https://www.sheepesports.com/rss",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": False,
     "notes": "Strong for LoL, VALORANT, CS2, RL leaks and breaking news"},
    {"name": "The Esports Radar", "url": "https://esportsradar.gg/feed",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": False},
    {"name": "Esports.gg", "url": "https://esports.gg/feed",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": False},
    {"name": "Esports.net News", "url": "https://www.esports.net/news/feed",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": False},
    {"name": "Escorenews", "url": "https://escorenews.com/en/rss",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": False},
    {"name": "ONE Esports General", "url": "https://www.oneesports.gg/feed",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": False},
    {"name": "The Loadout", "url": "https://www.theloadout.com/feed",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": False},
    {"name": "GGRecon", "url": "https://www.ggrecon.com/rss",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": False},
    {"name": "Esports Maven", "url": "https://www.esportsmaven.io/feed",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": False},
    {"name": "Strafe News", "url": "https://www.strafe.com/news/feed",
     "game": "multi", "type": TYPE_AGGREGATOR, "verified": False,
     "notes": "Covers CS2, LoL, VALORANT, Dota 2, OW, CoD, RL, R6. Strong news + leaks."},
]


# ============================================================
# Tier 3: Liquipedia per-wiki RSS (Recent Changes)
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
        "game": game,
        "type": TYPE_LIQUIPEDIA,
        "verified": True,
        "wiki": wiki,
    }
    for wiki, game in LIQUIPEDIA_WIKIS
]


# ============================================================
# Tier 5: Reddit subreddits
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
        "name": f"r/{sub}",
        "url": reddit_rss_url(sub),
        "game": game,
        "type": TYPE_REDDIT,
        "min_upvotes": REDDIT_MIN_UPVOTES,
        "verified": True,
    }
    for sub, game in REDDIT_SUBREDDITS
]


# ============================================================
# Helpers
# ============================================================

def all_feeds() -> list[dict]:
    return RSS_FEEDS + LIQUIPEDIA_RSS_FEEDS + REDDIT_FEEDS


def feeds_by_game(game: str) -> list[dict]:
    return [f for f in all_feeds() if f.get("game") == game or f.get("game") == "multi"]


def feeds_by_type(type_str: str) -> list[dict]:
    return [f for f in all_feeds() if f.get("type") == type_str]


def stats() -> dict:
    feeds = all_feeds()
    return {
        "total": len(feeds),
        "rss_primary": sum(1 for f in feeds if f["type"] == TYPE_PRIMARY),
        "rss_aggregator": sum(1 for f in feeds if f["type"] == TYPE_AGGREGATOR),
        "liquipedia_rss": sum(1 for f in feeds if f["type"] == TYPE_LIQUIPEDIA),
        "reddit": sum(1 for f in feeds if f["type"] == TYPE_REDDIT),
        "verified": sum(1 for f in feeds if f.get("verified")),
        "unverified": sum(1 for f in feeds if not f.get("verified")),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(stats(), indent=2))
