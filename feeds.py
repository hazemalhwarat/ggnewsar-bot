"""
feeds.py — sources + keyword lists for GGNewsAR bot
English only.

FEEDS: each item is a dict with name, url, tier.
  tier 1 = dedicated esports outlets  -> pulled in full
  tier 2 = general gaming + mainstream -> must mention esports to pass

Lines marked "verify" should be confirmed on the first run (any source that
shows DEAD in the Actions log can simply be deleted from this list).
Lines marked "needs bridge" have no native RSS; generate one with RSSHub or
rss.app and paste the generated url in.
"""

FEEDS = [

    # ---------- TIER 1: dedicated esports (multi game) ----------
    {"name": "Dexerto Esports",  "url": "https://www.dexerto.com/esports/feed/", "tier": 1},
    {"name": "Dot Esports",      "url": "https://dotesports.com/feed",            "tier": 1},
    {"name": "Esports Insider",  "url": "https://esportsinsider.com/feed",        "tier": 1},
    {"name": "Esports.net",      "url": "https://www.esports.net/news/feed/",     "tier": 1},
    {"name": "ESTNN",            "url": "https://estnn.com/feed/",                "tier": 1},
    {"name": "Jaxon",            "url": "https://jaxon.gg/feed/",                 "tier": 1},
    {"name": "ONE Esports",      "url": "https://www.oneesports.gg/feed/",        "tier": 1},
    {"name": "Esports News UK",  "url": "https://esports-news.co.uk/feed/",       "tier": 1},
    {"name": "GGRecon",          "url": "https://www.ggrecon.com/feed/",          "tier": 1},  # verify
    {"name": "The Game Haus",    "url": "https://thegamehaus.com/feed/",          "tier": 1},
    {"name": "Esports.gg",       "url": "https://www.esports.gg/feed/",           "tier": 1},  # verify
    {"name": "Inven Global",     "url": "https://www.invenglobal.com/rss",        "tier": 1},  # verify

    # ---------- TIER 1: dedicated esports (game specific) ----------
    {"name": "HLTV",             "url": "https://www.hltv.org/rss/news",          "tier": 1},  # CS2 NEWS ONLY
    {"name": "Dotabuff",         "url": "https://www.dotabuff.com/blog.rss",      "tier": 1},  # Dota 2
    # VALORANT (vlr.gg): no native RSS -> needs bridge, e.g.
    # {"name": "VLR",  "url": "https://rsshub.app/vlr/news", "tier": 1},
    # Rainbow Six (siege.gg): no native RSS -> needs bridge (rss.app)
    # Rocket League (octane.gg): stats only -> rely on Dexerto / Dot Esports
    # Liquipedia / Leaguepedia: no usable RSS -> keep the screenshot workflow

    # ---------- TIER 2: general gaming (keyword filtered) ----------
    {"name": "PC Gamer",          "url": "https://www.pcgamer.com/rss/",                 "tier": 2},
    {"name": "Eurogamer",         "url": "https://www.eurogamer.net/feed",               "tier": 2},
    {"name": "VGC",               "url": "https://www.videogameschronicle.com/feed/",    "tier": 2},
    {"name": "GamesIndustry.biz", "url": "https://www.gamesindustry.biz/feed",           "tier": 2},
    {"name": "Polygon",           "url": "https://www.polygon.com/rss/index.xml",        "tier": 2},
    {"name": "Kotaku",            "url": "https://kotaku.com/rss",                        "tier": 2},
    {"name": "The Verge Games",   "url": "https://www.theverge.com/games/rss/index.xml", "tier": 2},
    {"name": "Rock Paper Shotgun","url": "https://www.rockpapershotgun.com/feed",        "tier": 2},
    {"name": "GamesRadar",        "url": "https://www.gamesradar.com/rss/",              "tier": 2},
    {"name": "TheGamer",          "url": "https://www.thegamer.com/feed/",               "tier": 2},
    {"name": "Game Rant",         "url": "https://gamerant.com/feed/",                   "tier": 2},
    {"name": "IGN",               "url": "https://www.ign.com/rss/articles/feed",        "tier": 2},  # verify

    # ---------- TIER 2: mainstream / global news (keyword filtered) ----------
    {"name": "The Guardian Esports", "url": "https://www.theguardian.com/games/esports/rss", "tier": 2},
    {"name": "The Guardian Games",   "url": "https://www.theguardian.com/games/rss",         "tier": 2},
    {"name": "Forbes Games",         "url": "https://www.forbes.com/games/feed/",            "tier": 2},  # verify
]


# Whitelist: an item must contain at least one of these to count as esports
# (matched as a whole word, case insensitive, by bot.py).
ESPORTS_KEYWORDS = [
    "esports", "esport", "e-sports", "e-sport",
    "pro player", "roster", "lineup", "line-up", "benched",
    "tournament", "qualifier", "playoffs", "grand final", "prize pool",
    "lan", "world championship", "major",
    "vct", "valorant", "champions tour",
    "lck", "lec", "lpl", "lcs", "worlds", "msi",
    "iem", "esl", "blast", "pgl",
    "rlcs", "rocket league",
    "cdl", "call of duty league",
    "owl", "overwatch",
    "ewc", "esports world cup",
    "the international", "dota",
    "counter-strike", "cs2", "csgo",
    "league of legends",
    "rainbow six", "siege",
    "mobile legends", "mlbb",
    "pubg mobile", "honor of kings",
    "apex legends", "starcraft",
    "evo", "tekken", "street fighter",
    "asian games", "esports nations cup",
]


# Blacklist: trims off topic items from mixed Tier 1 sites (traditional sports
# and pure entertainment). Whitelist always wins, so an esports item is never
# blocked by these.
BLACKLIST_KEYWORDS = [
    "nfl", "nba", "mlb", "nhl",
    "premier league", "la liga", "serie a", "bundesliga", "ligue 1",
    "formula 1", "f1 grand prix", "ufc", "wwe", "boxing",
    "golf", "tennis", "nascar", "transfer deadline day",
    "netflix", "tiktok", "kardashian", "box office", "movie review",
]
