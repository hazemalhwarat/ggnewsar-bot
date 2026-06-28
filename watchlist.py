"""
GGNewsAR Bot — Liquipedia Watchlist
Pages to monitor for changes. Edit this file to add or remove pages.

Notes:
- Use underscores in page titles, exactly as in the Liquipedia URL
- For example, "Team Falcons" → "Team_Falcons"
- Per game, you can have up to ~150 pages before each run becomes slow
"""

WATCHLIST = {
    # === Counter Strike 2 ===
    "counterstrike": [
        # Arab teams (priority)
        "Team_Falcons",
        "Twisted_Minds",
        "Nigma_Galaxy",
        # Top international teams
        "Vitality",
        "Spirit",
        "FaZe",
        "MOUZ",
        "G2_Esports",
        "Natus_Vincere",
        "FURIA",
        "Astralis",
        "Team_Liquid",
        "Eternal_Fire",
        "TheMongolz",
        # Star players (use Liquipedia page names)
        "S1mple",
        "ZywOo",
        "Donk",
        "M0NESY",
        "NiKo",
        "Magisk",
        "B1t",
        "Ropz",
        "Frozen",
        # Active tournaments and seasons
        "IEM_Cologne_2026",
        "BLAST_Premier/Spring/2026",
        "Esports_World_Cup/2026/Counter-Strike_2",
        "Esports_Nations_Cup/2026/Counter-Strike_2",
    ],
    
    # === VALORANT ===
    "valorant": [
        # Arab teams
        "Team_Falcons",
        "Twisted_Minds",
        # Top international
        "Sentinels",
        "Fnatic",
        "Paper_Rex",
        "Team_Heretics",
        "Team_Liquid",
        "EDward_Gaming",
        "DRX",
        "Gen.G",
        "100_Thieves",
        # Tournaments
        "Esports_World_Cup/2026",
        "Esports_Nations_Cup/2026",
        "VCT/2026/Masters",
        "VCT/2026/Champions",
    ],
    
    # === League of Legends ===
    "leagueoflegends": [
        # Top teams
        "T1",
        "Gen.G",
        "JD_Gaming",
        "Bilibili_Gaming",
        "G2_Esports",
        "Fnatic",
        "Hanwha_Life_Esports",
        # Tournaments
        "2026_Season_World_Championship",
        "LCK/2026",
        "LEC/2026",
        "LPL/2026",
        "Esports_World_Cup/2026/League_of_Legends",
    ],
    
    # === Dota 2 ===
    "dota2": [
        # Arab teams
        "Nigma_Galaxy",
        "Team_Falcons",
        # Top teams
        "Team_Spirit",
        "Gaimin_Gladiators",
        "Team_Liquid",
        "PSG_Quest",
        "Tundra_Esports",
        # Tournaments
        "The_International/2026",
        "Esports_World_Cup/2026/Dota_2",
    ],
    
    # === Rainbow Six Siege ===
    "rainbowsix": [
        # Arab teams
        "Team_Falcons",
        "Twisted_Minds",
        # Top international
        "G2_Esports",
        "Team_Liquid",
        "Wolves_Esports",
        "FaZe_Clan",
        # Tournaments
        "Six_Invitational/2026",
        "Esports_World_Cup/2026/Rainbow_Six_Siege",
    ],
    
    # === Rocket League ===
    "rocketleague": [
        # Arab teams
        "Team_Falcons",
        "Twisted_Minds",
        # Top international
        "Karmine_Corp",
        "Gen.G_Mobil1_Racing",
        "Team_BDS",
        "Vitality",
        # Tournaments
        "RLCS_2026",
        "Esports_World_Cup/2026/Rocket_League",
    ],
    
    # === Mobile Legends ===
    "mobilelegends": [
        "ONIC_Esports",
        "RRQ_Hoshi",
        "EVOS_Glory",
        "Selangor_Red_Giants",
        "MPL/Indonesia/2026",
        "Esports_World_Cup/2026/Mobile_Legends:_Bang_Bang",
    ],
    
    # === Honor of Kings ===
    "honorofkings": [
        "Esports_World_Cup/2026/Honor_of_Kings",
        "King_Pro_League/2026",
    ],
    
    # === PUBG Mobile ===
    "pubgmobile": [
        # Arab teams
        "Team_Falcons",
        # Major tournaments
        "PMGC/2026",
        "Esports_World_Cup/2026/PUBG_Mobile",
        "PUBG_Mobile_Asian_Games_2026",
    ],
}


def total_pages() -> int:
    """Total pages being watched across all wikis."""
    return sum(len(pages) for pages in WATCHLIST.values())


def all_wikis() -> list[str]:
    return list(WATCHLIST.keys())
