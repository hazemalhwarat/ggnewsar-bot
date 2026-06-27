"""
feeds.py — GGNewsAR bot v7 (rebuilt from scratch)
English only. Competitive esports + industry + streamers.

FEEDS structure: dict with name, url, tier.
  tier 1 = trusted pure esports source (low content noise; passes broadly)
  tier 2 = mixed / general / mainstream (must mention esports to pass)

All filtering logic lives in filters.py.
"""

FEEDS = [
    # ============================================================
    # TIER 1 — Trusted pure esports
    # ============================================================

    # General esports outlets
    {"name": "Dexerto Esports",   "url": "https://www.dexerto.com/esports/feed/",  "tier": 1},
    {"name": "Dot Esports",       "url": "https://dotesports.com/feed",            "tier": 1},
    {"name": "Esports Insider",   "url": "https://esportsinsider.com/feed",        "tier": 1},
    {"name": "The Esports Radar", "url": "https://esportsradar.gg/feed/",          "tier": 1},  # industry/business
    {"name": "ESTNN",             "url": "https://estnn.com/feed/",                "tier": 1},
    {"name": "Esports News UK",   "url": "https://esports-news.co.uk/feed/",       "tier": 1},
    {"name": "The Game Haus",     "url": "https://thegamehaus.com/feed/",          "tier": 1},
    {"name": "Esports.gg",        "url": "https://www.esports.gg/feed/",           "tier": 1},
    {"name": "Sheep Esports",     "url": "https://www.sheepesports.com/rss",       "tier": 1},  # leaks LoL/VAL/CS2/RL
    {"name": "GosuGamers",        "url": "https://www.gosugamers.net/articles/rss","tier": 1},
    {"name": "Escorenews",        "url": "https://escorenews.com/en/rss",          "tier": 1},  # leaks aggregator

    # Game specific (native RSS)
    {"name": "HLTV",              "url": "https://www.hltv.org/rss/news",          "tier": 1},  # CS2
    {"name": "Dotabuff",          "url": "https://www.dotabuff.com/blog.rss",      "tier": 1},  # Dota 2

    # Cloudflare protected -> bridged via Google News
    {"name": "ONE Esports",       "url": "https://news.google.com/rss/search?q=site:oneesports.gg+when:2d&hl=en-US&gl=US&ceid=US:en", "tier": 1},
    {"name": "Esports.net",       "url": "https://news.google.com/rss/search?q=site:esports.net+when:2d&hl=en-US&gl=US&ceid=US:en",   "tier": 1},
    {"name": "Jaxon",             "url": "https://news.google.com/rss/search?q=site:jaxon.gg+when:2d&hl=en-US&gl=US&ceid=US:en",       "tier": 1},
    {"name": "GGRecon",           "url": "https://news.google.com/rss/search?q=site:ggrecon.com+when:2d&hl=en-US&gl=US&ceid=US:en",   "tier": 1},
    {"name": "Inven Global",      "url": "https://news.google.com/rss/search?q=site:invenglobal.com+when:2d&hl=en-US&gl=US&ceid=US:en", "tier": 1},

    # Game specific without native RSS -> bridged via Google News
    {"name": "VLR.gg",            "url": "https://news.google.com/rss/search?q=site:vlr.gg+when:2d&hl=en-US&gl=US&ceid=US:en",        "tier": 1},  # VALORANT
    {"name": "SiegeGG",           "url": "https://news.google.com/rss/search?q=site:siege.gg+when:2d&hl=en-US&gl=US&ceid=US:en",      "tier": 1},  # R6
    {"name": "Octane.gg",         "url": "https://news.google.com/rss/search?q=site:octane.gg+when:2d&hl=en-US&gl=US&ceid=US:en",     "tier": 1},  # Rocket League
    {"name": "Pley.gg",           "url": "https://news.google.com/rss/search?q=site:pley.gg+when:2d&hl=en-US&gl=US&ceid=US:en",       "tier": 1},  # CS2 leaks
    {"name": "dust2.us",          "url": "https://news.google.com/rss/search?q=site:dust2.us+when:2d&hl=en-US&gl=US&ceid=US:en",      "tier": 1},  # CS2

    # X (Twitter) insider accounts -> bridged via Google News (catches articles citing them).
    # Native X RSS bridges are unstable, so we go through aggregators that re-report them.
    {"name": "Insider: OverdriveCS", "url": "https://news.google.com/rss/search?q=%22OverdriveCS%22+OR+%22OverDrive%22+CS2+esports+when:2d&hl=en-US&gl=US&ceid=US:en", "tier": 1},
    {"name": "Insider: KRL",         "url": "https://news.google.com/rss/search?q=%22KRL%22+CS2+leak+esports+when:2d&hl=en-US&gl=US&ceid=US:en",                       "tier": 1},
    {"name": "Insider: Harumi",      "url": "https://news.google.com/rss/search?q=%22Harumi%22+CS2+esports+when:2d&hl=en-US&gl=US&ceid=US:en",                         "tier": 1},
    {"name": "Insider: Wooloo",      "url": "https://news.google.com/rss/search?q=%22Wooloo%22+LoL+esports+when:2d&hl=en-US&gl=US&ceid=US:en",                          "tier": 1},

    # ============================================================
    # TIER 2 — Mixed / general (must mention esports to pass)
    # ============================================================

    # Gaming press (covers esports + games + reviews + guides)
    {"name": "PC Gamer",           "url": "https://www.pcgamer.com/rss/",                 "tier": 2},
    {"name": "Eurogamer",          "url": "https://www.eurogamer.net/feed",               "tier": 2},
    {"name": "VGC",                "url": "https://www.videogameschronicle.com/feed/",    "tier": 2},
    {"name": "GamesIndustry.biz",  "url": "https://www.gamesindustry.biz/feed",           "tier": 2},
    {"name": "Polygon",            "url": "https://www.polygon.com/rss/index.xml",        "tier": 2},
    {"name": "Kotaku",             "url": "https://kotaku.com/rss",                       "tier": 2},
    {"name": "IGN",                "url": "https://www.ign.com/rss/articles/feed",        "tier": 2},

    # Mainstream news (esports coverage)
    {"name": "Guardian Esports",   "url": "https://www.theguardian.com/games/esports/rss","tier": 2},
    {"name": "Guardian Games",     "url": "https://www.theguardian.com/games/rss",        "tier": 2},
    {"name": "BBC Esports",        "url": "https://news.google.com/rss/search?q=site:bbc.com+esports+when:2d&hl=en-US&gl=US&ceid=US:en", "tier": 2},
    {"name": "Reuters Esports",    "url": "https://news.google.com/rss/search?q=site:reuters.com+esports+when:2d&hl=en-US&gl=US&ceid=US:en", "tier": 2},
]
