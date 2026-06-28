"""
GGNewsAR Bot — RSS Feed Configuration
Only sources that were verified working in live GitHub Actions tests.

To add a new source:
  1. Add it here with verified=False
  2. Push and run the bot manually
  3. Check the Actions log: if it appears in "Failed Sources", remove it
     If it appears in sources_ok with entries, set verified=True
"""

RSS_FEEDS = [
    # Game-specific primary sources
    {"name": "HLTV", "url": "https://www.hltv.org/rss/news", "verified": True},
    {"name": "VLR.gg", "url": "https://vlr.gg/rss", "verified": True},
    {"name": "Dotabuff Blog", "url": "https://www.dotabuff.com/blog.rss", "verified": True},

    # Multi-game news sites
    {"name": "Dot Esports", "url": "https://dotesports.com/feed", "verified": True},
    {"name": "Esports Insider", "url": "https://esportsinsider.com/feed", "verified": True},
    {"name": "ESTNN", "url": "https://estnn.com/feed", "verified": True},
    {"name": "Esports News UK", "url": "https://esports-news.co.uk/feed", "verified": True},
    {"name": "Insider Gaming", "url": "https://insider-gaming.com/feed", "verified": True},
    {"name": "The Esports Radar", "url": "https://esportsradar.gg/feed", "verified": True},
    {"name": "Esports.gg", "url": "https://esports.gg/feed", "verified": True},
    {"name": "The Loadout", "url": "https://www.theloadout.com/feed", "verified": True},
]


if __name__ == "__main__":
    print(f"Total feeds: {len(RSS_FEEDS)}")
    print(f"Verified: {sum(1 for f in RSS_FEEDS if f.get('verified'))}")
    for f in RSS_FEEDS:
        print(f"  - {f['name']}: {f['url']}")
