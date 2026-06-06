# -*- coding: utf-8 -*-
"""
GGNewsAR - RSS Feeds Configuration
قائمة موسّعة لمصادر أخبار الرياضات الإلكترونية بالإنجليزية فقط
"""

RSS_FEEDS = [
    # ===============================================
    # ENGLISH GENERAL ESPORTS (موسّع)
    # ===============================================
    {"name": "Dot Esports",          "url": "https://dotesports.com/feed",                          "category": "general"},
    {"name": "Dexerto Esports",      "url": "https://www.dexerto.com/feed/",                        "category": "general"},
    {"name": "ONE Esports",          "url": "https://www.oneesports.gg/feed/",                      "category": "general"},
    {"name": "Esports Insider",      "url": "https://esportsinsider.com/feed",                      "category": "industry"},
    {"name": "Esports.gg",           "url": "https://esports.gg/feed/",                             "category": "general"},
    {"name": "Esports.com",          "url": "https://www.esports.com/en/feed",                      "category": "general"},
    {"name": "EarlyGame",            "url": "https://earlygame.com/feed",                           "category": "general"},
    {"name": "Esports Talk",         "url": "https://www.esportstalk.com/feed/",                    "category": "general"},
    {"name": "DBLTAP",               "url": "https://www.dbltap.com/posts.rss",                     "category": "general"},
    {"name": "GINX Esports TV",      "url": "https://www.ginx.tv/feed",                             "category": "general"},
    {"name": "Sheep Esports",        "url": "https://sheepesports.com/feed",                        "category": "general"},
    {"name": "Strafe",               "url": "https://www.strafe.com/feed/",                         "category": "general"},
    {"name": "Esports News UK",      "url": "https://esports-news.co.uk/feed/",                     "category": "general"},
    {"name": "The Esports Advocate", "url": "https://www.theesportsadvocate.com/feed/",             "category": "general"},
    {"name": "Esports Bureau",       "url": "https://esportsbureau.com/feed/",                      "category": "general"},
    {"name": "The Loadout",          "url": "https://www.theloadout.com/feed",                      "category": "general"},
    {"name": "SBJ Esports",          "url": "https://www.sportsbusinessjournal.com/RSS/esports",    "category": "industry"},
    {"name": "Run It Back",          "url": "https://runitback.gg/feed/",                           "category": "general"},

    # ===============================================
    # COUNTER-STRIKE 2 / CS
    # ===============================================
    {"name": "HLTV News",            "url": "https://www.hltv.org/rss/news",                        "category": "cs2"},
    {"name": "HLTV Results",         "url": "https://www.hltv.org/rss/results",                     "category": "cs2"},
    {"name": "Dust2.us",             "url": "https://dust2.us/rss",                                 "category": "cs2"},
    {"name": "Dot Esports CS",       "url": "https://dotesports.com/counter-strike/feed",           "category": "cs2"},
    {"name": "Dexerto CS",           "url": "https://www.dexerto.com/cs2/feed/",                    "category": "cs2"},

    # ===============================================
    # VALORANT
    # ===============================================
    {"name": "VLR.gg",               "url": "https://www.vlr.gg/rss",                               "category": "valorant"},
    {"name": "Dot Esports Valorant", "url": "https://dotesports.com/valorant/feed",                 "category": "valorant"},
    {"name": "Dexerto Valorant",     "url": "https://www.dexerto.com/valorant/feed/",               "category": "valorant"},
    {"name": "ONE Esports Valorant", "url": "https://www.oneesports.gg/valorant/feed/",             "category": "valorant"},

    # ===============================================
    # DOTA 2 / STARCRAFT
    # ===============================================
    {"name": "TL.net",               "url": "https://tl.net/rss/news.xml",                          "category": "dota_sc"},
    {"name": "Dot Esports Dota 2",   "url": "https://dotesports.com/dota-2/feed",                   "category": "dota_sc"},
    {"name": "Dexerto Dota 2",       "url": "https://www.dexerto.com/dota2/feed/",                  "category": "dota_sc"},
    {"name": "ONE Esports Dota 2",   "url": "https://www.oneesports.gg/dota2/feed/",                "category": "dota_sc"},

    # ===============================================
    # LEAGUE OF LEGENDS
    # ===============================================
    {"name": "Dot Esports LoL",      "url": "https://dotesports.com/league-of-legends/feed",        "category": "lol"},
    {"name": "Dexerto LoL",          "url": "https://www.dexerto.com/league-of-legends/feed/",      "category": "lol"},
    {"name": "ONE Esports LoL",      "url": "https://www.oneesports.gg/league-of-legends/feed/",    "category": "lol"},

    # ===============================================
    # RAINBOW SIX SIEGE
    # ===============================================
    {"name": "SiegeGG",              "url": "https://siege.gg/feed",                                "category": "r6"},
    {"name": "Dot Esports R6",       "url": "https://dotesports.com/rainbow-6/feed",                "category": "r6"},
    {"name": "Dexerto R6",           "url": "https://www.dexerto.com/rainbow-six/feed/",            "category": "r6"},

    # ===============================================
    # FORTNITE
    # ===============================================
    {"name": "Fortnite Tracker",     "url": "https://fortnitetracker.com/feed",                     "category": "fortnite"},
    {"name": "Dot Esports Fortnite", "url": "https://dotesports.com/fortnite/feed",                 "category": "fortnite"},
    {"name": "Dexerto Fortnite",     "url": "https://www.dexerto.com/fortnite/feed/",               "category": "fortnite"},

    # ===============================================
    # CALL OF DUTY
    # ===============================================
    {"name": "Breaking Point CDL",   "url": "https://breakingpoint.gg/feed",                        "category": "cod"},
    {"name": "Dot Esports CoD",      "url": "https://dotesports.com/call-of-duty/feed",             "category": "cod"},
    {"name": "Dexerto CoD",          "url": "https://www.dexerto.com/call-of-duty/feed/",           "category": "cod"},

    # ===============================================
    # OVERWATCH
    # ===============================================
    {"name": "Over.gg",              "url": "https://www.over.gg/news.rss",                         "category": "overwatch"},
    {"name": "Dot Esports OW",       "url": "https://dotesports.com/overwatch/feed",                "category": "overwatch"},
    {"name": "Dexerto OW",           "url": "https://www.dexerto.com/overwatch/feed/",              "category": "overwatch"},

    # ===============================================
    # APEX LEGENDS
    # ===============================================
    {"name": "Dot Esports Apex",     "url": "https://dotesports.com/apex-legends/feed",             "category": "apex"},
    {"name": "Dexerto Apex",         "url": "https://www.dexerto.com/apex-legends/feed/",           "category": "apex"},

    # ===============================================
    # MOBILE ESPORTS (MLBB / PUBGM / FREE FIRE)
    # ===============================================
    {"name": "AFK Gaming",                  "url": "https://afkgaming.com/feeds/esports",            "category": "mobile"},
    {"name": "ONE Esports MLBB",            "url": "https://www.oneesports.gg/mobile-legends/feed/", "category": "mlbb"},
    {"name": "ONE Esports PUBG Mobile",     "url": "https://www.oneesports.gg/pubg-mobile/feed/",    "category": "pubgm"},
    {"name": "ONE Esports Free Fire",       "url": "https://www.oneesports.gg/free-fire/feed/",      "category": "ff"},
    {"name": "ONE Esports Wild Rift",       "url": "https://www.oneesports.gg/wild-rift/feed/",      "category": "wildrift"},
    {"name": "Talkesport",                  "url": "https://www.talkesport.com/feed/",               "category": "mobile"},

    # ===============================================
    # FIGHTING GAMES / FGC
    # ===============================================
    {"name": "Event Hubs",           "url": "https://www.eventhubs.com/rss/news/",                  "category": "fgc"},
]
