"""
GGNewsAR feeds catalog.

Each feed is a dict:
    {"name": "...", "url": "...", "tier": 1 or 2}

Tier 1 — esports dedicated sources. Items bypass the relevance filter.
Tier 2 — general or aggregated sources. Items must pass the relevance filter
         (must contain at least one ESPORTS_KEYWORDS match).

This is the clean baseline. Reddit, YouTube, tournament organizer blogs,
and expanded Google News queries are added in later phases.
"""

# Sources

FEEDS = [
    # ===== Tier 1: dedicated esports outlets =====

    {"name": "Dot Esports", "url": "https://dotesports.com/feed", "tier": 1},
    {"name": "Dexerto", "url": "https://www.dexerto.com/feed/", "tier": 1},
    {"name": "ESTNN", "url": "https://estnn.com/feed/", "tier": 1},
    {"name": "Esports.gg", "url": "https://escharts.com/news/rss", "tier": 1},
    {"name": "Esports.net", "url": "https://www.esports.net/news/feed/", "tier": 1},
    {"name": "Esports Insider", "url": "https://esportsinsider.com/feed", "tier": 1},
    {"name": "Esports News UK", "url": "https://esports-news.co.uk/feed/", "tier": 1},
    {"name": "ONE Esports", "url": "https://www.oneesports.gg/feed/", "tier": 1},
    {"name": "Sportskeeda Esports", "url": "https://www.sportskeeda.com/feed/esports", "tier": 1},
    {"name": "Hotspawn", "url": "https://www.hotspawn.com/feed", "tier": 1},
    {"name": "The Game Haus", "url": "https://thegamehaus.com/feed/", "tier": 1},
    {"name": "Run It Back", "url": "https://runitback.gg/feed/", "tier": 1},
    {"name": "Strafe Esports", "url": "https://strafe.com/feed/", "tier": 1},
    {"name": "Inven Global", "url": "https://www.invenglobal.com/rss", "tier": 1},
    {"name": "Esports Observer (TEO)", "url": "https://archive.esportsobserver.com/feed/", "tier": 1},

    # Game specific Tier 1

    {"name": "VLR.gg (Valorant)", "url": "https://vlr.gg/news.rss", "tier": 1},
    {"name": "Charlie Intel (CoD)", "url": "https://charlieintel.com/feed/", "tier": 1},
    {"name": "Dot Esports CS2", "url": "https://dotesports.com/counter-strike/feed", "tier": 1},
    {"name": "Dot Esports Valorant", "url": "https://dotesports.com/valorant/feed", "tier": 1},
    {"name": "Dot Esports Dota 2", "url": "https://dotesports.com/dota-2/feed", "tier": 1},
    {"name": "Dot Esports LoL", "url": "https://dotesports.com/league-of-legends/feed", "tier": 1},
    {"name": "Dot Esports Overwatch", "url": "https://dotesports.com/overwatch/feed", "tier": 1},
    {"name": "Dot Esports Rocket League", "url": "https://dotesports.com/rocket-league/feed", "tier": 1},
    {"name": "Dot Esports R6", "url": "https://dotesports.com/rainbow-6/feed", "tier": 1},
    {"name": "Dot Esports CoD", "url": "https://dotesports.com/call-of-duty/feed", "tier": 1},
    {"name": "Dot Esports Apex", "url": "https://dotesports.com/apex-legends/feed", "tier": 1},
    {"name": "Dot Esports Fortnite", "url": "https://dotesports.com/fortnite/feed", "tier": 1},
    {"name": "Dot Esports Mobile", "url": "https://dotesports.com/mobile/feed", "tier": 1},

    # ===== Tier 2: aggregators and general searches (must pass keyword filter) =====

    {"name": "Google News — Esports", "url": "https://news.google.com/rss/search?q=esports&hl=en-US&gl=US&ceid=US:en", "tier": 2},
    {"name": "Google News — Counter Strike", "url": "https://news.google.com/rss/search?q=%22Counter+Strike%22+OR+%22CS2%22+esports&hl=en-US&gl=US&ceid=US:en", "tier": 2},
    {"name": "Google News — Valorant", "url": "https://news.google.com/rss/search?q=Valorant+esports+OR+VCT&hl=en-US&gl=US&ceid=US:en", "tier": 2},
    {"name": "Google News — Dota 2", "url": "https://news.google.com/rss/search?q=%22Dota+2%22+esports&hl=en-US&gl=US&ceid=US:en", "tier": 2},
    {"name": "Google News — League of Legends", "url": "https://news.google.com/rss/search?q=%22League+of+Legends%22+esports+OR+LCK+OR+LEC+OR+LPL+OR+LCS&hl=en-US&gl=US&ceid=US:en", "tier": 2},
    {"name": "Google News — Rainbow Six", "url": "https://news.google.com/rss/search?q=%22Rainbow+Six%22+esports+OR+%22R6+Siege%22&hl=en-US&gl=US&ceid=US:en", "tier": 2},
    {"name": "Google News — Overwatch", "url": "https://news.google.com/rss/search?q=Overwatch+esports+OR+OWCS&hl=en-US&gl=US&ceid=US:en", "tier": 2},
    {"name": "Google News — Mobile Legends", "url": "https://news.google.com/rss/search?q=%22Mobile+Legends%22+MPL+OR+MLBB&hl=en-US&gl=US&ceid=US:en", "tier": 2},
    {"name": "Google News — PUBG Mobile", "url": "https://news.google.com/rss/search?q=%22PUBG+Mobile%22+esports+OR+PMSL&hl=en-US&gl=US&ceid=US:en", "tier": 2},
    {"name": "Google News — Fortnite", "url": "https://news.google.com/rss/search?q=Fortnite+FNCS+OR+%22Fortnite+Champion+Series%22&hl=en-US&gl=US&ceid=US:en", "tier": 2},
    {"name": "Google News — Esports World Cup", "url": "https://news.google.com/rss/search?q=%22Esports+World+Cup%22+OR+%22EWC%22+Riyadh&hl=en-US&gl=US&ceid=US:en", "tier": 2},
    {"name": "Google News — Team Falcons", "url": "https://news.google.com/rss/search?q=%22Team+Falcons%22+esports+-NFL+-Atlanta&hl=en-US&gl=US&ceid=US:en", "tier": 2},
    {"name": "Google News — Twisted Minds", "url": "https://news.google.com/rss/search?q=%22Twisted+Minds%22+esports&hl=en-US&gl=US&ceid=US:en", "tier": 2},
]


