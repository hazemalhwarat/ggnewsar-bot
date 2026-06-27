"""
filters.py — GGNewsAR bot v7
All relevance logic, separated from the engine.

Decision pipeline (returns "send" or "drop: <reason>"):

  1) MATCH RESULT GUARD
     - any live score, recap, group stage, head to head, vs, scoreline -> DROP
       (no exceptions, per user spec)

  2) GAME CONTENT GUARD (with competitive escape hatch)
     - skins, cosmetics, bundles, codes, in game events, lore, story    -> DROP
     - guides, tier lists, best settings, how to                        -> DROP
     - patches and balance changes                                      -> DROP
       UNLESS the same item mentions a tournament / circuit / pro scene
       (so "Riot nerfs Jett before VCT Champions" still passes).

  3) GAME ADDITIONS REGEX (with same escape hatch)
     - "new <game> agent/operator/hero/legend/map/weapon/mode/skin"     -> DROP
       UNLESS competitive context appears in the same text.

  4) NON LISTED GAMES
     - if text mentions an excluded game and NOT a listed competitive
       title nor an esports word -> DROP
     - if it mentions an "additional title" (Fortnite, Marvel Rivals,
       Free Fire, Brawl Stars, Smash, Delta Force, Naraka, Wild Rift,
       EA FC), it must also have a competitive signal -> else DROP

  5) TIER 2 GATE
     - general / mainstream sources must mention an esports title or term

  6) TRADITIONAL SPORTS / ENTERTAINMENT
     - blacklist hit AND no esports word -> DROP

  Anything not dropped is SENT.
"""

import re

# ----------------------------------------------------------------------------
# CORE TITLE SCOPE — your 14 main competitive titles + esports umbrella.
# Used for tier 2 gating and as escape hatch for blacklists.
# ----------------------------------------------------------------------------
TITLE_SCOPE = [
    # esports umbrella
    "esports", "esport", "e-sports", "e-sport",
    # CS2
    "counter-strike", "cs2", "csgo",
    # VALORANT
    "valorant", "vct", "champions tour", "valorant champions",
    # League of Legends
    "league of legends", "lol esports", "worlds", "msi",
    "lck", "lec", "lpl", "lcs",
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
    "call of duty league", "cdl", "warzone",
    # Overwatch
    "overwatch", "owcs", "overwatch champions",
    # Apex Legends
    "apex legends", "algs",
    # Fighting games
    "tekken", "street fighter", "mortal kombat", "fighting game", "evo",
    # Chess
    "chess",
    # Multi game / regional events
    "ewc", "esports world cup", "esports nations cup", "asian games",
    "iem", "esl pro league", "esl", "blast", "pgl",
    "saudi", "riyadh",
    # Distinctive esports orgs (catch short headlines)
    "navi", "faze", "fnatic", "astralis", "team falcons", "falcons esports",
    "team liquid", "team spirit", "team vitality", "sentinels", "gen.g",
    "the mongolz", "furia", "g2 esports", "twisted minds", "geekay",
    "cloud9", "evil geniuses", "karmine corp", "paper rex", "t1 esports",
    "nigma", "fate esports",
]

# ----------------------------------------------------------------------------
# ADDITIONAL TITLES — covered ONLY when a competitive signal is present.
# ----------------------------------------------------------------------------
ADDITIONAL_TITLES = [
    "fortnite", "fncs",
    "marvel rivals",
    "free fire", "free fire max", "ffws", "ffwc",
    "brawl stars", "brawl stars championship",
    "smash bros", "super smash",
    "delta force",
    "naraka", "naraka bladepoint",
    "wild rift", "wcs",
    "ea fc", "ea sports fc", "fc pro",
    "teamfight tactics", "tft",
    "hearthstone",
]

