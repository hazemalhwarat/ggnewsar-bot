"""
feeds.py — sources + keyword lists for GGNewsAR bot
English only. Competitive esports scene only.

FEEDS: each item is a dict with name, url, tier.
  tier 1 = dedicated esports outlets
  tier 2 = general gaming + mainstream
Both tiers are filtered the same strict way now (scope AND context).
Tier only softens the traditional-sports guard for trusted esports outlets.

An item is kept only if it satisfies BOTH:
  1) TITLE_SCOPE   -> it is about one of your titles, circuits, orgs, or the esports scene
  2) CONTEXT_SIGNALS -> it is about the COMPETITIVE scene (tournament, roster,
                        transfer, title...), not game content (skins, patches, guides)

Lines marked "verify" should be confirmed on the first run.
Lines marked "needs bridge" have no native RSS; generate one with RSSHub or rss.app.
"""

FEEDS = [

    # ---------- TIER 1: dedicated esports (multi game) ----------
    {"name": "Dexerto Esports",  "url": "https://www.dexerto.com/esports/feed/", "tier": 1},
    {"name": "Dot Esports",      "url": "https://dotesports.com/feed",            "tier": 1},
    {"name": "Esports Insider",  "url": "https://esportsinsider.com/feed",        "tier": 1},
    {"name": "Esports.net",      "url": "https://news.google.com/rss/search?q=site:esports.net+when:2d&hl=en-US&gl=US&ceid=US:en",   "tier": 1},  # Cloudflare, bridged via Google News
    {"name": "ESTNN",            "url": "https://estnn.com/feed/",                "tier": 1},
    {"name": "Jaxon",            "url": "https://news.google.com/rss/search?q=site:jaxon.gg+when:2d&hl=en-US&gl=US&ceid=US:en",       "tier": 1},  # Cloudflare, bridged via Google News
    {"name": "ONE Esports",      "url": "https://news.google.com/rss/search?q=site:oneesports.gg+when:2d&hl=en-US&gl=US&ceid=US:en", "tier": 1},  # Cloudflare, bridged via Google News
    {"name": "Esports News UK",  "url": "https://esports-news.co.uk/feed/",       "tier": 1},
    {"name": "GGRecon",          "url": "https://news.google.com/rss/search?q=site:ggrecon.com+when:2d&hl=en-US&gl=US&ceid=US:en",   "tier": 1},  # Cloudflare, bridged via Google News
    {"name": "The Game Haus",    "url": "https://thegamehaus.com/feed/",          "tier": 1},
    {"name": "Esports.gg",       "url": "https://www.esports.gg/feed/",           "tier": 1},  # verify
    {"name": "Inven Global",     "url": "https://news.google.com/rss/search?q=site:invenglobal.com+when:2d&hl=en-US&gl=US&ceid=US:en", "tier": 1},  # Cloudflare, bridged via Google News

    # ---------- TIER 1: dedicated esports (game specific) ----------
    {"name": "HLTV",             "url": "https://www.hltv.org/rss/news",          "tier": 1},  # CS2 NEWS ONLY
    {"name": "Dotabuff",         "url": "https://www.dotabuff.com/blog.rss",      "tier": 1},  # Dota 2
    # VALORANT (vlr.gg): no native RSS -> needs bridge, e.g.
    # {"name": "VLR",  "url": "https://rsshub.app/vlr/news", "tier": 1},
    # Rainbow Six (siege.gg): no native RSS -> needs bridge (rss.app)
    # Rocket League (octane.gg): stats only -> rely on Dexerto / Dot Esports
    # Liquipedia / Leaguepedia: no usable RSS -> keep the screenshot workflow

    # ---------- TIER 2: general gaming (strict filter) ----------
    {"name": "PC Gamer",          "url": "https://www.pcgamer.com/rss/",                 "tier": 2},
    {"name": "Eurogamer",         "url": "https://www.eurogamer.net/feed",               "tier": 2},
    {"name": "VGC",               "url": "https://www.videogameschronicle.com/feed/",    "tier": 2},
    {"name": "GamesIndustry.biz", "url": "https://www.gamesindustry.biz/feed",           "tier": 2},
    {"name": "Polygon",           "url": "https://www.polygon.com/rss/index.xml",        "tier": 2},
    {"name": "Kotaku",            "url": "https://kotaku.com/rss",                        "tier": 2},
    {"name": "The Verge",         "url": "https://www.theverge.com/rss/index.xml",       "tier": 2},
    {"name": "Rock Paper Shotgun","url": "https://www.rockpapershotgun.com/feed",        "tier": 2},
    {"name": "GamesRadar",        "url": "https://www.gamesradar.com/rss/",              "tier": 2},
    {"name": "TheGamer",          "url": "https://www.thegamer.com/feed/",               "tier": 2},
    {"name": "Game Rant",         "url": "https://gamerant.com/feed/",                   "tier": 2},
    {"name": "IGN",               "url": "https://www.ign.com/rss/articles/feed",        "tier": 2},  # verify

    # ---------- TIER 2: mainstream / global news (strict filter) ----------
    {"name": "The Guardian Esports", "url": "https://www.theguardian.com/games/esports/rss", "tier": 2},
    {"name": "The Guardian Games",   "url": "https://www.theguardian.com/games/rss",         "tier": 2},
]


