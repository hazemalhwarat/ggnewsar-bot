"""
feeds.py — sources + keyword lists for GGNewsAR bot
English only.

Filtering model (v6, recall first):
  KEEP esports news broadly; only DROP what is clearly unwanted.
  An item is dropped if ANY of these is true:
    - it is pure game content (skins, patches, guides, cosmetics, lore...)  -> GAME_CONTENT
    - it is about a game that is NOT on your list                           -> EXCLUDED_TITLES
    - it is from a general / mainstream site and never mentions esports     -> tier 2 needs TITLE_SCOPE
    - it is traditional sports / entertainment with no esports word          -> BLACKLIST_KEYWORDS
    - it is a routine / live match score (handled in bot.py result filter)
  Everything else from an esports source passes, even short headlines.

FEEDS: dict with name, url, tier.
  tier 1 = trusted pure esports source -> kept unless it hits a drop rule above
  tier 2 = mixed / general / mainstream -> ALSO must mention an esports title/term
"""

FEEDS = [

    # ---------- TIER 1: trusted pure esports ----------
    {"name": "Dexerto Esports",  "url": "https://www.dexerto.com/esports/feed/",  "tier": 1},
    {"name": "Esports Insider",  "url": "https://esportsinsider.com/feed",         "tier": 1},
    {"name": "The Esports Radar","url": "https://esportsradar.gg/feed/",           "tier": 1},  # esports business
    {"name": "ESTNN",            "url": "https://estnn.com/feed/",                 "tier": 1},
    {"name": "Esports News UK",  "url": "https://esports-news.co.uk/feed/",        "tier": 1},
    {"name": "The Game Haus",    "url": "https://thegamehaus.com/feed/",           "tier": 1},
    {"name": "Esports.gg",       "url": "https://www.esports.gg/feed/",            "tier": 1},  # verify
    {"name": "HLTV",             "url": "https://www.hltv.org/rss/news",           "tier": 1},  # CS2 NEWS ONLY
    {"name": "Dotabuff",         "url": "https://www.dotabuff.com/blog.rss",       "tier": 1},  # Dota 2

    # Cloudflare protected -> bridged via Google News (bypasses the block)
    {"name": "ONE Esports",      "url": "https://news.google.com/rss/search?q=site:oneesports.gg+when:2d&hl=en-US&gl=US&ceid=US:en", "tier": 1},
    {"name": "Esports.net",      "url": "https://news.google.com/rss/search?q=site:esports.net+when:2d&hl=en-US&gl=US&ceid=US:en",   "tier": 1},
    {"name": "Jaxon",            "url": "https://news.google.com/rss/search?q=site:jaxon.gg+when:2d&hl=en-US&gl=US&ceid=US:en",       "tier": 1},
    {"name": "GGRecon",          "url": "https://news.google.com/rss/search?q=site:ggrecon.com+when:2d&hl=en-US&gl=US&ceid=US:en",   "tier": 1},
    {"name": "Inven Global",     "url": "https://news.google.com/rss/search?q=site:invenglobal.com+when:2d&hl=en-US&gl=US&ceid=US:en", "tier": 1},

    # ---------- TIER 2: mixed / general (must mention esports) ----------
    {"name": "Dot Esports",       "url": "https://dotesports.com/feed",                  "tier": 2},  # covers many non esports games + guides
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
    {"name": "The Guardian Esports", "url": "https://www.theguardian.com/games/esports/rss", "tier": 2},
    {"name": "The Guardian Games",   "url": "https://www.theguardian.com/games/rss",         "tier": 2},
]


# ----------------------------------------------------------------------------
# TITLE_SCOPE — positive esports markers.
# Used as the tier 2 gate (general sites must mention one of these) and as an
# override for the excluded titles guard.
# ----------------------------------------------------------------------------
TITLE_SCOPE = [
    # esports umbrella
    "esports", "esport", "e-sports", "e-sport",
    # titles
    "counter-strike", "cs2", "csgo",
    "valorant", "vct", "champions tour", "valorant champions",
    "league of legends", "lol esports", "worlds", "msi",
    "lck", "lec", "lpl", "lcs",
    "dota 2", "dota2", "the international",
    "rocket league", "rlcs",
    "rainbow six", "siege", "r6", "six invitational",
    "mobile legends", "mlbb", "mpl",
    "pubg mobile", "pmsl", "pmwc", "pmgc",
    "honor of kings", "kic", "king pro league",
    "call of duty league", "cdl",
    "overwatch", "owcs",
    "apex legends", "algs",
    "tekken", "street fighter", "fighting game", "evo",
    "chess",
    # multi game events
    "ewc", "esports world cup", "esports nations cup", "asian games",
    "iem", "esl pro league", "esl", "blast", "pgl",
    # distinctive orgs (help short headlines)
    "navi", "faze", "fnatic", "astralis", "team falcons", "falcons esports",
    "team liquid", "team spirit", "team vitality", "sentinels", "gen.g",
    "the mongolz", "furia", "g2 esports", "twisted minds", "geekay",
    "cloud9", "evil geniuses", "karmine corp", "paper rex", "t1 esports",
]


# ----------------------------------------------------------------------------
# GAME_CONTENT — pure game content to DROP (not esports news).
# Kept specific to avoid colliding with real news words like "update" or "season".
# ----------------------------------------------------------------------------
GAME_CONTENT = [
    "skin", "skins", "cosmetic", "cosmetics", "bundle", "battle pass", "battlepass",
    "patch notes", "patch update", "hotfix", "buff", "buffs", "nerf", "nerfs",
    "balance changes", "tier list", "best settings", "best loadout", "loadout",
    "guide", "how to", "walkthrough", "tips and tricks", "beginner",
    "lore", "story mode", "campaign", "release date", "launch date",
    "trailer", "gameplay reveal", "datamine", "datamined",
    "new agent", "new operator", "new hero", "new champion", "new legend",
    "new map", "new mode", "new weapon", "new character", "new skin",
    "dlc", "expansion pack", "early access", "crossover skin", "collab skin",
    "redeem code", "redeem codes", "free rewards", "promo code",
]


# ----------------------------------------------------------------------------
# EXCLUDED_TITLES — games NOT on your list. Dropped unless a listed title also
# appears in the same item.
# ----------------------------------------------------------------------------
EXCLUDED_TITLES = [
    "fortnite", "marvel rivals", "ea fc", "ea sports fc", "fifa",
    "hearthstone", "smash bros", "super smash", "brawl stars",
    "clash royale", "clash of clans", "free fire", "teamfight tactics",
    "deadlock", "world of warcraft", "genshin", "roblox", "minecraft",
    "pokemon", "pokémon", "wuthering waves", "marvel snap",
]


# ----------------------------------------------------------------------------
# BLACKLIST_KEYWORDS — traditional sports / entertainment.
# Only blocks when there is NO explicit esports word present.
# ----------------------------------------------------------------------------
BLACKLIST_KEYWORDS = [
    "nfl", "nba", "mlb", "nhl",
    "premier league", "la liga", "serie a", "bundesliga", "ligue 1",
    "formula 1", "f1 grand prix", "ufc", "wwe", "boxing",
    "golf", "tennis", "nascar", "transfer deadline day",
    "netflix", "tiktok", "kardashian", "box office", "movie review",
]
