# -*- coding: utf-8 -*-
"""
GGNewsAR Bot — RSS to Telegram (نسخة بدون AI)
=================================================
- يقرأ كل RSS feeds من feeds.py
- يرسل الجديد فقط لتيليقرام: المصدر + العنوان + الوصف + الرابط
- أول تشغيل: يسكّت كل شي حالياً ويبدأ من الجديد فقط
- يتجاهل أي خبر أقدم من MAX_AGE_HOURS ساعة
- ما يستخدم Gemini أو أي AI
"""

import os
import re
import json
import html
import time
import feedparser
import requests
from pathlib import Path

from feeds import all_feeds

# ════════════════════════════════════════════════════════════════
# إعدادات (من GitHub Secrets)
# ════════════════════════════════════════════════════════════════
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID   = os.environ["TELEGRAM_CHAT_ID"]

# ════════════════════════════════════════════════════════════════
# ثوابت
# ════════════════════════════════════════════════════════════════
STATE_FILE            = "seen.json"
MAX_DESC_LEN          = 280        # حد طول الوصف
MAX_ENTRIES_PER_FEED  = 10         # كم خبر نفحص من كل مصدر
MAX_MSG_PER_RUN       = 100        # حماية من الفيضان
SEND_DELAY            = 0.8        # ثواني بين كل رسالتين
REQUEST_TIMEOUT       = 20
MAX_AGE_HOURS         = 48         # تجاهل أي خبر أقدم من هذا

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


# ════════════════════════════════════════════════════════════════
# إدارة الحالة (seen.json)
# ════════════════════════════════════════════════════════════════

def load_seen() -> set:
    """يحمّل قائمة IDs اللي شفناها سابقاً."""
    if not Path(STATE_FILE).exists():
        return set()
    try:
        data = json.loads(Path(STATE_FILE).read_text(encoding="utf-8"))
        return set(data)
    except Exception as e:
        print(f"⚠️  ما قدرت أقرأ {STATE_FILE}: {e}")
        return set()


def save_seen(seen: set) -> None:
    """يحفظ الحالة. نحتفظ بآخر 15,000 ID لمنع تضخم الملف."""
    items = list(seen)[-15000:]
    Path(STATE_FILE).write_text(
        json.dumps(items, ensure_ascii=False, indent=0),
        encoding="utf-8",
    )


# ════════════════════════════════════════════════════════════════
# معالجة المحتوى
# ════════════════════════════════════════════════════════════════

def clean_html(text: str) -> str:
    """يشيل HTML tags ويرجع نص نظيف."""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def is_recent(entry) -> bool:
    """يرجّع True لو الخبر منشور خلال آخر MAX_AGE_HOURS ساعة."""
    published = (
        entry.get("published_parsed")
        or entry.get("updated_parsed")
    )
    if not published:
        # ما في تاريخ = نعتبره غير موثوق ونتجاهله (احتياط)
        return False
    try:
        article_time = time.mktime(published)
        age_hours = (time.time() - article_time) / 3600
        return age_hours <= MAX_AGE_HOURS
    except Exception:
        return False


def get_entry_id(entry) -> str:
    """ID مستقر للخبر — نفضّل الـ link لأنه الأكثر استقراراً."""
    return entry.get("link") or entry.get("id") or entry.get("guid", "")


def format_message(feed_name: str, entry) -> str:
    """يبني رسالة تيليقرام بصيغة HTML."""
    title = clean_html(entry.get("title", "Untitled"))
    link  = entry.get("link", "")

    desc = clean_html(
        entry.get("summary")
        or entry.get("description")
        or ""
    )
    # شيل العنوان من بداية الوصف لو متكرر
    if desc.startswith(title):
        desc = desc[len(title):].lstrip(" -—:|")

    if len(desc) > MAX_DESC_LEN:
        desc = desc[:MAX_DESC_LEN].rsplit(" ", 1)[0] + "…"

    parts = [
        f"📰 <b>{html.escape(feed_name)}</b>",
        "",
        f"<b>{html.escape(title)}</b>",
    ]
    if desc:
        parts += ["", html.escape(desc)]
    parts += ["", f"🔗 {link}"]

    return "\n".join(parts)


# ════════════════════════════════════════════════════════════════
# إرسال إلى تيليقرام
# ════════════════════════════════════════════════════════════════

