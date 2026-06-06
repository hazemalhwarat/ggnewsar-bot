# -*- coding: utf-8 -*-
"""
GGNewsAR Telegram Bot
يقرأ الـ RSS feeds، يحلل الأخبار عبر Gemini، ويرسل النتيجة للتيليقرام
"""

import os
import json
import time
import hashlib
import requests
import feedparser
from datetime import datetime, timedelta, timezone
import google.generativeai as genai

# =============== الإعدادات من Secrets ===============
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# =============== إعداد Gemini ===============
# نستخدم gemini-2.5-flash (Gemini 2.0 Flash توقّف يوم 1 يونيو 2026)
genai.configure(api_key=GEMINI_API_KEY)
MODEL = genai.GenerativeModel("gemini-2.5-flash")

# =============== ملف تتبع الأخبار المرسلة سابقاً ===============
SEEN_FILE = "seen_articles.json"
MAX_AGE_HOURS = 24
MAX_PER_RUN = 10


def load_seen():
    if os.path.exists(SEEN_FILE):
        try:
            with open(SEEN_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()


def save_seen(seen):
    seen_list = list(seen)[-500:]
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(seen_list, f, ensure_ascii=False)


def make_id(entry):
    link = entry.get("link", "")
    title = entry.get("title", "")
    return hashlib.md5(f"{link}{title}".encode("utf-8")).hexdigest()


def is_recent(entry):
    published = entry.get("published_parsed") or entry.get("updated_parsed")
    if not published:
        return True
    try:
        pub_date = datetime(*published[:6], tzinfo=timezone.utc)
        cutoff = datetime.now(timezone.utc) - timedelta(hours=MAX_AGE_HOURS)
        return pub_date >= cutoff
    except Exception:
        return True


def clean_html(text):
    import re
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def analyze_news(title, summary, source):
    """تحليل الخبر عبر Gemini وإرجاع حزمة جاهزة للنشر"""

    prompt = f"""أنت محرر صحفي متخصص في الرياضات الإلكترونية تكتب لحساب GGNewsAR العربي.

الخبر الأصلي (إنجليزي):
العنوان: {title}
الملخص: {summary}
المصدر: {source}

مهامك بالترتيب:

1. قيّم إذا كان الخبر يستحق النشر في GGNewsAR. كن متساهلاً وليس صارماً. يستحق النشر إذا كان:
   - نتيجة بطولة أو مباراة
   - انتقال لاعب أو تغيير في تشكيلة فريق
   - إعلان من فريق أو منظّم أو ناشر
   - تحديث مهم لبطولة قادمة (تاريخ، مكان، فرق مشاركة)
   - خبر عن لاعب مشهور
   - تحليل أو ملخص لحدث رياضي إلكتروني
   لا تتجاهل إلا: الإشاعات غير المؤكدة، المقالات الرأيية البحتة، التحديثات التقنية للعبة (patches) إذا لم تؤثر على المشهد التنافسي.

2. صنّف اللعبة والبطولة (إن وُجدت)

3. اكتب نسخة عربية بالفصحى البيضاء، بأسلوب GGNewsAR:
   - عنوان قصير يجمع الرقم الأهم + اسم اللعبة + اسم البطولة، بدون حشو
   - نص متدفّق كنثر صحفي رياضي (لا نقاط ولا أقسام)
   - جملة افتتاحية تبدأ بإيموجي واحد مقصود + نقطتين، ثم العنوان
   - هرم مقلوب (الأهم أولاً)
   - جمل قصيرة
   - نبرة حماسية محايدة بدون انحياز لأي طرف
   - إبراز الأرقام
   - المصطلحات الإنجليزية اللي تعريبها ركيك تترك بالإنجليزية
   - أسماء مشهورة مثل Valve وSteam بالإنجليزية مباشرة
   - بدون داش بين الكلمات نهائياً

4. اكتب نسخة X (تويتر) مضغوطة ضمن 280 حرف

5. اكتب كابشن انستقرام (أطول قليلاً، 3-5 أسطر)

أرجع النتيجة بصيغة JSON بهذا الشكل بالضبط (بدون أي نص قبل أو بعد، بدون backticks):
{{
  "worthy": true,
  "reason": "سبب مختصر للتقييم",
  "game": "اسم اللعبة بالإنجليزية",
  "tournament": "اسم البطولة إن وُجدت، وإلا فارغ",
  "x_post": "نسخة X كاملة جاهزة للنشر",
  "instagram_caption": "كابشن انستقرام كامل جاهز للنشر"
}}

ملاحظة: لو الخبر لا يستحق النشر، أرجع worthy=false مع reason ولا تكتب باقي الحقول."""

    try:
        response = MODEL.generate_content(prompt)
        text = response.text.strip()

        # تنظيف JSON من backticks لو الموديل حطّها
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip("` \n")

        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"  ❌ خطأ في تحليل JSON: {e}")
        print(f"     النص المُستلم: {text[:200] if 'text' in dir() else 'N/A'}")
        return None
    except Exception as e:
        print(f"  ❌ خطأ في Gemini: {e}")
        return None