# ----------------------------------------------------------------------------
# COMPETITIVE SIGNALS — used as the escape hatch when an item looks like
# game content but is actually about the competitive scene.
# Also required to validate ADDITIONAL_TITLES.
# ----------------------------------------------------------------------------
COMPETITIVE_SIGNALS = [
    # events
    "tournament", "qualifier", "qualify", "qualified", "qualifies",
    "playoffs", "playoff", "grand final", "finals", "semifinal", "semi-final",
    "bracket", "championship", "champions", "champion", "title", "trophy",
    "crowned", "winners", "prize pool", "lan event", "major",
    # roster
    "roster", "lineup", "line-up", "signs", "signing", "sign", "signed",
    "transfer", "benched", "stand-in", "free agent",
    "joins", "joined", "leaves", "departs", "departure",
    "retires", "retirement", "acquire", "acquires",
    "pro player", "head coach", "igl",
    # business
    "sponsorship", "sponsor", "sponsors", "title sponsor",
    "partnership", "partners with", "partner with",
    "investment", "investor", "funding", "valuation", "acquisition",
    "viewership", "viewers", "peak viewers",
    # circuits double as signals
    "vct", "iem", "esl", "blast", "pgl", "rlcs", "cdl", "algs", "mpl",
    "ewc", "the international", "worlds", "msi", "owcs", "six invitational",
    "fncs",
]

# ----------------------------------------------------------------------------
# GAME CONTENT — words that mark pure game content (drop UNLESS competitive).
# ----------------------------------------------------------------------------
GAME_CONTENT = [
    # cosmetics
    "skin", "skins", "cosmetic", "cosmetics", "bundle", "battle pass", "battlepass",
    # patches / balance
    "patch", "patch notes", "patch update", "hotfix", "buff", "buffs", "nerf", "nerfs",
    "balance changes", "balance patch", "balance update",
    # guides
    "tier list", "best settings", "best loadout", "loadout", "best agents",
    "best heroes", "best champions", "best legends", "best operators",
    "best builds", "best class", "best weapons",
    "guide", "how to", "walkthrough", "tips and tricks", "beginner",
    "guides for", "ranking the", "ranked: best",
    # game world
    "lore", "story mode", "campaign", "release date", "launch date",
    "trailer", "gameplay reveal", "datamine", "datamined", "leaked skin",
    # in game
    "dlc", "expansion pack", "early access",
    "redeem code", "redeem codes", "free rewards", "promo code",
    # crossovers (game side)
    "crossover skin", "collab skin",
]

# Game additions with the title in the middle: "new VALORANT agent".
GAME_CONTENT_RE = re.compile(
    r"\bnew\s+(?:\w+\s+){0,3}"
    r"(agent|operator|hero|legend|map|weapon|mode|skin|character|bundle|gun)\b",
    re.I,
)

# "best <something>" guide patterns with the game name often in between.
BEST_OF_RE = re.compile(
    r"\bbest\s+(?:\w+\s+){0,3}"
    r"(agents?|heroes?|champions?|legends?|operators?|builds?|classes?|weapons?|guns?|"
    r"settings?|loadouts?|sensitivities?|crosshairs?|maps?|setups?|comps?)\b",
    re.I,
)
# Other guide phrases.
GUIDE_PHRASE_RE = re.compile(
    r"\b(tier list|how to|walkthrough|tips and tricks|beginner['s]* guide|"
    r"complete guide|ultimate guide|ranking every|ranked from worst to best)\b",
    re.I,
)

# ----------------------------------------------------------------------------
# EXCLUDED_TITLES — games never in scope.
# ----------------------------------------------------------------------------
EXCLUDED_TITLES = [
    "world of warcraft", "wow classic",
    "genshin", "wuthering waves", "honkai",
    "roblox", "minecraft",
    "pokemon", "pokémon", "pokemon unite",
    "marvel snap",
    "diablo", "path of exile",
    "valheim", "elden ring", "elden ring nightreign",
    "baldur", "starfield", "cyberpunk",
    "the last of us", "spider-man", "god of war",
    "gta", "grand theft auto",
    "sims 4", "the sims",
    "stardew", "factorio",
    "tarkov", "escape from tarkov",
    "destiny 2", "deadlock",
]

