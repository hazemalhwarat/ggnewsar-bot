"""
GGNewsAR Bot — RSS Feed Configuration
Large candidate list assembled from documented esports RSS directories
(Feedspot game-specific lists, publisher sites). English-language only.

IMPORTANT — read before editing:
  "verified": True  -> confirmed working in an actual GitHub Actions run.
  "verified": False -> URL exists in public RSS directories, but the exact
                       feed path has NOT been tested live yet. Some of these
                       will fail on first run. That is expected.

Workflow for cleanup after each run:
  1. Check the Actions log "Failed Sources" section.
  2. Delete failing entries from this file (or fix the URL if you find the
     correct path).
  3. Sources that work move from verified=False to verified=True over time.

This list intentionally errs toward MORE sources per user request — quantity
over pre-verification. bot.py is built to skip failures gracefully and keep
running, so a dead feed here does not break anything else.
"""

RSS_FEEDS = [
    # ============================================================
    # Confirmed working (verified in live test, 2026-06-27/28)
    # ============================================================
    {"name": "HLTV", "url": "https://www.hltv.org/rss/news", "verified": True},
    {"name": "VLR.gg", "url": "https://vlr.gg/rss", "verified": True},
    {"name": "Dotabuff Blog", "url": "https://www.dotabuff.com/blog.rss", "verified": True},
    {"name": "Dot Esports", "url": "https://dotesports.com/feed", "verified": True},
    {"name": "Esports Insider", "url": "https://esportsinsider.com/feed", "verified": True},
    {"name": "ESTNN", "url": "https://estnn.com/feed", "verified": True},
    {"name": "Esports News UK", "url": "https://esports-news.co.uk/feed", "verified": True},
    {"name": "Insider Gaming", "url": "https://insider-gaming.com/feed", "verified": True},
    {"name": "The Esports Radar", "url": "https://esportsradar.gg/feed", "verified": True},
    {"name": "Esports.gg", "url": "https://esports.gg/feed", "verified": True},
    {"name": "The Loadout", "url": "https://www.theloadout.com/feed", "verified": True},

    # ============================================================
    # General esports aggregators (unverified)
    # ============================================================
    {"name": "TalkEsport", "url": "https://talkesport.com/feed", "verified": False},
    {"name": "Esports Talk", "url": "https://esportstalk.com/feed", "verified": False},
    {"name": "The Game Haus", "url": "https://thegamehaus.com/feed", "verified": False},
    {"name": "Snowball Esports", "url": "https://snowballesports.com/feed", "verified": False},
    {"name": "AFK Gaming", "url": "https://afkgaming.com/rssfeed", "verified": False},
    {"name": "Dexerto Esports", "url": "https://www.dexerto.com/esports/feed", "verified": False},
    {"name": "WIN.gg", "url": "https://win.gg/feed", "verified": False},
    {"name": "GosuGamers", "url": "https://www.gosugamers.net/feed", "verified": False},
    {"name": "Esports.com", "url": "https://www.esports.com/en/feed", "verified": False},
    {"name": "DBLTap", "url": "https://www.dbltap.com/feed", "verified": False},
    {"name": "Esports.net", "url": "https://www.esports.net/feed", "verified": False},
    {"name": "Fragster", "url": "https://fragster.com/feed", "verified": False},
    {"name": "Hotspawn", "url": "https://www.hotspawn.com/feed", "verified": False},
    {"name": "GameRiv", "url": "https://gameriv.com/feed", "verified": False},
    {"name": "Esports Wizard", "url": "https://esportswizard.com/feed", "verified": False},
    {"name": "G2G News Esports", "url": "https://g2g.news/feed", "verified": False},
    {"name": "GamingOnPhone", "url": "https://gamingonphone.com/feed", "verified": False},
    {"name": "ONE Esports", "url": "https://www.oneesports.gg/feed", "verified": False},
    {"name": "Esports Group", "url": "https://esportsgroup.net/feed", "verified": False},

    # ============================================================
    # Counter-Strike / CS2
    # ============================================================
    {"name": "Way to Smurf", "url": "https://www.waytosmurf.com/feed", "verified": False},
    {"name": "CS Spy", "url": "https://csspy.com/feed", "verified": False},
    {"name": "UKCSGO", "url": "https://ukcsgo.com/feed", "verified": False},
    {"name": "CSGO2ASIA", "url": "https://csgo2asia.com/feed", "verified": False},
    {"name": "Esports Talk CS", "url": "https://esportstalk.com/blog/csgo/feed", "verified": False},
    {"name": "Counter-Strike Official Blog", "url": "https://blog.counter-strike.net/index.php/feed", "verified": False},

    # ============================================================
    # VALORANT
    # ============================================================
    {"name": "GameRiv Valorant", "url": "https://gameriv.com/valorant/feed", "verified": False},
    {"name": "Esports Talk Valorant", "url": "https://esportstalk.com/blog/valorant/feed", "verified": False},
    {"name": "Esports.net Valorant", "url": "https://www.esports.net/news/valorant/feed", "verified": False},
    {"name": "Fragster Valorant", "url": "https://fragster.com/valorant/feed", "verified": False},
    {"name": "ValorantInfo.gg", "url": "https://valorantinfo.gg/feed", "verified": False},
    {"name": "DBLTap Valorant", "url": "https://www.dbltap.com/leagues/valorant/feed", "verified": False},

    # ============================================================
    # League of Legends
    # ============================================================
    {"name": "Nerfplz", "url": "https://www.nerfplz.com/feeds/posts/default", "verified": False},
    {"name": "LoL News", "url": "https://lolnews.com/feed", "verified": False},
    {"name": "Surrender at 20", "url": "https://feeds.feedburner.com/Surrenderat20", "verified": False},
    {"name": "ESTNN LoL", "url": "https://estnn.com/tag/league-of-legends/feed", "verified": False},
    {"name": "Snowball LoL", "url": "https://snowballesports.com/games/league-of-legends/feed", "verified": False},
    {"name": "Esports Talk LoL", "url": "https://esportstalk.com/blog/league-of-legends/feed", "verified": False},
    {"name": "Escorenews LoL", "url": "https://escorenews.com/en/lol/feed", "verified": False},

    # ============================================================
    # Dota 2
    # ============================================================
    {"name": "ONE Esports Dota 2", "url": "https://www.oneesports.gg/dota2/feed", "verified": False},
    {"name": "Esports.net Dota", "url": "https://www.esports.net/news/dota/feed", "verified": False},
    {"name": "DotaBlast", "url": "https://dotablast.com/feed", "verified": False},
    {"name": "Sportskeeda Dota 2", "url": "https://www.sportskeeda.com/esports/dota-2/feed", "verified": False},
    {"name": "Esports.com Dota 2", "url": "https://www.esports.com/en/dota-2/feed", "verified": False},
    {"name": "WIN.gg Dota 2", "url": "https://win.gg/dota2/feed", "verified": False},

    # ============================================================
    # Overwatch
    # ============================================================
    {"name": "Fragster Overwatch", "url": "https://fragster.com/overwatch/feed", "verified": False},
    {"name": "Esports Talk Overwatch", "url": "https://esportstalk.com/blog/overwatch/feed", "verified": False},
    {"name": "DBLTap Overwatch", "url": "https://www.dbltap.com/leagues/overwatch/feed", "verified": False},
    {"name": "Hotspawn Overwatch", "url": "https://www.hotspawn.com/overwatch/news/feed", "verified": False},
    {"name": "ESTNN Overwatch", "url": "https://estnn.com/tag/overwatch-esports/feed", "verified": False},

    # ============================================================
    # Call of Duty
    # ============================================================
    {"name": "Esports Talk CoD", "url": "https://esportstalk.com/blog/call-of-duty/feed", "verified": False},
    {"name": "ONE Esports CoD", "url": "https://www.oneesports.gg/call-of-duty/feed", "verified": False},
    {"name": "MP1st CoD", "url": "https://mp1st.com/tag/call-of-duty/feed", "verified": False},
    {"name": "Global Esports News CoD", "url": "https://global-esports.news/category/call-of-duty/feed", "verified": False},

    # ============================================================
    # Apex Legends
    # ============================================================
    {"name": "Esports Wizard Apex", "url": "https://esportswizard.com/news/tag/apex-legends/feed", "verified": False},
    {"name": "Dexerto Apex", "url": "https://www.dexerto.com/apex-legends/feed", "verified": False},
    {"name": "ONE Esports Apex", "url": "https://www.oneesports.gg/apex-legends/feed", "verified": False},

    # ============================================================
    # PUBG / PUBG Mobile / Battle Royale
    # ============================================================
    {"name": "Dot Esports PUBG", "url": "https://dotesports.com/pubg/feed", "verified": False},
    {"name": "Esports Talk PUBG Mobile", "url": "https://esportstalk.com/news/pubg-mobile/feed", "verified": False},
    {"name": "The Loadout PUBG", "url": "https://www.theloadout.com/pubg/feed", "verified": False},
    {"name": "DBLTap PUBG", "url": "https://www.dbltap.com/leagues/pubg/feed", "verified": False},

    # ============================================================
    # Mobile esports (Mobile Legends, general mobile)
    # ============================================================
    {"name": "GamingOnPhone News", "url": "https://gamingonphone.com/category/news/feed", "verified": False},
    {"name": "Esports.net Mobile Games", "url": "https://www.esports.net/news/mobile-games/feed", "verified": False},

    # ============================================================
    # Rocket League
    # ============================================================
    {"name": "RLRSS", "url": "https://rlrss.qrivi.dev/feed", "verified": False},

    # ============================================================
    # Fighting Games (FGC)
    # ============================================================
    {"name": "EventHubs", "url": "https://www.eventhubs.com/feed/", "verified": False},

    # ============================================================
    # India / Asia esports (English-language)
    # ============================================================
    {"name": "AFK Gaming Alt", "url": "https://afkgaming.com/feed", "verified": False},
    {"name": "InsideSport Esports", "url": "https://insidesport.in/topic/esports/feed", "verified": False},
    {"name": "India Today Gaming", "url": "https://www.indiatodaygaming.com/feed", "verified": False},

    # ============================================================
    # Industry / business of esports
    # ============================================================
    {"name": "Esports Insider (alt path)", "url": "https://esportsinsider.com/news/feed", "verified": False},
    {"name": "The Esports Observer Archive", "url": "https://esportsobserver.com/feed", "verified": False},
    {"name": "Esports Advocate", "url": "https://esportsadvocate.net/feed", "verified": False},
    {"name": "Esports Wales", "url": "https://esportswales.org/feed", "verified": False},
    {"name": "GRID Esports Data Blog", "url": "https://blog.grid.gg/feed", "verified": False},

    # ============================================================
    # Rainbow Six (additional)
    # ============================================================
    {"name": "Esports.net Rainbow Six", "url": "https://www.esports.net/news/rainbow-six/feed", "verified": False},
    {"name": "Strafe Valorant", "url": "https://www.strafe.com/news/valorant/feed", "verified": False},
    {"name": "Strafe R6S", "url": "https://www.strafe.com/news/r6s/feed", "verified": False},
    {"name": "Strafe General", "url": "https://www.strafe.com/news/feed", "verified": False},
    {"name": "SiegeGG News", "url": "https://siege.gg/news/feed", "verified": False},

    # ============================================================
    # Racing / sim esports
    # ============================================================
    {"name": "Traxion.gg Esports", "url": "https://traxion.gg/category/esports/feed", "verified": False},

    # ============================================================
    # Philippines / SEA esports (English-language)
    # ============================================================
    {"name": "Esports Inquirer", "url": "https://esports.inquirer.net/feed", "verified": False},
    {"name": "Philstar Esports", "url": "https://www.philstar.com/esport/news/feed", "verified": False},
    {"name": "GamingPH", "url": "https://gamingph.com/feed", "verified": False},

    # ============================================================
    # General gaming sites with strong esports sections
    # ============================================================
    {"name": "GGRecon", "url": "https://www.ggrecon.com/feed", "verified": False},
    {"name": "PC Invasion Esports", "url": "https://www.pcinvasion.com/category/esports/feed", "verified": False},
    {"name": "RealSport101", "url": "https://realsport101.com/feed.xml", "verified": False},
    {"name": "Sportskeeda Esports", "url": "https://www.sportskeeda.com/esports/feed", "verified": False},
    {"name": "TechRadar Gaming", "url": "https://www.techradar.com/feeds/tag/gaming", "verified": False},
    {"name": "Esports Betting News", "url": "https://esportsbets.com/feed", "verified": False},

    # ============================================================
    # More CS2 / VALORANT supplementary
    # ============================================================
    {"name": "Esports Talk CS2 Alt", "url": "https://esportstalk.com/news/csgo/feed", "verified": False},
    {"name": "Escorenews CS2", "url": "https://escorenews.com/en/cs2/feed", "verified": False},
    {"name": "Mobalytics Valorant", "url": "https://mobalytics.gg/blog/valorant/feed", "verified": False},

    # ============================================================
    # More LoL / Dota supplementary
    # ============================================================
    {"name": "Esports Talk Dota2", "url": "https://esportstalk.com/blog/dota-2/feed", "verified": False},
    {"name": "WIN.gg LoL", "url": "https://win.gg/lol/feed", "verified": False},

    # ============================================================
    # More mobile / battle royale supplementary
    # ============================================================
    {"name": "Mobile Gaming Hub", "url": "https://mobilegaminghub.com/feed", "verified": False},
    {"name": "PC Games N Esports", "url": "https://www.pcgamesn.com/feed", "verified": False},
]


if __name__ == "__main__":
    print(f"Total feeds: {len(RSS_FEEDS)}")
    print(f"Verified:   {sum(1 for f in RSS_FEEDS if f.get('verified'))}")
    print(f"Unverified: {sum(1 for f in RSS_FEEDS if not f.get('verified'))}")
