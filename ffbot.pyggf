import os
import json
import time
import logging
import urllib.parse
import urllib.request
import urllib.error

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("al-ezz-bot")

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"].strip()
TRENDAWE_API_KEY = os.getenv("TRENDAWE_API_KEY", os.getenv("SMMGEN_API_KEY", "")).strip()
TRENDAWE_API_URL = os.getenv("TRENDAWE_API_URL", os.getenv("SMMGEN_API_URL", "https://trendawe.com/api/v2")).strip()
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Services extracted from the user's Trendawe channel CSV.
SERVICES = [
  {
    "id": "5912",
    "description": "Instagram Comments | Max 1M | Custom | Real Mixed | 50k /Days | Instant | No Refill ⚠️ 🚀",
    "price": "0.54"
  },
  {
    "id": "5913",
    "description": "Instagram Comments | Max 1M | Random | Real Mixed | 50k /Days | Instant | No Refill ⚠️ 🚀",
    "price": "0.54"
  },
  {
    "id": "5914",
    "description": "Instagram Comments | Max 1M | Emoji | Real Mixed | 50k /Days | Instant | No Refill ⚠️ 🚀",
    "price": "0.36"
  },
  {
    "id": "5911",
    "description": "Instagram Repost | Max 10M | Real Mixed Accounts | 200K /Days | Instant | No Refill ⚠️ 🚀",
    "price": "0.3673"
  },
  {
    "id": "5910",
    "description": "Instagram Saves | Max 10M | 200K /Days | Instant | No Refill ⚠️ 🚀",
    "price": "0.049"
  },
  {
    "id": "5915",
    "description": "لايكات انستقرام | حسابات حقيقي | 100 ألف / يوم | فوري | الضمان: بدون تعويض ⚠️ 🚀",
    "price": "0.025"
  },
  {
    "id": "5916",
    "description": "واتساب سيندر لارسال حملات واتساب | إصدار 6.1.35 | رخصة واحدة لجهاز واحد | اشتراك 365 يوم | [الضمان: 365 يوم] ♻️ 🚀",
    "price": "3.00"
  },
  {
    "id": "5917",
    "description": "واتساب سيندر لارسال حملات واتساب | إصدار 6.1.35 | رخصة واحدة لجهاز واحد | اشتراك مدى الحياة | [الضمان: مدى الحياة] ♻️ 🚀",
    "price": "10.00"
  },
  {
    "id": "481",
    "description": "Discord Server Members | Offline | High Quality | Instant | 100/Day | 30 Days Refill ♻️ ❗️",
    "price": "1.4929"
  },
  {
    "id": "5918",
    "description": "تعليقات فيسبوك | عشوائي | حسابات مخفية | الحد الأقصى 10 ألف | 10 ألف/يوم | فوري | الضمان: بدون تعويض ⚠️ 🚀",
    "price": "1.2034"
  },
  {
    "id": "5919",
    "description": "تعليق فيسبوك | مخصص | حسابات مكررة وتعليقات مخفية | 10 ألف/يوم | فوري | الضمان: بدون تعويض ⚠️ 🚀",
    "price": "1.5697"
  },
  {
    "id": "5920",
    "description": "تعليق فيسبوك | إيموجي | حسابات مكررة وتعليقات مخفية | 10 ألف/يوم | فوري | الضمان: بدون تعويض ⚠️ 🚀",
    "price": "1.5697"
  },
  {
    "id": "5921",
    "description": "تعليقات فيسبوك | مخصص | عالمي | الحد الأدنى 5 | 5 ألف/يوم | فوري | الضمان: بدون تعويض ⚠️ 🚀",
    "price": "1.914"
  },
  {
    "id": "5922",
    "description": "تعليقات فيسبوك | مخصص | عالمي | الحد الأدنى 10 | 5 ألف/يوم | فوري | الضمان: بدون تعويض ⚠️ 🚀",
    "price": "2.1828"
  },
  {
    "id": "5923",
    "description": "تعليقات فيسبوك | مخصص | عالمي | الحد الأدنى 10 | 20 ألف/يوم | فوري | الضمان: بدون تعويض ⚠️ 🚀",
    "price": "2.2489"
  },
  {
    "id": "5780",
    "description": "متابعين تيك توك | جودة عالية | سريعة | فوري | [الضمان: 10 يوم] ♻️ 🚀",
    "price": "1.1125"
  },
  {
    "id": "4100",
    "description": "أعضاء / متابعين قناة واتساب | جودة حقيقية | الهند 🇮🇳 | سرعة فائقة 100 ألف في اليوم | بدون نقص | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.4063"
  },
  {
    "id": "2591",
    "description": "أعضاء / متابعين قناة واتساب | جودة حقيقية | عربي 🇦🇪 | سرعة فائقة 100 ألف في اليوم | بدون نقص | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.4063"
  },
  {
    "id": "2592",
    "description": "أعضاء / متابعين قناة واتساب | جودة حقيقية | تركيا 🇹🇷 | سرعة فائقة 100 ألف في اليوم | بدون نقص | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.4063"
  },
  {
    "id": "4392",
    "description": "أعضاء / متابعين قناة واتساب | جودة حقيقية | أمريكا 🇺🇸 | سرعة فائقة 100 ألف في اليوم | بدون نقص | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.4063"
  },
  {
    "id": "1129",
    "description": "أعضاء / متابعين قناة واتساب | جودة حقيقية | أوروبا 🇪🇺 | سرعة فائقة 100 ألف في اليوم | بدون نقص | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.4063"
  },
  {
    "id": "2411",
    "description": "أعضاء / متابعين قناة واتساب | جودة حقيقية | البرازيل 🇧🇷 | سرعة فائقة 100 ألف في اليوم | بدون نقص | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.4063"
  },
  {
    "id": "2413",
    "description": "أعضاء / متابعين قناة واتساب | جودة حقيقية | باكستان 🇵🇰 | سرعة فائقة 100 ألف في اليوم | بدون نقص | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.4063"
  },
  {
    "id": "3209",
    "description": "أعضاء / متابعين قناة واتساب | جودة حقيقية | الفلبين 🇵🇭 | سرعة فائقة 100 ألف في اليوم | بدون نقص | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.4063"
  },
  {
    "id": "3487",
    "description": "أعضاء / متابعين قناة واتساب | جودة حقيقية | تايلاند 🇹🇭 | سرعة فائقة 100 ألف في اليوم | بدون نقص | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.4063"
  },
  {
    "id": "1474",
    "description": "أعضاء / متابعين قناة واتساب | جودة حقيقية | نيجيريا 🇳🇬 | سرعة فائقة 100 ألف في اليوم | بدون نقص | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.4063"
  },
  {
    "id": "4726",
    "description": "متابعين فيسبوك | الحد الأقصى 30 ألف | كل الأنواع بروفايل / صفحات | داتا بوت | 20 ألف في اليوم ~ فوري ~ | الضمان: بدون تعويض ⚠️ 🚀",
    "price": "0.1213"
  },
  {
    "id": "4940",
    "description": "متابعين فيسبوك | الحد الأقصى 30 ألف | كل الأنواع بروفايل / صفحات | داتا بوت | 20 ألف في اليوم ~ فوري ~ | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.1347"
  },
  {
    "id": "4938",
    "description": "متابعين فيسبوك | الحد الأقصى 30 ألف | كل الأنواع بروفايل / صفحات | داتا بوت | 20 ألف في اليوم ~ فوري ~ | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.1282"
  },
  {
    "id": "5924",
    "description": "متابعين فيسبوك مصريين 100% 🎯 | بروفايل + صفحة | 💥 السرعة 10 ألف في اليوم | [الضمان: مدى الحياة] ♻️ 🚀",
    "price": "1.1185"
  },
  {
    "id": "4725",
    "description": "متابعين فيسبوك | الحد الأقصى 30 ألف | كل الأنواع بروفايل / صفحات | داتا بوت | 20 ألف في اليوم ~ فوري ~ | الضمان: بدون تعويض ⚠️ 🚀",
    "price": "0.118"
  },
  {
    "id": "5925",
    "description": "Instagram Shares - [ 𝗦𝘂𝗽𝗲𝗿 𝗙𝗮𝘀𝘁 ]",
    "price": "0.0005"
  },
  {
    "id": "5926",
    "description": "Instagram Story Shares - [ 𝗦𝘂𝗽𝗲𝗿 𝗙𝗮𝘀𝘁 ]",
    "price": "0.0275"
  },
  {
    "id": "5927",
    "description": "🇮🇷 Instagram Shares - [ IRAN ] 🇮🇷",
    "price": "0.0825"
  },
  {
    "id": "5928",
    "description": "🇮🇳 Instagram Shares - [ INDIA ] 🇮🇳",
    "price": "0.0825"
  },
  {
    "id": "5929",
    "description": "🇹🇷 Instagram Shares - [ TURKEY ] 🇹🇷",
    "price": "0.0825"
  },
  {
    "id": "5930",
    "description": "🇷🇺 Instagram Shares - [ RUSSIA ] 🇷🇺",
    "price": "0.0825"
  },
  {
    "id": "5931",
    "description": "🇧🇷 Instagram Shares - [ BRAZIL ] 🇧🇷",
    "price": "0.0825"
  },
  {
    "id": "5932",
    "description": "🇪🇸 Instagram Shares - [ SPAIN ] 🇪🇸",
    "price": "0.0825"
  },
  {
    "id": "5933",
    "description": "🇸🇦 Instagram Shares - [ SAUDI ARABIA ] 🇸🇦",
    "price": "0.0825"
  },
  {
    "id": "5934",
    "description": "🇺🇸 Instagram Shares - [ UNITED STATE ] 🇺🇸",
    "price": "0.0825"
  },
  {
    "id": "5935",
    "description": "🇨🇳 Instagram Shares - [ CHINA ] 🇨🇳",
    "price": "0.0825"
  },
  {
    "id": "5936",
    "description": "🇮🇹 Instagram Shares - [ ITALY ] 🇮🇹",
    "price": "0.0825"
  },
  {
    "id": "5937",
    "description": "🇩🇪 Instagram Shares - [ GERMANY ] 🇩🇪",
    "price": "0.0825"
  },
  {
    "id": "5938",
    "description": "🇫🇷 Instagram Shares - [ FRANCE ] 🇫🇷",
    "price": "0.0825"
  },
  {
    "id": "5939",
    "description": "🇮🇩 Instagram Shares - [ INDONESIA ] 🇮🇩",
    "price": "0.0825"
  },
  {
    "id": "5942",
    "description": "YouTube Subscribers | Country/Quality: Jordan JO 🇯🇴 | Start Time: Within 24 Hours | Speed: Up to 1-5K /Days | 30 Days Refill ♻️ 🚀",
    "price": "35.2373"
  },
  {
    "id": "5943",
    "description": "YouTube Subscribers | Country/Quality: Libya LY 🇱🇾 | Start Time: Within 24 Hours | Speed: Up to 1-5K /Days | 30 Days Refill ♻️ 🚀",
    "price": "35.2373"
  },
  {
    "id": "5944",
    "description": "YouTube Subscribers | Country/Quality: Syria SY 🇸🇾 | Start Time: Within 24 Hours | Speed: Up to 1-5K /Days | 30 Days Refill ♻️ 🚀",
    "price": "35.2373"
  },
  {
    "id": "5945",
    "description": "YouTube Subscribers | Country/Quality: Yemen YE 🇾🇪 | Start Time: Within 24 Hours | Speed: Up to 1-5K /Days | 30 Days Refill ♻️ 🚀",
    "price": "35.2373"
  },
  {
    "id": "5946",
    "description": "YouTube Subscribers | Country/Quality: Kuwait KW 🇰🇼 | Start Time: Within 24 Hours | Speed: Up to 1-5K /Days | 30 Days Refill ♻️ 🚀",
    "price": "35.2373"
  },
  {
    "id": "5947",
    "description": "YouTube Subscribers | Country/Quality: Qatar QA 🇶🇦 | Start Time: Within 24 Hours | Speed: Up to 1-5K /Days | 30 Days Refill ♻️ 🚀",
    "price": "35.2373"
  },
  {
    "id": "5940",
    "description": "Facebook Post Shares | [Hidden] | Posts Only | 💥 Speed: 20K /Days | Lifetime Refill ♻️",
    "price": "0.2059"
  },
  {
    "id": "5941",
    "description": "Facebook Post Shares | [Hidden] | Posts + Videos | 💥 Speed: 20K /Days | Lifetime Refill ♻️",
    "price": "0.4117"
  },
  {
    "id": "5948",
    "description": "Gemini Pro Subscription | 18 Months | No Refill ⚠️ 🚀",
    "price": "4.00"
  },
  {
    "id": "5791",
    "description": "Facebook Followers | Page / Profile | 🎯 100 Pages 💯 | Speed: +10K /Days | 30 Days Refill ♻️ 🚀",
    "price": "2.0143"
  },
  {
    "id": "5792",
    "description": "Facebook Followers Egyptian 🎯 | Profile / Pages | 30 Days Refill ♻️ 🚀",
    "price": "2.1816"
  },
  {
    "id": "5654",
    "description": "TikTok Followers | Arabs & Egyptians SA EG | 100% Active Accounts | Sponsored Ads | No Refill ⛔ ⚠️ 🚀",
    "price": "3.3608"
  },
  {
    "id": "5655",
    "description": "TikTok Followers | Arabs & Egyptians SA EG | 100% Active Accounts | Sponsored Ads | 30 Days Refill ♻️ 🚀",
    "price": "3.5269"
  },
  {
    "id": "5656",
    "description": "TikTok Followers | Arabs & Egyptians SA EG | 100% Active Accounts | Sponsored Ads | 60 Days Refill ♻️ 🚀",
    "price": "3.6166"
  },
  {
    "id": "5657",
    "description": "TikTok Followers | Arabs & Egyptians SA EG | 100% Active Accounts | Sponsored Ads | 90 Days Refill ♻️ 🚀",
    "price": "3.7063"
  },
  {
    "id": "5949",
    "description": "Pack 5K Facebook Followers Egyptian 🎯 | Non Drop 🔥 | Speed 1000/5000 /Days | Lifetime Refill ♻️ 🚀",
    "price": "1.334"
  },
  {
    "id": "5950",
    "description": "Pack 10K Facebook Followers | 100% Egyptian Pages 🎯 | Profile+Page | 💥 Speed 50K /Days | Lifetime Refill ♻️ 🚀",
    "price": "1.2314"
  },
  {
    "id": "4879",
    "description": "Facebook Followers | Page Likes + Followers | Real Accounts | Low Drop | Instant Speed | Lifetime Refill ♻️ 🚀",
    "price": "0.35"
  },
  {
    "id": "4244",
    "description": "YouTube WatchTime [100 - 4000 hours] | SLOW | 30 Days Refill ♻️ 🚀",
    "price": "17.50"
  },
  {
    "id": "4243",
    "description": "YouTube WatchTime [4000 hours] | 30 Days Refill ♻️ 🚀",
    "price": "18.75"
  },
  {
    "id": "4242",
    "description": "YouTube WatchTime [2000 hours] | 30 Days Refill ♻️ 🚀",
    "price": "22.50"
  },
  {
    "id": "2632",
    "description": "YouTube Views | Speed 2000-4000 per day | No Refill ⚠️ 🔴 🚀",
    "price": "0.40"
  },
  {
    "id": "2633",
    "description": "YouTube Views | 👤 Real | Speed 10K /Days | 30 Days Refill ♻️ ⚡ 🚀",
    "price": "0.80"
  },
  {
    "id": "2224",
    "description": "YouTube Views | 5K-10K /Days | Non Drop | Lifetime Refill ♻️ 🔮 🏆 🚀",
    "price": "0.85"
  },
  {
    "id": "2634",
    "description": "YouTube Views | Min: 10 | Non Drop | Speed: 3K/Day | Lifetime Refill ♻️ 🍿 🚀",
    "price": "0.875"
  },
  {
    "id": "5951",
    "description": "Facebook Followers [ All Types ] [ Max 1M ] | Hidden Profiles | Low Drop | No Refill ⚠️ | Instant Start | 25K /Days 🚀",
    "price": "0.125"
  },
  {
    "id": "5952",
    "description": "Facebook Followers [ All Types ] [ Max 1M ] | Hidden Profiles | Low Drop | 30 Days Refill ♻️ | Instant Start | 25K /Days 🚀",
    "price": "0.1313"
  },
  {
    "id": "5953",
    "description": "Facebook Followers [ All Types ] [ Max 1M ] | Hidden Profiles | Low Drop | 60 Days Refill ♻️ | Instant Start | 25K /Days 🚀",
    "price": "0.1338"
  },
  {
    "id": "5954",
    "description": "Facebook Followers [ All Types ] [ Max 1M ] | Hidden Profiles | Low Drop | 90 Days Refill ♻️ | Instant Start | 25K /Days 🚀",
    "price": "0.1375"
  },
  {
    "id": "5955",
    "description": "Facebook Followers [ All Types ] [ Max 1M ] | Hidden Profiles | Low Drop | 365 Days Refill ♻️ | Instant Start | 25K /Days 🚀",
    "price": "0.14"
  },
  {
    "id": "5956",
    "description": "Facebook Followers [ All Types ] [ Max 1M ] | Hidden Profiles | Low Drop | Lifetime Refill ♻️ | Instant Start | 25K /Days 🚀",
    "price": "0.1425"
  },
  {
    "id": "4900",
    "description": "Facebook Post Likes | Hidden Accounts | 5K /Days | Likes 👍 | No Refill ⚠️ 🚀",
    "price": "0.2113"
  },
  {
    "id": "5226",
    "description": "Facebook Post Reaction | Hidden Accounts | 5K /Days | Love 💖 | No Refill ⚠️ 🚀",
    "price": "0.2113"
  },
  {
    "id": "5464",
    "description": "Facebook Post Reaction | Hidden Accounts | 5K /Days | Wow 😲 | No Refill ⚠️ 🚀",
    "price": "0.2113"
  },
  {
    "id": "5228",
    "description": "Facebook Post Reaction | Hidden Accounts | 5K /Days | Haha 😂 | No Refill ⚠️ 🚀",
    "price": "0.2113"
  },
  {
    "id": "5227",
    "description": "Facebook Post Reaction | Hidden Accounts | 5K /Days | Sad 😭 | No Refill ⚠️ 🚀",
    "price": "0.2113"
  },
  {
    "id": "5229",
    "description": "Facebook Post Reaction | Hidden Accounts | 5K /Days | Angry 😡 | No Refill ⚠️ 🚀",
    "price": "0.2113"
  },
  {
    "id": "4899",
    "description": "Facebook Post React | Arab | Angry 🤬 | Non Drop | +500/Day | Lifetime Refill 🔥 🚀",
    "price": "2.235"
  },
  {
    "id": "4901",
    "description": "Facebook Post React | Arab | Mix React 👍 ❤️ 🥰 | +500/Day | Lifetime Refill 🔥 🚀",
    "price": "2.235"
  },
  {
    "id": "5957",
    "description": "TikTok Views | HQ | Fast | Instant | No Refill ⚠️ 🚀",
    "price": "0.003"
  },
  {
    "id": "5958",
    "description": "TikTok Views | HQ | Fast | Instant | 30 Days Refill ♻️ 🚀",
    "price": "0.0039"
  },
  {
    "id": "5784",
    "description": "YouTube Like | Max 5k | 5k /Days | Instant | No Refill ⚠️ 🚀",
    "price": "0.2448"
  },
  {
    "id": "5960",
    "description": "Facebook Followers 100% Egyptian 🎯 | Profile + Page | 💥 Speed: 10K /Days | Lifetime Refill ♻️ 🚀",
    "price": "0.673"
  },
  {
    "id": "5959",
    "description": "Facebook Followers 100% Egyptian 🎯 | Profile + Page | 💥 Speed: 10K /Days | 30 Days Refill ♻️ 🚀",
    "price": "0.7408"
  }
]
SERVICE_BY_ID = {s["id"]: s for s in SERVICES}
sessions = {}


