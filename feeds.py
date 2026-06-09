# -*- coding: utf-8 -*-
"""
GGNewsAR — قائمة RSS feeds للرياضات الإلكترونية
================================================================
البنية: قاموس مصنّف حسب اللعبة/الفئة، كل عنصر يحتوي:
  - name: الاسم المختصر
  - url: رابط الـ RSS
  - lang: en / multi
  - category: الفئة (مفيدة للوغ والتصنيف، ليست للفلترة)

ملاحظات:
  - أُزيلت الأولوية — البوت يعالج كل المصادر بالتساوي
  - معظم مواقع WordPress تستخدم /feed/ (الصيغة القياسية)
  - فيه احتمال 10–15% من الروابط ميتة أو تحتاج تعديل، البوت راح يتجاهلها بصمت
    لو سجّلت اللوغ المناسب في bot.py
"""

RSS_FEEDS = {

    # ════════════════════════════════════════════════════════════════
    # 1) أخبار عامة متعددة الألعاب — العمود الفقري
    # ════════════════════════════════════════════════════════════════
    "general_multigame": [
        {"name": "Dot Esports",            "url": "https://dotesports.com/feed",                       "lang": "en"},
        {"name": "Dexerto Esports",        "url": "https://www.dexerto.com/feed/",                     "lang": "en"},
        {"name": "ONE Esports",            "url": "https://www.oneesports.gg/feed/",                   "lang": "en"},
        {"name": "ESTNN",                  "url": "https://estnn.com/feed/",                           "lang": "en"},
        {"name": "Esports.gg",             "url": "https://esports.gg/feed/",                          "lang": "en"},
        {"name": "Esports.net",            "url": "https://www.esports.net/feed/",                     "lang": "en"},
        {"name": "Esports News UK",        "url": "https://esports-news.co.uk/feed/",                  "lang": "en"},
        {"name": "GGRecon",                "url": "https://www.ggrecon.com/feed/",                     "lang": "en"},
        {"name": "EarlyGame",              "url": "https://earlygame.com/feed",                        "lang": "en"},
        {"name": "The Game Haus",          "url": "https://thegamehaus.com/feed/",                     "lang": "en"},
        {"name": "Snowball Esports",       "url": "https://snowballesports.com/feed/",                 "lang": "en"},
        {"name": "Esportimes",             "url": "https://esportimes.com/en/feed/",                   "lang": "en"},
        {"name": "Hotspawn",               "url": "https://www.hotspawn.com/feed",                     "lang": "en"},
        {"name": "DBLTAP Esports",         "url": "https://www.dbltap.com/.rss/full/",                 "lang": "en"},
        {"name": "Sportskeeda Esports",    "url": "https://www.sportskeeda.com/feed/esports",          "lang": "en"},
        {"name": "GameRiv",                "url": "https://gameriv.com/feed/",                         "lang": "en"},
        {"name": "Global Esport News",     "url": "https://global-esports.news/feed/",                 "lang": "en"},
        {"name": "EGamersWorld",           "url": "https://egamersworld.com/rss",                      "lang": "en"},
        {"name": "Fragster",               "url": "https://fragster.com/feed/",                        "lang": "en"},
        {"name": "Inven Global",           "url": "https://www.invenglobal.com/rss",                   "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 2) أخبار الصناعة والأعمال (Business / Industry)
    # ════════════════════════════════════════════════════════════════
    "business_industry": [
        {"name": "Esports Insider",         "url": "https://esportsinsider.com/feed",                  "lang": "en"},
        {"name": "The Esports Advocate",    "url": "https://esportsadvocate.com/feed/",                "lang": "en"},
        {"name": "Business of Esports",     "url": "https://thebusinessofesports.com/feed/",           "lang": "en"},
        {"name": "Sports Business Journal", "url": "https://www.sportsbusinessjournal.com/rss/esports","lang": "en"},
        {"name": "PocketGamer.biz",         "url": "https://www.pocketgamer.biz/rss/",                 "lang": "en"},
        {"name": "Esports Charts News",     "url": "https://escharts.com/news.rss",                    "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 3) Counter-Strike 2 / CS:GO
    # ════════════════════════════════════════════════════════════════
    "counter_strike": [
        {"name": "HLTV News",              "url": "https://www.hltv.org/rss/news",                    "lang": "en"},
        {"name": "Dot Esports — CS",       "url": "https://dotesports.com/counter-strike/feed",        "lang": "en"},
        {"name": "Dexerto — CS",           "url": "https://www.dexerto.com/cs2/feed/",                 "lang": "en"},
        {"name": "Esports.gg — CS",        "url": "https://esports.gg/news/counter-strike/feed/",      "lang": "en"},
        {"name": "ESTNN — CS",             "url": "https://estnn.com/category/csgo/feed/",             "lang": "en"},
        {"name": "Esports Talk — CS",      "url": "https://www.esportstalk.com/blog/csgo/feed/",       "lang": "en"},
        {"name": "CSGO2ASIA",              "url": "https://csgo2asia.com/feed/",                       "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 4) VALORANT
    # ════════════════════════════════════════════════════════════════
    "valorant": [
        {"name": "Dot Esports — Valorant",  "url": "https://dotesports.com/valorant/feed",             "lang": "en"},
        {"name": "Dexerto — Valorant",      "url": "https://www.dexerto.com/valorant/feed/",           "lang": "en"},
        {"name": "ONE Esports — Valorant",  "url": "https://www.oneesports.gg/valorant/feed/",         "lang": "en"},
        {"name": "Esports.gg — Valorant",   "url": "https://esports.gg/news/valorant/feed/",           "lang": "en"},
        {"name": "GGRecon — Valorant",      "url": "https://www.ggrecon.com/valorant/feed/",           "lang": "en"},
        {"name": "Sheep Esports",           "url": "https://www.sheepesports.com/rss.xml",             "lang": "en"},
        {"name": "Valo2Asia",               "url": "https://valo2asia.com/feed/",                      "lang": "en"},
        {"name": "GameRiv — Valorant",      "url": "https://gameriv.com/valorant/feed/",               "lang": "en"},
        {"name": "Strafe — Valorant",       "url": "https://strafe.com/news/valorant/feed/",           "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 5) League of Legends
    # ════════════════════════════════════════════════════════════════
    "league_of_legends": [
        {"name": "Dot Esports — LoL",       "url": "https://dotesports.com/league-of-legends/feed",    "lang": "en"},
        {"name": "Dexerto — LoL",           "url": "https://www.dexerto.com/league-of-legends/feed/",  "lang": "en"},
        {"name": "ONE Esports — LoL",       "url": "https://www.oneesports.gg/league-of-legends/feed/","lang": "en"},
        {"name": "Esports.gg — LoL",        "url": "https://esports.gg/news/league-of-legends/feed/",  "lang": "en"},
        {"name": "Sheep Esports — LoL",     "url": "https://www.sheepesports.com/lol/rss.xml",         "lang": "en"},
        {"name": "Inven Global — LoL",      "url": "https://www.invenglobal.com/lol/rss",              "lang": "en"},
        {"name": "ESTNN — LoL",             "url": "https://estnn.com/tag/league-of-legends/feed/",    "lang": "en"},
        {"name": "Blog of Legends",         "url": "https://blogoflegends.com/feed/",                  "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 6) Dota 2
    # ════════════════════════════════════════════════════════════════
    "dota2": [
        {"name": "Dot Esports — Dota 2",    "url": "https://dotesports.com/dota-2/feed",               "lang": "en"},
        {"name": "Dexerto — Dota 2",        "url": "https://www.dexerto.com/dota2/feed/",              "lang": "en"},
        {"name": "ONE Esports — Dota 2",    "url": "https://www.oneesports.gg/dota-2/feed/",           "lang": "en"},
        {"name": "Esports.gg — Dota 2",     "url": "https://esports.gg/news/dota-2/feed/",             "lang": "en"},
        {"name": "Dotabuff Blog",           "url": "https://www.dotabuff.com/blog.rss",                "lang": "en"},
        {"name": "AFK Gaming — Dota 2",     "url": "https://afkgaming.com/esports/dota2/feed",         "lang": "en"},
        {"name": "Escorenews — Dota 2",     "url": "https://escorenews.com/en/dota-2/rss",             "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 7) Mobile Legends: Bang Bang (MLBB)
    # ════════════════════════════════════════════════════════════════
    "mlbb": [
        {"name": "ONE Esports — MLBB",      "url": "https://www.oneesports.gg/mobile-legends/feed/",   "lang": "en"},
        {"name": "Dot Esports — Mobile",    "url": "https://dotesports.com/mobile/feed",               "lang": "en"},
        {"name": "Esports.gg — MLBB",       "url": "https://esports.gg/news/mobile-legends/feed/",     "lang": "en"},
        {"name": "AFK Gaming — MLBB",       "url": "https://afkgaming.com/mobileesports/mobile-legends/feed", "lang": "en"},
        {"name": "MENA MPL (official)",     "url": "https://mena-mpl.com/feed/",                       "lang": "multi"},
        {"name": "GGWP Indonesia",          "url": "https://ggwp.id/feed",                             "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 8) PUBG / PUBG Mobile / BGMI
    # ════════════════════════════════════════════════════════════════
    "pubg_battle_royale": [
        {"name": "ONE Esports — PUBG",      "url": "https://www.oneesports.gg/pubg-mobile/feed/",      "lang": "en"},
        {"name": "Dot Esports — PUBG",      "url": "https://dotesports.com/pubg/feed",                 "lang": "en"},
        {"name": "AFK Gaming — PUBG",       "url": "https://afkgaming.com/mobileesports/pubg-mobile/feed", "lang": "en"},
        {"name": "Esports.gg — PUBG",       "url": "https://esports.gg/news/pubg/feed/",               "lang": "en"},
        {"name": "Sportskeeda — BGMI",      "url": "https://www.sportskeeda.com/feed/bgmi",            "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 9) Fortnite
    # ════════════════════════════════════════════════════════════════
    "fortnite": [
        {"name": "Dot Esports — Fortnite",  "url": "https://dotesports.com/fortnite/feed",             "lang": "en"},
        {"name": "Dexerto — Fortnite",      "url": "https://www.dexerto.com/fortnite/feed/",           "lang": "en"},
        {"name": "Esports.gg — Fortnite",   "url": "https://esports.gg/news/fortnite/feed/",           "lang": "en"},
        {"name": "Fortnite Tracker",        "url": "https://fortnitetracker.com/site-api/feed.xml",    "lang": "en"},
        {"name": "ProGameGuides — FN",      "url": "https://progameguides.com/fortnite/feed/",         "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 10) Rocket League
    # ════════════════════════════════════════════════════════════════
    "rocket_league": [
        {"name": "Dot Esports — RL",        "url": "https://dotesports.com/rocket-league/feed",        "lang": "en"},
        {"name": "Dexerto — RL",            "url": "https://www.dexerto.com/rocket-league/feed/",      "lang": "en"},
        {"name": "Esports.gg — RL",         "url": "https://esports.gg/news/rocket-league/feed/",      "lang": "en"},
        {"name": "Rocketeers",              "url": "https://rocketeers.gg/feed/",                      "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 11) Rainbow Six Siege
    # ════════════════════════════════════════════════════════════════
    "rainbow_six": [
        {"name": "Dot Esports — R6",        "url": "https://dotesports.com/rainbow-6/feed",            "lang": "en"},
        {"name": "Dexerto — R6",            "url": "https://www.dexerto.com/rainbow-six/feed/",        "lang": "en"},
        {"name": "Esports.gg — R6",         "url": "https://esports.gg/news/rainbow-six/feed/",        "lang": "en"},
        {"name": "SiegeGG",                 "url": "https://siege.gg/news.rss",                        "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 12) Apex Legends
    # ════════════════════════════════════════════════════════════════
    "apex_legends": [
        {"name": "Dot Esports — Apex",      "url": "https://dotesports.com/apex-legends/feed",         "lang": "en"},
        {"name": "Dexerto — Apex",          "url": "https://www.dexerto.com/apex-legends/feed/",       "lang": "en"},
        {"name": "ONE Esports — Apex",      "url": "https://www.oneesports.gg/apex-legends/feed/",     "lang": "en"},
        {"name": "Esports.gg — Apex",       "url": "https://esports.gg/news/apex-legends/feed/",       "lang": "en"},
        {"name": "PCGamesN — Apex",         "url": "https://www.pcgamesn.com/apex-legends/feed",       "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 13) Call of Duty
    # ════════════════════════════════════════════════════════════════
    "call_of_duty": [
        {"name": "Charlie Intel",           "url": "https://charlieintel.com/feed/",                   "lang": "en"},
        {"name": "Dexerto — CoD",           "url": "https://www.dexerto.com/call-of-duty/feed/",       "lang": "en"},
        {"name": "Dot Esports — CoD",       "url": "https://dotesports.com/call-of-duty/feed",         "lang": "en"},
        {"name": "Esports.gg — CoD",        "url": "https://esports.gg/news/call-of-duty/feed/",       "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 14) Overwatch
    # ════════════════════════════════════════════════════════════════
    "overwatch": [
        {"name": "Dot Esports — OW",        "url": "https://dotesports.com/overwatch/feed",            "lang": "en"},
        {"name": "Dexerto — OW",            "url": "https://www.dexerto.com/overwatch/feed/",          "lang": "en"},
        {"name": "Esports.gg — OW",         "url": "https://esports.gg/news/overwatch/feed/",          "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 15) Fighting Games (Tekken / SF / MK / Smash)
    # ════════════════════════════════════════════════════════════════
    "fighting_games": [
        {"name": "Dot Esports — Fighting",  "url": "https://dotesports.com/fgc/feed",                  "lang": "en"},
        {"name": "Dexerto — Fighting",      "url": "https://www.dexerto.com/fighting-games/feed/",     "lang": "en"},
        {"name": "EventHubs",               "url": "https://www.eventhubs.com/rss/news/",              "lang": "en"},
        {"name": "Esports.gg — Fighting",   "url": "https://esports.gg/news/fighting-games/feed/",     "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 16) Marvel Rivals
    # ════════════════════════════════════════════════════════════════
    "marvel_rivals": [
        {"name": "Dot Esports — MR",        "url": "https://dotesports.com/marvel-rivals/feed",        "lang": "en"},
        {"name": "Dexerto — MR",            "url": "https://www.dexerto.com/marvel-rivals/feed/",      "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 17) ألعاب موبايل أخرى (Free Fire / Wild Rift / HoK / Clash Royale)
    # ════════════════════════════════════════════════════════════════
    "mobile_other": [
        {"name": "ONE Esports — Wild Rift", "url": "https://www.oneesports.gg/wild-rift/feed/",        "lang": "en"},
        {"name": "ONE Esports — Free Fire", "url": "https://www.oneesports.gg/free-fire/feed/",        "lang": "en"},
        {"name": "ONE Esports — HoK",       "url": "https://www.oneesports.gg/honor-of-kings/feed/",   "lang": "en"},
        {"name": "AFK Gaming Mobile",       "url": "https://afkgaming.com/mobileesports/feed",         "lang": "en"},
        {"name": "Esports.gg — Clash R",    "url": "https://esports.gg/news/clash-royale/feed/",       "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 18) ألعاب رياضية رقمية (EA FC / F1 / Sim Racing)
    # ════════════════════════════════════════════════════════════════
    "sports_sims": [
        {"name": "F1 Esports News",         "url": "https://f1esports.com/news/feed/",                 "lang": "en"},
        {"name": "Dexerto — FIFA/EA FC",    "url": "https://www.dexerto.com/ea-fc/feed/",              "lang": "en"},
        {"name": "Dot Esports — EA FC",     "url": "https://dotesports.com/ea-fc/feed",                "lang": "en"},
        {"name": "Traxion (Sim Racing)",    "url": "https://traxion.gg/feed/",                         "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 19) منظمو البطولات الرسميون
    # ════════════════════════════════════════════════════════════════
    "tournament_organizers": [
        {"name": "Esports World Cup News",  "url": "https://esportsworldcup.com/en/news/rss",          "lang": "en"},
        {"name": "Riot LoL Esports",        "url": "https://lolesports.com/rss",                       "lang": "en"},
        {"name": "BLAST.tv News",           "url": "https://blast.tv/feed",                            "lang": "en"},
        {"name": "ESL Newsroom",            "url": "https://about.eslgaming.com/feed/",                "lang": "en"},
        {"name": "PGL Esports",             "url": "https://pglesports.com/feed/",                     "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 20) الفرق العربية — Google News RSS لكل فريق
    # السبب: معظم الفرق العربية ما عندها RSS في مواقعها، تنشر بس على X/IG
    # Google News يجمع كل ذكر للفريق من كل المصادر العالمية والإقليمية
    # ════════════════════════════════════════════════════════════════
    "arab_teams_saudi": [
        {"name": "Team Falcons",
         "url": "https://news.google.com/rss/search?q=%22Team+Falcons%22+esports&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Twisted Minds",
         "url": "https://news.google.com/rss/search?q=%22Twisted+Minds%22+esports&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Riyadh Falcons (CDL)",
         "url": "https://news.google.com/rss/search?q=%22Riyadh+Falcons%22&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Power187",
         "url": "https://news.google.com/rss/search?q=%22Power187%22+esports&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "AXE MENA",
         "url": "https://news.google.com/rss/search?q=%22AXE+MENA%22+OR+%22AXE+Esports%22&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "BoostGate Esports",
         "url": "https://news.google.com/rss/search?q=%22BoostGate%22+esports&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "WRG Riyadh",
         "url": "https://news.google.com/rss/search?q=%22WRG+Riyadh%22+OR+%22WRG+Esports%22&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
    ],

    "arab_teams_uae": [
        {"name": "Geekay Esports",
         "url": "https://news.google.com/rss/search?q=%22Geekay+Esports%22&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "NASR Esports",
         "url": "https://news.google.com/rss/search?q=%22NASR+Esports%22&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "YaLLa Esports",
         "url": "https://news.google.com/rss/search?q=%22YaLLa+Esports%22&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Nigma Galaxy",
         "url": "https://news.google.com/rss/search?q=%22Nigma+Galaxy%22&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Fox Esports (MENA)",
         "url": "https://news.google.com/rss/search?q=%22Fox+Esports%22+UAE+OR+MENA&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Storm Esports",
         "url": "https://news.google.com/rss/search?q=%22Storm+Esports%22+MENA&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
    ],

    "arab_teams_egypt": [
        {"name": "Anubis Gaming",
         "url": "https://news.google.com/rss/search?q=%22Anubis+Gaming%22&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Falconize Esports",
         "url": "https://news.google.com/rss/search?q=%22Falconize%22+esports&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "3BL Esports",
         "url": "https://news.google.com/rss/search?q=%223BL+Esports%22+OR+%223BL+Gaming%22&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Egypt Force",
         "url": "https://news.google.com/rss/search?q=%22Egypt+Force%22+esports&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
    ],

    "arab_teams_jordan_levant": [
        {"name": "FATE Esports",
         "url": "https://news.google.com/rss/search?q=%22FATE+Esports%22+Jordan&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "JEF (Jordan Esports Federation)",
         "url": "https://news.google.com/rss/search?q=%22Jordan+Esports+Federation%22+OR+%22JEF+Jordan%22&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 21) البطولات الإقليمية العربية والمنتخبات الوطنية
    # ════════════════════════════════════════════════════════════════
    "arab_tournaments": [
        {"name": "MPL MENA (Mobile Legends)",
         "url": "https://news.google.com/rss/search?q=%22MPL+MENA%22&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Arab Esports Championship",
         "url": "https://news.google.com/rss/search?q=%22Arab+Esports+Championship%22+OR+%22كأس+العرب%22&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Arabic League (Valorant/LoL)",
         "url": "https://news.google.com/rss/search?q=%22Arabic+League%22+esports&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "STAD Tournament",
         "url": "https://news.google.com/rss/search?q=%22STAD+Tournament%22+Jordan&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Gamers8 / EWC Saudi Arabia",
         "url": "https://news.google.com/rss/search?q=%22Gamers8%22+OR+%22Esports+World+Cup%22+Saudi&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Saudi National Team",
         "url": "https://news.google.com/rss/search?q=%22Saudi+Arabia%22+%22national+team%22+esports&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "UAE National Team",
         "url": "https://news.google.com/rss/search?q=%22UAE%22+%22national+team%22+esports&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Jordan National Team",
         "url": "https://news.google.com/rss/search?q=%22Jordan%22+%22national+team%22+esports&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Egypt National Team",
         "url": "https://news.google.com/rss/search?q=%22Egypt%22+%22national+team%22+esports&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Saudi Esports Federation",
         "url": "https://news.google.com/rss/search?q=%22Saudi+Esports+Federation%22&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "MENA esports general",
         "url": "https://news.google.com/rss/search?q=MENA+esports+OR+%22Middle+East%22+esports&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 21) إقليمي — آسيا
    # ════════════════════════════════════════════════════════════════
    "regional_asia": [
        {"name": "AFK Gaming",              "url": "https://afkgaming.com/esports/feed",               "lang": "en"},
        {"name": "TalkEsport (India)",      "url": "https://talkesport.com/feed/",                     "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 22) إقليمي — أوروبا/أوقيانوسيا/أفريقيا
    # ════════════════════════════════════════════════════════════════
    "regional_other": [
        {"name": "Snowball (Oceania)",      "url": "https://snowballesports.com/feed/",                "lang": "en"},
        {"name": "British Esports Assoc.",  "url": "https://britishesports.org/feed/",                 "lang": "en"},
        {"name": "Esports News UK",         "url": "https://esports-news.co.uk/feed/",                 "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 23) إعلام عام يغطي gaming/esports
    # ════════════════════════════════════════════════════════════════
    "general_gaming_media": [
        {"name": "IGN Esports",             "url": "https://feeds.ign.com/ign/esports",                "lang": "en"},
        {"name": "PC Gamer",                "url": "https://www.pcgamer.com/rss/",                     "lang": "en"},
        {"name": "Polygon Esports",         "url": "https://www.polygon.com/rss/group/esports/index.xml","lang": "en"},
        {"name": "Eurogamer",               "url": "https://www.eurogamer.net/feed",                   "lang": "en"},
        {"name": "VG247",                   "url": "https://www.vg247.com/feed",                       "lang": "en"},
        {"name": "Kotaku",                  "url": "https://kotaku.com/rss",                           "lang": "en"},
        {"name": "GameSpot News",           "url": "https://www.gamespot.com/feeds/news/",             "lang": "en"},
        {"name": "ESPN Esports",            "url": "https://www.espn.com/espn/rss/esports/news",       "lang": "en"},
    ],

    # ════════════════════════════════════════════════════════════════
    # 24) Google News searches — احتياطي قوي يلتقط أخبار من كل المصادر
    # ════════════════════════════════════════════════════════════════
    "google_news_searches": [
        {"name": "Google News — Esports",
         "url": "https://news.google.com/rss/search?q=esports&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Google News — Esports World Cup",
         "url": "https://news.google.com/rss/search?q=%22Esports+World+Cup%22&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Google News — IEM Cologne Major",
         "url": "https://news.google.com/rss/search?q=%22IEM+Cologne+Major%22&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Google News — VCT",
         "url": "https://news.google.com/rss/search?q=%22VCT%22+valorant&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Google News — LoL Worlds",
         "url": "https://news.google.com/rss/search?q=%22LoL+Worlds%22+OR+%22League+of+Legends+Worlds%22&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Google News — Esports Nations Cup",
         "url": "https://news.google.com/rss/search?q=%22Esports+Nations+Cup%22&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
        {"name": "Google News — MLBB",
         "url": "https://news.google.com/rss/search?q=%22MLBB%22+OR+%22Mobile+Legends%22+esports&hl=en&gl=US&ceid=US:en",
         "lang": "en"},
    ],

}


# ════════════════════════════════════════════════════════════════
# دوال مساعدة
# ════════════════════════════════════════════════════════════════

def all_feeds():
    """يرجّع قائمة مسطّحة بكل الـ feeds."""
    out = []
    for category, feeds in RSS_FEEDS.items():
        for f in feeds:
            f_with_cat = dict(f)
            f_with_cat["category"] = category
            out.append(f_with_cat)
    return out


def feeds_by_category(category):
    """يرجّع feeds من فئة محدّدة."""
    return [dict(f, category=category) for f in RSS_FEEDS.get(category, [])]


TOTAL_FEEDS = len(all_feeds())
