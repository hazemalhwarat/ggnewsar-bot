import os
import json
import time
import hashlib
from datetime import datetime, timedelta, timezone

import feedparser
import requests

from dateutil import parser as dateparser

from feeds import FEEDS

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

DB_FILE = "sent_news.json"

HEADERS = {
    "User-Agent": "GGNewsBot/1.0"
}
def load_sent():
    if not os.path.exists(DB_FILE):
        return {}

    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_sent(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


SENT = load_sent()def send_message(text):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    r = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text,
            "disable_web_page_preview": False,
        },
        timeout=30,
    )

    print(r.status_code)def is_recent(date_string):

    try:
        published = dateparser.parse(date_string)

        if published.tzinfo is None:
            published = published.replace(tzinfo=timezone.utc)

        return (
            datetime.now(timezone.utc) - published
        ) <= timedelta(hours=24)

    except:
        return False 
def already_sent(link):

    uid = hashlib.md5(link.encode()).hexdigest()

    if uid in SENT:
        return True

    SENT[uid] = time.time()

    return False 
def fetch_rss(source_name, url):

    news = []

    try:

        feed = feedparser.parse(url)

        for entry in feed.entries:

            published = ""

            if hasattr(entry, "published"):
                published = entry.published

            elif hasattr(entry, "updated"):
                published = entry.updated

            if not published:
                continue

            if not is_recent(published):
                continue

            link = entry.link

            if already_sent(link):
                continue

            news.append({
                "source": source_name,
                "title": entry.title.strip(),
                "link": link,
                "date": published,
            })

    except Exception as e:
        print(source_name, e)

    return news


def fetch_reddit(source_name, url):

    news = []

    try:

        data = requests.get(
            url,
            headers=HEADERS,
            timeout=20,
        ).json()

        posts = data["data"]["children"]

        for post in posts:

            post = post["data"]

            published = datetime.fromtimestamp(
                post["created_utc"],
                tz=timezone.utc,
            )

            if (
                datetime.now(timezone.utc) - published
            ) > timedelta(hours=24):
                continue

            link = "https://reddit.com" + post["permalink"]

            if already_sent(link):
                continue

            news.append({
                "source": source_name,
                "title": post["title"],
                "link": link,
                "date": published.isoformat(),
            })

    except Exception as e:
        print(source_name, e)

    return news
def collect_news():

    all_news = []

    for source_name, source_type, url in FEEDS:

        print("Checking:", source_name)

        if source_type == "rss":

            all_news.extend(
                fetch_rss(source_name, url)
            )

        elif source_type == "reddit":

            all_news.extend(
                fetch_reddit(source_name, url)
            )

    return all_news
    def cleanup():

    now = time.time()

    remove = []

    for uid, ts in SENT.items():

        if now - ts > 60 * 60 * 24 * 7:
            remove.append(uid)

    for uid in remove:
        del SENT[uid]

    save_sent(SENT)


def main():

    print("=" * 60)
    print("GGNews Bot Started")
    print("=" * 60)

    news = collect_news()

    print(f"Found {len(news)} news")

    news.sort(
        key=lambda x: x["date"],
        reverse=True,
    )

    for item in news:

        text = (
            f"📰 {item['title']}\n\n"
            f"🏷 Source: {item['source']}\n"
            f"🔗 {item['link']}"
        )

        try:

            send_message(text)

            time.sleep(2)

        except Exception as e:

            print(e)

    cleanup()

    print("Finished")


if __name__ == "__main__":
    main()
    
