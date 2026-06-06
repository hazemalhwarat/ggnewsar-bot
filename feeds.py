# -*- coding: utf-8 -*-
"""
GGNewsAR - RSS Feeds Configuration
قائمة مصادر أخبار الرياضات الإلكترونية
"""

RSS_FEEDS = [
    # =========================
    # English General Esports
    # =========================
    {"name": "Dot Esports",          "url": "https://dotesports.com/feed",                          "category": "general"},
    {"name": "Dexerto Esports",      "url": "https://www.dexerto.com/feed/",                        "category": "general"},
    {"name": "ONE Esports",          "url": "https://www.oneesports.gg/feed/",                      "category": "general"},
    {"name": "Esports Insider",      "url": "https://esportsinsider.com/feed",                      "category": "industry"},
    {"name": "Esports.gg",           "url": "https://esports.gg/feed/",                             "category": "general"},
    {"name": "EarlyGame",            "url": "https://earlygame.com/feed",                           "category": "general"},
    {"name": "Esports Talk",         "url": "https://www.esportstalk.com/feed/",                    "category": "general"},
    {"name": "DBLTAP",               "url": "https://www.dbltap.com/posts.rss",                     "category": "general"},
    {"name": "GINX Esports TV",      "url": "https://www.ginx.tv/feed",                             "category": "general"},
    {"name": "Sheep Esports",        "url": "https://sheepesports.com/feed",                        "category": "general"},
    {"name": "Strafe",               "url": "https://www.strafe.com/feed/",                         "category": "general"},

    # =========================
    # Counter-Strike 2
    # =========================
    {"name": "HLTV News",            "url": "https://www.hltv.org/rss/news",                        "category": "cs2"},
    {"name": "Dust2.us",             "url": "https://dust2.us/rss",                                 "category": "cs2"},

    # =========================
    # Valorant
    # =========================
    {"name": "VLR.gg",               "url": "https://www.vlr.gg/rss",                               "category": "valorant"},

    # =========================
    # Dota 2 / StarCraft
    # =========================
    {"name": "TL.net",               "url": "https://tl.net/rss/news.xml",                          "category": "dota_sc"},

    # =========================
    # Game-specific (via Dot Esports)
    # =========================
    {"name": "Dot Esports LoL",      "url": "https://dotesports.com/league-of-legends/feed",        "category": "lol"},
    {"name": "Dot Esports R6",       "url": "https://dotesports.com/rainbow-6/feed",                "category": "r6"},
    {"name": "Dot Esports Fortnite", "url": "https://dotesports.com/fortnite/feed",                 "category": "fortnite"},
    {"name": "Dot Esports CoD",      "url": "https://dotesports.com/call-of-duty/feed",             "category": "cod"},
    {"name": "Dot Esports Apex",     "url": "https://dotesports.com/apex-legends/feed",             "category": "apex"},

    # =========================
    # Mobile Esports
    # =========================
    {"name": "AFK Gaming",                  "url": "https://afkgaming.com/feeds/esports",            "category": "mobile"},
    {"name": "ONE Esports MLBB",            "url": "https://www.oneesports.gg/mobile-legends/feed/", "category": "mlbb"},
    {"name": "ONE Esports PUBG Mobile",     "url": "https://www.oneesports.gg/pubg-mobile/feed/",    "category": "pubgm"},
    {"name": "ONE Esports Free Fire",       "url": "https://www.oneesports.gg/free-fire/feed/",      "category": "ff"},
    {"name": "Talkesport",                  "url": "https://www.talkesport.com/feed/",               "category": "mobile"},

    # =========================
    # Arabic Sources
    # =========================
    {"name": "True Gaming",          "url": "https://true-gaming.net/feed/",                        "category": "arabic"},
    {"name": "Arageek Gaming",       "url": "https://www.arageek.com/tech/gaming/feed",             "category": "arabic"},
    {"name": "Saudi Gamer",          "url": "https://www.saudigamer.com/feed/",                     "category": "arabic"},
]