# Esports relevance whitelist

ESPORTS_KEYWORDS = [
    # Generic
    "esports", "e sports", "esport", "competitive gaming", "pro gaming",

    # Games and abbreviations
    "cs2", "cs:go", "csgo", "counter strike", "counter-strike",
    "valorant", "vct", "vlr", "vct masters", "vct champions",
    "dota", "dota 2", "dota2", "the international", "ti13", "ti14", "ti15",
    "league of legends", "lol esports", "lck", "lec", "lpl", "lcs",
    "worlds", "msi", "lcp", "ljl", "cblol",
    "overwatch", "owcs", "owl", "overwatch league", "overwatch champions",
    "rainbow six", "r6", "r6 siege", "siege esports", "eml", "blast r6",
    "rocket league", "rlcs", "rocket league championship",
    "apex legends", "als", "apex legends global", "alga",
    "call of duty", "cdl", "call of duty league", "warzone esports", "cod mobile",
    "fortnite", "fncs", "fortnite champion series",
    "pubg", "pubg mobile", "pmsl", "pgs", "pgc", "pubg global",
    "mobile legends", "mlbb", "mpl", "m6 world championship", "mpli", "msc",
    "free fire", "ffws", "ff world series", "ffml",
    "wild rift", "wrl", "wild rift league",
    "starcraft", "starcraft 2", "sc2", "gsl",
    "hearthstone", "hct", "hearthstone masters",
    "street fighter", "tekken", "mortal kombat", "guilty gear", "evo championship",
    "efootball", "eafc", "fc pro", "fifa esports",
    "marvel rivals esports", "marvel rivals championship",
    "honor of kings", "hok", "king pro league",
    "clash royale", "crl",
    "brawl stars", "bsc",

    # Scene terms
    "roster", "lineup change", "transfer window", "free agent",
    "igl", "in game leader", "awper", "duelist", "controller", "sentinel",
    "mid laner", "top laner", "jungler", "support player", "carry player",
    "offlaner", "soft support", "hard support",
    "lan event", "lan finals", "major tournament", "masters event",
    "grand finals", "open qualifier", "closed qualifier",
    "pro player", "tier 1 team", "tier 2 team",
    "shoutcaster", "esports caster", "esports analyst", "esports desk",
    "scrim", "bootcamp", "esports streamer",

    # Major orgs
    "team falcons", "twisted minds", "geekay esports", "nasr esports",
    "nigma galaxy", "g2 esports", "fnatic", "navi", "natus vincere",
    "team liquid", "cloud9", "evil geniuses", "t1 esports", "gen.g",
    "tsm", "faze clan", "sentinels esports", "paper rex", "drx",
    "edward gaming", "team vitality", "team spirit", "mouz",
    "astralis", "heroic", "psg talon", "lng esports", "jd gaming",
    "royal never give up", "invictus gaming", "bilibili gaming",
    "team secret", "og esports", "tundra esports", "gaimin gladiators",
    "aurora gaming", "team aurora", "team bds", "team heretics",
    "karmine corp", "movistar koi", "leviatan", "loud esports",
    "talon esports", "rare atom", "anyone's legend",

    # Saudi and MENA scene
    "saudi esports", "saudi esports federation", "sef",
    "esports world cup", "ewc", "gamers8", "gamers galaxy",
    "arabic league", "arab league of legends", "mpl mena",
    "jordan esports", "jef", "fate esports",

    # Tournament organizers
    "iem", "intel extreme masters", "esl pro league", "esl one",
    "blast premier", "blast bounty", "pgl major", "pgl cs",
    "dreamhack", "iesf", "asian games esports", "sea games esports",

    # Platforms commonly linked to esports
    "twitch streamer", "youtube gaming",
]


# Blacklist (kept short — the system primarily relies on the whitelist)
# These are explicit non-esports signals that often slip in via Google News.

BLACKLIST_KEYWORDS = [
    # American sports
    "nfl", "super bowl", "quarterback", "touchdown pass",
    "nba", "lakers", "celtics", "warriors basketball",
    "mlb", "major league baseball", "home run",
    "nhl", "stanley cup",

    # Soccer
    "premier league", "la liga", "serie a", "bundesliga", "ligue 1",
    "uefa champions league", "europa league", "fifa world cup 2026",
    "manchester united", "manchester city", "liverpool fc", "arsenal fc",
    "chelsea fc", "tottenham", "real madrid", "barcelona fc",
    "atletico madrid", "juventus", "inter milan", "ac milan",
    "bayern munich", "borussia dortmund",
    "atlanta falcons",

    # Motorsport
    "formula 1", "formula one", "f1 grand prix", "verstappen",
    "lewis hamilton", "charles leclerc", "nascar", "motogp",

    # Other traditional sports
    "wimbledon", "us open tennis", "roland garros", "australian open",
    "cricket world cup", "rugby world cup", "boxing match",
    "ufc fight night", "wwe", "wrestling raw",
]