def send_telegram(text: str, retries: int = 2) -> bool:
    """يرسل رسالة لتيليقرام. يرجّع True لو نجح."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }

    for attempt in range(retries + 1):
        try:
            r = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
            if r.status_code == 200:
                return True
            # 429 = Too Many Requests، خذ راحة
            if r.status_code == 429:
                wait = r.json().get("parameters", {}).get("retry_after", 5)
                print(f"  ⏸  Telegram rate limit، انتظار {wait}s")
                time.sleep(wait + 1)
                continue
            print(f"  ⚠️  Telegram {r.status_code}: {r.text[:200]}")
            return False
        except Exception as e:
            print(f"  ⚠️  محاولة {attempt+1}: {type(e).__name__}: {e}")
            time.sleep(2)
    return False


# ════════════════════════════════════════════════════════════════
# الحلقة الرئيسية
# ════════════════════════════════════════════════════════════════

def main():
    seen = load_seen()
    is_first_run = len(seen) == 0

    if is_first_run:
        print("🆕 أول تشغيل — راح أسكّت كل شي حالياً وأبدأ من الجديد فقط.\n")
    else:
        print(f"📂 {len(seen)} خبر مسجّل سابقاً في seen.json\n")

    feeds = all_feeds()
    new_ids = set()
    sent_count = 0
    skipped_old = 0
    failed_feeds = []

    for i, feed in enumerate(feeds, 1):
        name = feed["name"]
        url  = feed["url"]

        try:
            d = feedparser.parse(url, agent=USER_AGENT)
            entries = d.entries[:MAX_ENTRIES_PER_FEED] if hasattr(d, "entries") else []

            if not entries:
                status = getattr(d, "status", "?")
                failed_feeds.append(f"{name} (HTTP {status})")
                print(f"[{i:3d}/{len(feeds)}] ⚠️  {name}: ما فيه أخبار")
                continue

            new_here = 0

            for entry in entries:
                # فلتر العمر — نتجاهل أي خبر أقدم من MAX_AGE_HOURS ساعة
                if not is_recent(entry):
                    skipped_old += 1
                    continue

                eid = get_entry_id(entry)
                if not eid or eid in seen or eid in new_ids:
                    continue

                if is_first_run:
                    # تسكين: نعلّمه شفناه بدون إرسال
                    new_ids.add(eid)
                    continue

                if sent_count >= MAX_MSG_PER_RUN:
                    # حماية من الفيضان — نعلّمه شفناه ولا نرسله
                    new_ids.add(eid)
                    continue

                msg = format_message(name, entry)
                if send_telegram(msg):
                    new_ids.add(eid)
                    sent_count += 1
                    new_here += 1
                    time.sleep(SEND_DELAY)

            symbol = "🆕" if new_here else "✓"
            print(f"[{i:3d}/{len(feeds)}] {symbol} {name}: {new_here} جديد")

        except Exception as e:
            failed_feeds.append(f"{name} ({type(e).__name__})")
            print(f"[{i:3d}/{len(feeds)}] ❌ {name}: {type(e).__name__}: {str(e)[:80]}")

    # حفظ الحالة
    seen.update(new_ids)
    save_seen(seen)

    # ════════ ملخص نهائي ════════
    print(f"\n{'='*60}")
    if is_first_run:
        print(f"✅ أول تشغيل خلص:")
        print(f"   • {len(new_ids)} خبر تسكّن")
        print(f"   • {skipped_old} خبر قديم تم تجاهله (أقدم من {MAX_AGE_HOURS} ساعة)")
        print(f"   • 0 رسالة أُرسلت")
        print(f"   • التشغيل الجاي راح يبدأ بإرسال الجديد")
    else:
        print(f"✅ التشغيل خلص:")
        print(f"   • {sent_count} رسالة جديدة أُرسلت")
        print(f"   • {skipped_old} خبر قديم تم تجاهله (أقدم من {MAX_AGE_HOURS} ساعة)")
        print(f"   • {len(seen)} خبر مسجّل بالمجمل")

    if failed_feeds:
        print(f"\n⚠️  {len(failed_feeds)} مصدر فشل:")
        for f in failed_feeds[:20]:
            print(f"   • {f}")
        if len(failed_feeds) > 20:
            print(f"   ... و{len(failed_feeds) - 20} غيرهم")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