def post_form(url, data, timeout=60):
    body = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(url, data=body, method="POST")
    request.add_header("Content-Type", "application/x-www-form-urlencoded")
    request.add_header("User-Agent", "AlEzzMediaBot/1.0")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail[:250]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from exc


def telegram(method, data):
    result = post_form(f"{TELEGRAM_API}/{method}", data)
    if not result.get("ok", False):
        raise RuntimeError(f"Telegram API error: {result}")
    return result


def send(chat_id, text):
    telegram("sendMessage", {"chat_id": str(chat_id), "text": text})


def send_service_page(chat_id, page=0):
    page_size = 10
    start = page * page_size
    items = SERVICES[start:start + page_size]
    if not items:
        send(chat_id, "لا توجد صفحة خدمات بهذا الرقم.")
        return
    lines = [f"الخدمات (صفحة {page + 1}/{(len(SERVICES) + page_size - 1) // page_size}):"]
    for s in items:
        lines.append(f"{s['id']} — {s['description']} — {s['price']}$ / 1000")
    lines.append("\nأرسل رقم Service ID لاختيار الخدمة، أو /services 2 للصفحة التالية.")
    send(chat_id, "\n".join(lines))


def start_message(chat_id):
    sessions[chat_id] = {"step": "service"}
    send(chat_id, "أهلًا بك في @AlEzzMediaBot.\n\nأرسل /services لرؤية الخدمات.\nثم أرسل رقم Service ID للخدمة المطلوبة.\n\nأرسل /cancel للإلغاء.")


