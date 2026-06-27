"""
GGNewsAR Bot — Scraping Targets (Comprehensive)
HTML scraping configuration for sources that don't expose RSS.

Categories:
- arab_team: Saudi/UAE/Arab esports organizations
- federation: Saudi/Jordan/IESF esports federations
- tournament: tournament organizers (ESL, BLAST, PGL, DreamHack, Riot, EWC)
- publisher: game publishers' esports news (Valve, Riot, Ubisoft)

Each target needs:
- url: page listing news/announcements
- selectors: CSS selectors to extract article cards
- active: False until verified manually on first run

When implementing the scraper:
1. Fetch each url with regular User-Agent
2. Parse with BeautifulSoup
3. Find all "container" elements
4. For each container, extract title, link, date

Sites with heavy JS rendering (SPA) need either:
- Playwright/Selenium (heavy, slow), OR
- Mark active=False and rely on Liquipedia + RSS + Reddit
"""

SCRAPE_TARGETS = [
    # =================================================
    # ARAB TEAMS
    # =================================================
    {
        "name": "Team Falcons",
        "url": "https://www.teamfalcons.sa/news",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "multi", "category": "arab_team", "active": False,
        "notes": "Verify /news path exists. SPA site, may need Playwright.",
    },
    {
        "name": "Nigma Galaxy",
        "url": "https://nigmagalaxy.com/",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "multi", "category": "arab_team", "active": False,
        "notes": "Homepage has Announcements + News categories.",
    },
    {
        "name": "Twisted Minds",
        "url": "TBD",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "multi", "category": "arab_team", "active": False,
        "notes": "Primarily on X. Covered indirectly via Liquipedia Watcher.",
    },
    {
        "name": "Geekay Esports",
        "url": "TBD",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "multi", "category": "arab_team", "active": False,
        "notes": "Primarily on X. Covered indirectly via Liquipedia Watcher.",
    },
    {
        "name": "FATE Esports",
        "url": "TBD",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "multi", "category": "arab_team", "active": False,
        "notes": "Primarily on X. Covered indirectly via Liquipedia Watcher.",
    },
    {
        "name": "Power League Gaming",
        "url": "TBD",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "multi", "category": "arab_team", "active": False,
        "notes": "UAE based, covers MENA tournaments.",
    },

    # =================================================
    # FEDERATIONS
    # =================================================
    {
        "name": "Saudi Esports Federation",
        "url": "https://saudiesports.org.sa/en/media/news",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "multi", "category": "federation", "active": False,
        "notes": "Bilingual. Critical for ENC and EWC announcements.",
    },
    {
        "name": "IESF Press",
        "url": "https://iesf.org/news",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "multi", "category": "federation", "active": False,
        "notes": "International Esports Federation. World Esports Championships.",
    },
    {
        "name": "Jordan Esports Federation",
        "url": "TBD",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "multi", "category": "federation", "active": False,
        "notes": "Local relevance. May only have Facebook/Instagram presence.",
    },
    {
        "name": "UAE Esports Federation",
        "url": "TBD",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "multi", "category": "federation", "active": False,
        "notes": "Verify if public news site exists.",
    },

    # =================================================
    # TOURNAMENT ORGANIZERS
    # =================================================
    {
        "name": "Esports World Cup Press",
        "url": "https://esportsworldcup.com/en/press-releases",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "multi", "category": "tournament", "active": False,
        "notes": "Most critical TO source. EWC 2026 announcements + schedule changes.",
    },
    {
        "name": "ESL Gaming News",
        "url": "https://www.eslgaming.com/news",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "multi", "category": "tournament", "active": False,
        "notes": "IEM, ESL Pro League, ESL One, DreamHack. Confirm /news path.",
    },
    {
        "name": "BLAST News",
        "url": "https://blast.tv/news",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "multi", "category": "tournament", "active": False,
        "notes": "BLAST Premier (CS2), BLAST SLAM (Dota 2), BLAST RL.",
    },
    {
        "name": "PGL Esports",
        "url": "https://www.pglesports.com/news",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "multi", "category": "tournament", "active": False,
        "notes": "PGL CS Majors, Dota 2, PUBG events.",
    },
    {
        "name": "DreamHack",
        "url": "https://dreamhack.com/news",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "multi", "category": "tournament", "active": False,
        "notes": "Festival events worldwide, often FGC + CS2.",
    },
    {
        "name": "LoL Esports News",
        "url": "https://lolesports.com/en-US/news/",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "lol", "category": "tournament", "active": False,
        "notes": "Riot Games official LoL Esports. SPA with React, needs Playwright.",
    },
    {
        "name": "VALORANT Esports News",
        "url": "https://valorantesports.com/en-US/news",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "valorant", "category": "tournament", "active": False,
        "notes": "Riot Games official VCT. SPA, needs Playwright.",
    },
    {
        "name": "Ubisoft R6 Esports",
        "url": "https://www.ubisoft.com/en-us/esports/rainbow-six/siege",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "r6", "category": "tournament", "active": False,
        "notes": "Six Invitational, BLAST R6 Major announcements.",
    },
    {
        "name": "ALGS Apex News",
        "url": "https://algs.ea.com/en/news",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "apex", "category": "tournament", "active": False,
        "notes": "Official Apex Legends Global Series news.",
    },
    {
        "name": "FC Pro Official",
        "url": "https://www.ea.com/games/ea-sports-fc/fc-pro/news",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "eafc", "category": "tournament", "active": False,
        "notes": "Official EA FC Pro circuit announcements.",
    },
    {
        "name": "MLBB Esports Official",
        "url": "https://en.moonton.com/news",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "ml", "category": "tournament", "active": False,
        "notes": "Moonton press releases for M-Series, MPL, MSC.",
    },

    # =================================================
    # GAME PUBLISHERS
    # =================================================
    {
        "name": "Counter-Strike Blog",
        "url": "https://www.counter-strike.net/news",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "cs2", "category": "publisher", "active": False,
        "notes": "Valve official CS2 patch notes and operations announcements.",
    },
    {
        "name": "Dota 2 Blog",
        "url": "https://www.dota2.com/news",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "dota2", "category": "publisher", "active": False,
        "notes": "Valve official Dota 2 patches, TI announcements.",
    },
    {
        "name": "Riot Games News",
        "url": "https://www.riotgames.com/en/news",
        "selectors": {"container": "TODO", "title": "TODO", "link": "TODO", "date": "TODO", "summary": "TODO"},
        "game": "multi", "category": "publisher", "active": False,
        "notes": "Riot corporate news (LoL, VAL, TFT, 2XKO).",
    },
]


# === Helpers ===

def active_targets() -> list[dict]:
    return [t for t in SCRAPE_TARGETS if t.get("active")]


def targets_by_category(category: str) -> list[dict]:
    return [t for t in SCRAPE_TARGETS if t.get("category") == category]


def stats() -> dict:
    return {
        "total": len(SCRAPE_TARGETS),
        "active": sum(1 for t in SCRAPE_TARGETS if t.get("active")),
        "arab_teams": sum(1 for t in SCRAPE_TARGETS if t.get("category") == "arab_team"),
        "federations": sum(1 for t in SCRAPE_TARGETS if t.get("category") == "federation"),
        "tournaments": sum(1 for t in SCRAPE_TARGETS if t.get("category") == "tournament"),
        "publishers": sum(1 for t in SCRAPE_TARGETS if t.get("category") == "publisher"),
        "needs_url_confirmation": sum(1 for t in SCRAPE_TARGETS if t.get("url") == "TBD"),
        "needs_selectors": sum(
            1 for t in SCRAPE_TARGETS
            if any(v == "TODO" for v in t.get("selectors", {}).values())
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(stats(), indent=2))
