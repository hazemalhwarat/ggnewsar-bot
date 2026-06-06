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
genai.configure(api_key=GEMINI_API_KEY)
MODEL = genai.GenerativeModel("gemini-2.0-flash")

# =============== ملف تتبع الأخبار المرسلة سابقاً ===============
SEEN_FILE = "seen_articles.json"
MAX_AGE_HOURS = 24   # تجاهل الأخبار الأقدم من 24 ساعة
MAX_PER_RUN = 10     # حد أقصى للأخبار في كل تشغيلة (تجنب spam وحفظ الـ limits)


# =============== Helpers ===============
def load_seen():
    """تحميل قائمة الأخبار اللي أرسلناها سابقاً"""
    if os.path.exists(SEEN_FILE):
        try:
            with open(SEEN_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()


def save_seen(seen):
    """حفظ قائمة الأخبار المرسلة (نحتفظ بآخر 500 فقط)"""
    seen_list = list(seen)[-500:]
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(seen_list, f, ensure_ascii=False)


def make_id(entry):
    """صنع معرّف فريد لكل خبر"""
    link = entry.get("link", "")
    title = entry.get("title", "")
    return hashlib.md5(f"{link}{title}".encode("utf-8")).hexdigest()


def is_recent(entry):
    """التحقق إن الخبر حديث (آخر 24 ساعة)"""
    published = entry.get("published_parsed") or entry.get("updated_parsed")
    if not published:
        return True   # لو ما فيه تاريخ، نعتبره حديث ونرسله
    try:
        pub_date = datetime(*published[:6], tzinfo=timezone.utc)
        cutoff = datetime.now(timezone.utc) - timedelta(hours=MAX_AGE_HOURS)
        return pub_date >= cutoff
    except Exception:
        return True


def clean_html(text):
    """تنظيف HTML من النص"""
    import re
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# =============== Gemini Analysis ===============
def analyze_news(title, summary, source):
    """تحليل الخبر عبر Gemini وإرجاع حزمة جاهزة للنشر"""

    prompt = f"""أنت محرر صحفي متخصص في الرياضات الإلكترونية تكتب لحساب GGNewsAR العربي.

الخبر الأصلي (إنجليزي):
العنوان: {title}
الملخص: {summary}
المصدر: {source}

مهامك بالترتيب:
1. قيّم إذا كان الخبر يستحق النشر في GGNewsAR (يستحق إذا: نتيجة بطولة كبرى، انتقال لاعب مشهور، إعلان فريق/منظّم، خبر له ضجة). تجاهل: الإشاعات، التحديثات التقنية البسيطة، المقالات الرأيية.
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

أرجع النتيجة بصيغة JSON بهذا الشكل بالضبط (بدون أي نص قبل أو بعد):
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
    except Exception as e:
        print(f"  ❌ خطأ في تحليل Gemini: {e}")
        return None


# =============== Telegram ===============
def send_to_telegram(text):
    """إرسال رسالة للتيليقرام"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        return r.status_code == 200
    except Exception as e:
        print(f"  ❌ خطأ في إرسال تيليقرام: {e}")
        return False


def format_for_telegram(analysis, original_link, source_name):
    """تنسيق الخبر للتيليقرام كحزمة جاهزة للنسخ"""

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


# =============== Main ===============
def main():
    print(f"\n{'='*50}")
    print(f"🚀 بدء التشغيل - {datetime.now(timezone.utc).isoformat()}")
    print(f"{'='*50}\n")

    from feeds import RSS_FEEDS

    seen = load_seen()
    print(f"📚 عدد الأخبار المعالجة سابقاً: {len(seen)}")

    new_entries = []

    # 1) جمع كل الأخبار الحديثة من كل المصادر
    for feed in RSS_FEEDS:
        print(f"📡 جاري قراءة: {feed['name']}")
        try:
            parsed = feedparser.parse(feed["url"])
            for entry in parsed.entries[:5]:   # آخر 5 أخبار من كل مصدر
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

    # 2) تحديد عدد الأخبار اللي راح نعالجها هذه التشغيلة
    to_process = new_entries[:MAX_PER_RUN]
    print(f"⚙️ راح يتم معالجة {len(to_process)} خبر هذه التشغيلة\n")

    processed = 0
    published = 0
    skipped = 0

    # 3) معالجة كل خبر
    for item in to_process:
        entry = item["entry"]
        source = item["source"]
        title = entry.get("title", "")
        summary = clean_html(entry.get("summary", entry.get("description", "")))[:1500]
        link = entry.get("link", "")

        print(f"📰 معالجة: {title[:70]}...")

        # تحليل عبر Gemini
        analysis = analyze_news(title, summary, source)
        seen.add(item["id"])   # نسجّله كمعالج حتى لو فشل عشان ما نعيد المحاولة
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

        # إرسال للتيليقرام
        msg = format_for_telegram(analysis, link, source)
        if send_to_telegram(msg):
            print(f"  ✅ تم الإرسال")
            published += 1
        else:
            print(f"  ❌ فشل الإرسال")

        # فاصل زمني عشان نتجنب rate limit
        time.sleep(4)

    # 4) حفظ القائمة المحدّثة
    save_seen(seen)

    # 5) ملخص نهائي
    print(f"\n{'='*50}")
    print(f"📊 الملخص:")
    print(f"   معالج: {processed}")
    print(f"   منشور: {published}")
    print(f"   متجاهل: {skipped}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