def handle_message(message):
    chat_id = message.get("chat", {}).get("id")
    text = (message.get("text") or "").strip()
    if chat_id is None:
        return
    if text in ("/start", "/help"):
        start_message(chat_id); return
    if text == "/cancel":
        sessions.pop(chat_id, None); send(chat_id, "تم إلغاء العملية."); return
    if text.startswith("/services"):
        parts=text.split(); page=int(parts[1])-1 if len(parts)>1 and parts[1].isdigit() else 0
        send_service_page(chat_id, max(0,page)); return
    session = sessions.get(chat_id)
    if not session:
        send(chat_id, "أرسل /start للبدء."); return
    if session["step"] == "service":
        service=SERVICE_BY_ID.get(text)
        if not service:
            send(chat_id, "رقم الخدمة غير موجود. أرسل /services لرؤية القائمة."); return
        session.update(service=service["id"], description=service["description"], step="link")
        send(chat_id, f"اخترت الخدمة: {service['description']}\nأرسل الرابط المطلوب."); return
    if session["step"] == "link":
        if not text.startswith(("http://", "https://")):
            send(chat_id, "أرسل رابطًا صحيحًا يبدأ بـ http:// أو https://"); return
        session.update(link=text, step="quantity")
        send(chat_id, "أرسل الكمية المطلوبة بالأرقام."); return
    if session["step"] == "quantity":
        try:
            quantity=int(text)
            if not 1 <= quantity <= 1_000_000: raise ValueError
        except ValueError:
            send(chat_id, "أرسل كمية صحيحة بين 1 و 1,000,000."); return
        send(chat_id, "جارٍ إرسال الطلب، انتظر قليلًا...")
        try:
            result=post_form(TRENDAWE_API_URL, {"key":TRENDAWE_API_KEY,"action":"add","service":session["service"],"link":session["link"],"quantity":str(quantity)})
            if result.get("order"):
                send(chat_id, f"تم استلام الطلب بنجاح.\nرقم الطلب: {result['order']}")
            else:
                send(chat_id, "لم يتم إنشاء الطلب:\n" + str(result.get("error", result)))
        except Exception:
            log.exception("Trendawe request failed")
            send(chat_id, "تعذر الاتصال بمنصة الطلبات. تأكد من مفتاح ترنداوي ورابط API.")
        finally:
            sessions.pop(chat_id, None)


def main():
    offset=0
    log.info("Bot started with %s services", len(SERVICES))
    while True:
        try:
            result=post_form(f"{TELEGRAM_API}/getUpdates", {"offset":str(offset),"timeout":"50","allowed_updates":json.dumps(["message"])}, timeout=65)
            for update in result.get("result", []):
                offset=update["update_id"]+1
                if update.get("message"):
                    try: handle_message(update["message"])
                    except Exception: log.exception("Message handling failed")
        except Exception:
            log.exception("Polling failed"); time.sleep(5)


if __name__ == "__main__":
    main()
