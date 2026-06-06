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
MODEL = genai.GenerativeModel("gemini-2.5-flash-lite")

# =============== إعدادات التشغيل ===============
SEEN_FILE = "seen_articles.json"
MAX_AGE_HOURS = 24
MAX_PER_RUN = 8


def load_seen():
    if os.path.exists(SEEN_FILE):
        try:
            with open(SEEN_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()


def save_seen(seen):
    seen_list = list(seen)[-1000:]
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
    """تحليل الخبر عبر Gemini وإرجاع حزمة جاهزة للنشر بأسلوب GGNewsAR"""

    prompt = f"""أنت محرر صحفي رياضي إلكتروني عربي محترف، تكتب حصرياً لحساب GGNewsAR.
مهمتك تحويل خبر إنجليزي إلى محتوى عربي بأسلوب GGNewsAR الحصري.

# قواعد البصمة (مطلقة):

1. عربية فصحى بيضاء فقط. ممنوع منعاً باتاً اللهجة الخليجية أو العامية.
2. الافتتاحية تبدأ بإيموجي واحد مقصود ثم نقطتين، ثم العنوان الخاطف مباشرة.
3. هيكل النص: نثر صحفي متدفّق متماسك. ممنوع: النقاط، الأقسام، رؤوس فرعية، فواصل سطور كثيرة.
4. الجمل قصيرة ومكثّفة. لا حشو ولا تكرار. كل كلمة تخدم المعنى.
5. الهرم المقلوب: الخبر الأهم في الجملة الأولى، ثم الأرقام والتفاصيل، ثم السياق.
6. الأرقام تُبرز بوضوح (3-1، مليون دولار، الفوز الثاني على التوالي).
7. النبرة: حماسية محايدة. ممنوع التحيّز لأي فريق أو لاعب.
8. أسماء مشهورة بالإنجليزية مباشرة: Valve, Steam, FaZe, ESL, EWC, Falcons، إلخ.
9. مصطلحات تقنية إذا كان تعريبها ركيكاً، تُترك بالإنجليزية.
10. ممنوع: علامة الداش ( - ) بين الكلمات نهائياً.
11. ممنوع: تبدأ بـ"أعلن" أو "كشف" بشكل تقليدي. ابدأ بالحدث/الأثر مباشرة.

# أمثلة من بصمة GGNewsAR الفعلية (قلّد هذه النبرة بالضبط):

مثال 1 (نتيجة بطولة):
💥 ثلاثية تاريخية للفلكنز: Team Falcons يحسم نهائي EWC للمرة الثالثة على التوالي، بعد تغلّبه على The MongolZ بنتيجة 3-1 في ملحمة استمرت ساعتين، ليرفع رصيده من جوائز الموسم إلى ما يتجاوز مليون دولار.

مثال 2 (مفاجأة):
🔥 صدمة في Champions Tour: Sentinels يُقصى من ربع نهائي Paris على يد NRG بنتيجة 2-0، رغم تواجد TenZ في تشكيلة جديدة، في واحدة من أكبر مفاجآت موسم Valorant 2026.

مثال 3 (انتقال):
⚡ صفقة العام في R6: Team Falcons يضم اللاعب البرازيلي Soulz1 قادماً من w7m، ضمن إعادة هيكلة شاملة للتشكيلة قبل انطلاق موسم Six Invitational 2027.

مثال 4 (إعلان بطولة):
🏆 ESL تكشف عن جوائز IEM Cologne 2026: إجمالي مليون دولار، بزيادة 25% عن نسخة العام الماضي، مع تأهّل مباشر للبطل إلى Major الختامي.

# الخبر المطلوب معالجته:

العنوان: {title}
الملخص: {summary}
المصدر: {source}

# مهامك:

1. قيّم إذا كان الخبر يستحق النشر:
   ⚠️ السياسة: متساهل جداً. الافتراض الأساسي أن الخبر يستحق النشر.
   
   ✅ يستحق النشر (worthy = true) في كل الحالات تقريباً، ومن ضمنها:
   - أي نتيجة مباراة أو بطولة (حتى لو ليست كبرى)
   - أي انتقال لاعب أو تغيير في تشكيلة فريق
   - أي إعلان من فريق أو منظّم أو ناشر
   - أي خبر عن بطولة (تاريخ، فرق مشاركة، جوائز، مكان)
   - تحليلات وملخصات الأحداث الرياضية الإلكترونية
   - أخبار اللاعبين (إصابات، عودة، تصريحات)
   - تحديثات اللعبة إذا كان لها أي علاقة بالمشهد التنافسي
   - الأرقام القياسية والإحصائيات
   - الخلافات والقضايا التي تخص الفرق أو اللاعبين
   - رعاية تجارية أو شراكات
   
   ❌ لا يستحق النشر (worthy = false) فقط في هذه الحالات الواضحة:
   - الخبر لا علاقة له بالرياضات الإلكترونية إطلاقاً
   - الخبر مجرد إشاعة مصدرها مجهول تماماً
   - الخبر تقني بحت عن لعبة غير تنافسية
   - الخبر مقال رأي صرف بدون أي معلومات جديدة
   - دليل لعب أو نصائح لاعبين عاديين (guides, tips, tutorials)
   
   🎯 في حالة الشك، اعتبر الخبر يستحق النشر. حازم يفضّل يرى أكثر ويقرر بنفسه.

2. صنّف اللعبة والبطولة (إن وُجدت).

3. اكتب نسخة X (تويتر) ضمن 280 حرف، بأسلوب الأمثلة السابقة تماماً. تبدأ بإيموجي + نقطتين، تكون مكثّفة جداً، فيها الرقم الأهم والاسم الأهم.

4. اكتب كابشن انستقرام: 3-5 جمل، نفس أسلوب الأمثلة، لكن مع شرح أعمق قليلاً. ابدأ بإيموجي + نقطتين، اختم بجملة قوية إن كانت طبيعية.

# الإخراج (JSON فقط، بدون أي نص خارجه، بدون backticks):

{{
  "worthy": true,
  "reason": "سبب مختصر",
  "game": "اسم اللعبة بالإنجليزية",
  "tournament": "اسم البطولة إن وُجدت، وإلا فارغ",
  "x_post": "نسخة X كاملة بأسلوب الأمثلة",
  "instagram_caption": "كابشن انستقرام كامل بأسلوب الأمثلة"
}}

إذا الخبر لا يستحق، أرجع worthy=false مع reason فقط."""

    try:
        response = MODEL.generate_content(prompt)
        text = response.text.strip()

        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip("` \n")

        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"  ❌ خطأ في تحليل JSON: {e}")
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
    print(f"📊 عدد المصادر: {len(RSS_FEEDS)}\n")

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
            time.sleep(15)
            continue

        if not analysis.get("worthy"):
            print(f"  ⏭ تجاهل: {analysis.get('reason', 'غير مستحق')}")
            skipped += 1
            time.sleep(15)
            continue

        msg = format_for_telegram(analysis, link, source)
        if send_to_telegram(msg):
            print(f"  ✅ تم الإرسال")
            published += 1
        else:
            print(f"  ❌ فشل الإرسال")

        time.sleep(15)

    save_seen(seen)

    print(f"\n{'='*50}")
    print(f"📊 الملخص:")
    print(f"   معالج: {processed}")
    print(f"   منشور: {published}")
    print(f"   متجاهل: {skipped}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