# ----------------------------------------------------------------------------
# GATE 1 — TITLE_SCOPE
# The item must mention one of your titles, a circuit, a known org, or the
# esports scene. A non listed game (Fortnite, EA FC, Elden Ring...) is ignored.
# ----------------------------------------------------------------------------
TITLE_SCOPE = [
    # esports umbrella
    "esports", "esport", "e-sports", "e-sport",
    # Counter-Strike
    "counter-strike", "cs2", "csgo",
    # VALORANT
    "valorant", "vct", "champions tour", "valorant champions",
    # League of Legends
    "league of legends", "lol esports", "worlds", "msi",
    "lck", "lec", "lpl", "lcs", "lck cup",
    # Dota 2
    "dota 2", "dota2", "the international",
    # Rocket League
    "rocket league", "rlcs",
    # Rainbow Six
    "rainbow six", "siege", "r6", "six invitational",
    # Mobile Legends
    "mobile legends", "mlbb", "mpl", "m6", "m7",
    # PUBG Mobile
    "pubg mobile", "pmsl", "pmwc", "pmgc",
    # Honor of Kings
    "honor of kings", "kic", "king pro league",
    # Call of Duty
    "call of duty league", "cdl",
    # Overwatch
    "overwatch", "owcs", "overwatch champions",
    # Apex
    "apex legends", "algs",
    # Fighting games
    "tekken", "street fighter", "fighting game", "evo ",
    # Chess
    "chess",
    # multi game events you cover
    "ewc", "esports world cup", "esports nations cup", "asian games",
    "iem", "esl pro league", "blast", "pgl",
    # distinctive orgs (help catch terse transfer headlines)
    "navi", "faze", "fnatic", "astralis", "team falcons", "team liquid",
    "team spirit", "team vitality", "sentinels", "gen.g", "the mongolz",
    "furia", "g2 esports", "twisted minds", "geekay",
]


# ----------------------------------------------------------------------------
# GATE 2 — CONTEXT_SIGNALS
# The item must be about the COMPETITIVE scene, not game content.
# A bare game title with no competitive word will NOT pass.
# ----------------------------------------------------------------------------
CONTEXT_SIGNALS = [
    # events / stages
    "tournament", "qualifier", "qualify", "qualifies", "qualified",
    "playoffs", "grand final", "final", "finals", "semifinal", "semi-final",
    "bracket", "championship", "champions", "champion", "title", "trophy",
    "crowned", "winner", "wins", "prize pool", "lan", "major",
    # roster / personnel
    "roster", "lineup", "line-up", "signs", "signing", "sign",
    "transfer", "benched", "stand-in", "free agent",
    "joins", "joined", "leaves", "departs", "departure",
    "retires", "retirement", "acquire", "acquires",
    "pro player", "head coach", "coach", "igl",
    # circuits double as context
    "vct", "iem", "esl", "blast", "pgl", "rlcs", "cdl", "algs", "mpl",
    "ewc", "esports world cup", "esports nations cup", "the international",
    "worlds", "msi", "owcs", "six invitational",
]


# ----------------------------------------------------------------------------
# Guard — traditional sports / pure entertainment.
# Only blocks when there is NO explicit esports word present.
# ----------------------------------------------------------------------------
BLACKLIST_KEYWORDS = [
    "nfl", "nba", "mlb", "nhl",
    "premier league", "la liga", "serie a", "bundesliga", "ligue 1",
    "formula 1", "f1 grand prix", "ufc", "wwe", "boxing",
    "golf", "tennis", "nascar", "transfer deadline day",
    "netflix", "tiktok", "kardashian", "box office", "movie review",
]