def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        if r.status_code != 200:
            print(f"     Telegram error: {r.status_code} - {r.text[:200]}")
        return r.status_code == 200
    except Exception as e:
        print(f"  ❌ خطأ في إرسال تيليقرام: {e}")
        return False


def format_for_telegram(analysis, original_link, source_name):
    game = analysis.get("game", "")
    tournament = analysis.get("tournament", "")
    x_post = analysis.get("x_post", "")
    ig_caption = analysis.get("instagram_caption", "")

    msg = f"<b>🎮 GGNewsAR — خبر جديد</b>\n\n"
    msg += f"<b>🕹 اللعبة:</b> {game}\n"
    if tournament:
        msg += f"<b>🏆 البطولة:</b> {tournament}\n"
    msg += f"<b>📡 المصدر:</b> {source_name}\n"
    msg += f"<b>🔗 الرابط الأصلي:</b> {original_link}\n"
    msg += "\n" + "─" * 30 + "\n\n"
    msg += "<b>📱 نسخة X (تويتر):</b>\n"
    msg += f"<code>{x_post}</code>\n\n"
    msg += "<b>📸 كابشن انستقرام:</b>\n"
    msg += f"<code>{ig_caption}</code>"

    return msg


def main():
    print(f"\n{'='*50}")
    print(f"🚀 بدء التشغيل - {datetime.now(timezone.utc).isoformat()}")
    print(f"{'='*50}\n")

    from feeds import RSS_FEEDS

    seen = load_seen()
    print(f"📚 عدد الأخبار المعالجة سابقاً: {len(seen)}")

    new_entries = []

    for feed in RSS_FEEDS:
        print(f"📡 جاري قراءة: {feed['name']}")
        try:
            parsed = feedparser.parse(feed["url"])
            for entry in parsed.entries[:5]:
                entry_id = make_id(entry)
                if entry_id in seen:
                    continue
                if not is_recent(entry):
                    continue
                new_entries.append({
                    "id": entry_id,
                    "entry": entry,
                    "source": feed["name"],
                })
        except Exception as e:
            print(f"  ⚠️ فشل: {e}")
            continue

    print(f"\n🆕 عدد الأخبار الجديدة: {len(new_entries)}")

    if not new_entries:
        print("✨ لا توجد أخبار جديدة. انتهى التشغيل.")
        save_seen(seen)
        return

    to_process = new_entries[:MAX_PER_RUN]
    print(f"⚙️ راح يتم معالجة {len(to_process)} خبر هذه التشغيلة\n")

    processed = 0
    published = 0
    skipped = 0

    for item in to_process:
        entry = item["entry"]
        source = item["source"]
        title = entry.get("title", "")
        summary = clean_html(entry.get("summary", entry.get("description", "")))[:1500]
        link = entry.get("link", "")

        print(f"📰 معالجة: {title[:70]}...")

        analysis = analyze_news(title, summary, source)
        seen.add(item["id"])
        processed += 1

        if not analysis:
            print(f"  ⏭ تجاهل (فشل التحليل)")
            skipped += 1
            time.sleep(4)
            continue

        if not analysis.get("worthy"):
            print(f"  ⏭ تجاهل: {analysis.get('reason', 'غير مستحق')}")
            skipped += 1
            time.sleep(4)
            continue

        msg = format_for_telegram(analysis, link, source)
        if send_to_telegram(msg):
            print(f"  ✅ تم الإرسال")
            published += 1
        else:
            print(f"  ❌ فشل الإرسال")

        time.sleep(4)

    save_seen(seen)

    print(f"\n{'='*50}")
    print(f"📊 الملخص:")
    print(f"   معالج: {processed}")
    print(f"   منشور: {published}")
    print(f"   متجاهل: {skipped}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