# ----------------------------------------------------------------------------
# RESULT PATTERNS — live / routine match scores. Always drop, no exceptions.
# ----------------------------------------------------------------------------
RESULT_RE = re.compile(
    r"\blive\b[: ]|\blive blog\b|"
    r"\bresults?\b|\brecap\b|\bround-?up\b|\bstandings\b|"
    r"\bgroup stage day\b|\bday \d\b|\bmatchday\b|"
    r"\b\d{1,2}\s?[-\u2013:]\s?\d{1,2}\b|"      # scorelines 16-14, 2-1, 3:0
    r"\b(beat|beats|defeat|defeats|def\.|downs|edge|edges|topple|overcome)\b|"
    r"\bvs\.?\b|\bhead to head\b",
    re.I,
)

# ----------------------------------------------------------------------------
# BLACKLIST — traditional sports / entertainment. Only blocks when no esports.
# ----------------------------------------------------------------------------
BLACKLIST = [
    "nfl", "nba", "mlb", "nhl",
    "premier league", "la liga", "serie a", "bundesliga", "ligue 1",
    "formula 1", "f1 grand prix", "ufc", "wwe", "boxing",
    "golf", "tennis", "nascar", "transfer deadline day",
    "netflix series", "tiktok trend", "kardashian", "box office", "movie review",
]

ESPORTS_WORDS = ["esports", "esport", "e-sports", "e-sport"]

# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def _has_any(text: str, keywords) -> bool:
    return any(re.search(r"\b" + re.escape(k.strip()) + r"\b", text) for k in keywords)


def _strip_html(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


# ----------------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------------
def is_match_result(title: str, summary: str) -> bool:
    """True = a live / routine match result. Always dropped (user spec)."""
    text = (title + " " + _strip_html(summary)).lower()
    return bool(RESULT_RE.search(text))


def relevance_decision(title: str, summary: str, tier: int) -> tuple[bool, str]:
    """
    Returns (send, reason). reason is empty when send=True.

    The pipeline mirrors the docstring at the top of this module.
    """
    text = (title + " " + _strip_html(summary)).lower()

    has_competitive = _has_any(text, COMPETITIVE_SIGNALS)
    has_title_scope = _has_any(text, TITLE_SCOPE)
    has_additional = _has_any(text, ADDITIONAL_TITLES)
    has_excluded = _has_any(text, EXCLUDED_TITLES)
    has_esports_word = _has_any(text, ESPORTS_WORDS)
    has_blacklist = _has_any(text, BLACKLIST)
    has_game_content = (
        _has_any(text, GAME_CONTENT)
        or bool(GAME_CONTENT_RE.search(text))
        or bool(BEST_OF_RE.search(text))
        or bool(GUIDE_PHRASE_RE.search(text))
    )

    # 1) Game content -> drop unless competitive context is present
    if has_game_content and not has_competitive:
        return False, "game_content"

    # 2) Non listed games -> drop, unless a listed title or esports word also present
    if has_excluded and not has_title_scope and not has_esports_word:
        return False, "excluded_title"

    # 3) Additional titles -> require a competitive signal
    if has_additional and not has_title_scope and not has_competitive:
        return False, "additional_title_no_signal"

    # 4) Tier 2 gate -> general site must mention esports
    if tier == 2 and not has_title_scope and not has_additional:
        return False, "tier2_no_scope"

    # 5) Traditional sports / entertainment guard
    if has_blacklist and not has_esports_word:
        return False, "blacklist"

    return True, ""


def should_send(title: str, summary: str, tier: int) -> tuple[bool, str]:
    """Combine match result guard and relevance. Returns (send, reason)."""
    if is_match_result(title, summary):
        return False, "match_result"
    return relevance_decision(title, summary, tier)
