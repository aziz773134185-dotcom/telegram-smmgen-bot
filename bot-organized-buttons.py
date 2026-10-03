import os, json, time, logging, urllib.parse, urllib.request, urllib.error
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log=logging.getLogger("al-ezz-bot")
BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN", "").strip(); API_KEY=os.getenv("TRENDAWE_API_KEY", "").strip(); API_URL=os.getenv("TRENDAWE_API_URL", "https://trendawe.com/api/v2").strip()
if not BOT_TOKEN: raise RuntimeError("Missing Railway Variable: TELEGRAM_BOT_TOKEN")
if not API_KEY: raise RuntimeError("Missing Railway Variable: TRENDAWE_API_KEY")
TG=f"https://api.telegram.org/bot{BOT_TOKEN}"
SERVICES=[
  {
    "id": "5912",
    "platform": "Instagram",
    "category": "Comments",
    "description": "Instagram Comments | Max 1M | Custom | Real Mixed | 50k /Days | Instant | No Refill ⚠️ 🚀",
    "price": "0.54"
  },
  {
    "id": "5913",
    "platform": "Instagram",
    "category": "Comments",
    "description": "Instagram Comments | Max 1M | Random | Real Mixed | 50k /Days | Instant | No Refill ⚠️ 🚀",
    "price": "0.54"
  },
  {
    "id": "5914",
    "platform": "Instagram",
    "category": "Comments",
    "description": "Instagram Comments | Max 1M | Emoji | Real Mixed | 50k /Days | Instant | No Refill ⚠️ 🚀",
    "price": "0.36"
  },
  {
    "id": "5911",
    "platform": "Instagram",
    "category": "Shares / Reposts",
    "description": "Instagram Repost | Max 10M | Real Mixed Accounts | 200K /Days | Instant | No Refill ⚠️ 🚀",
    "price": "0.3673"
  },
  {
    "id": "5910",
    "platform": "Instagram",
    "category": "Other Services",
    "description": "Instagram Saves | Max 10M | 200K /Days | Instant | No Refill ⚠️ 🚀",
    "price": "0.049"
  },
  {
    "id": "5915",
    "platform": "Instagram",
    "category": "Likes / Reactions",
    "description": "لايكات انستقرام | حسابات حقيقي | 100 ألف / يوم | فوري | الضمان: بدون تعويض ⚠️ 🚀",
    "price": "0.025"
  },
  {
    "id": "5916",
    "platform": "WhatsApp",
    "category": "Subscriptions / Tools",
    "description": "واتساب سيندر لارسال حملات واتساب | إصدار 6.1.35 | رخصة واحدة لجهاز واحد | اشتراك 365 يوم | [الضمان: 365 يوم] ♻️ 🚀",
    "price": "3.00"
  },
  {
    "id": "5917",
    "platform": "WhatsApp",
    "category": "Subscriptions / Tools",
    "description": "واتساب سيندر لارسال حملات واتساب | إصدار 6.1.35 | رخصة واحدة لجهاز واحد | اشتراك مدى الحياة | [الضمان: مدى الحياة] ♻️ 🚀",
    "price": "10.00"
  },
  {
    "id": "481",
    "platform": "Discord",
    "category": "Followers / Members",
    "description": "Discord Server Members | Offline | High Quality | Instant | 100/Day | 30 Days Refill ♻️ ❗️",
    "price": "1.4929"
  },
  {
    "id": "5918",
    "platform": "Facebook",
    "category": "Comments",
    "description": "تعليقات فيسبوك | عشوائي | حسابات مخفية | الحد الأقصى 10 ألف | 10 ألف/يوم | فوري | الضمان: بدون تعويض ⚠️ 🚀",
    "price": "1.2034"
  },
  {
    "id": "5919",
    "platform": "Facebook",
    "category": "Comments",
    "description": "تعليق فيسبوك | مخصص | حسابات مكررة وتعليقات مخفية | 10 ألف/يوم | فوري | الضمان: بدون تعويض ⚠️ 🚀",
    "price": "1.5697"
  },
  {
    "id": "5920",
    "platform": "Facebook",
    "category": "Comments",
    "description": "تعليق فيسبوك | إيموجي | حسابات مكررة وتعليقات مخفية | 10 ألف/يوم | فوري | الضمان: بدون تعويض ⚠️ 🚀",
    "price": "1.5697"
  },
  {
    "id": "5921",
    "platform": "Facebook",
    "category": "Comments",
    "description": "تعليقات فيسبوك | مخصص | عالمي | الحد الأدنى 5 | 5 ألف/يوم | فوري | الضمان: بدون تعويض ⚠️ 🚀",
    "price": "1.914"
  },
  {
    "id": "5922",
    "platform": "Facebook",
    "category": "Comments",
    "description": "تعليقات فيسبوك | مخصص | عالمي | الحد الأدنى 10 | 5 ألف/يوم | فوري | الضمان: بدون تعويض ⚠️ 🚀",
    "price": "2.1828"
  },
  {
    "id": "5923",
    "platform": "Facebook",
    "category": "Comments",
    "description": "تعليقات فيسبوك | مخصص | عالمي | الحد الأدنى 10 | 20 ألف/يوم | فوري | الضمان: بدون تعويض ⚠️ 🚀",
    "price": "2.2489"
  },
  {
    "id": "5780",
    "platform": "TikTok",
    "category": "Followers / Members",
    "description": "متابعين تيك توك | جودة عالية | سريعة | فوري | [الضمان: 10 يوم] ♻️ 🚀",
    "price": "1.1125"
  },
  {
    "id": "4100",
    "platform": "WhatsApp",
    "category": "Followers / Members",
    "description": "أعضاء / متابعين قناة واتساب | جودة حقيقية | الهند 🇮🇳 | سرعة فائقة 100 ألف في اليوم | بدون نقص | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.4063"
  },
  {
    "id": "2591",
    "platform": "WhatsApp",
    "category": "Followers / Members",
    "description": "أعضاء / متابعين قناة واتساب | جودة حقيقية | عربي 🇦🇪 | سرعة فائقة 100 ألف في اليوم | بدون نقص | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.4063"
  },
  {
    "id": "2592",
    "platform": "WhatsApp",
    "category": "Followers / Members",
    "description": "أعضاء / متابعين قناة واتساب | جودة حقيقية | تركيا 🇹🇷 | سرعة فائقة 100 ألف في اليوم | بدون نقص | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.4063"
  },
  {
    "id": "4392",
    "platform": "WhatsApp",
    "category": "Followers / Members",
    "description": "أعضاء / متابعين قناة واتساب | جودة حقيقية | أمريكا 🇺🇸 | سرعة فائقة 100 ألف في اليوم | بدون نقص | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.4063"
  },
  {
    "id": "1129",
    "platform": "WhatsApp",
    "category": "Followers / Members",
    "description": "أعضاء / متابعين قناة واتساب | جودة حقيقية | أوروبا 🇪🇺 | سرعة فائقة 100 ألف في اليوم | بدون نقص | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.4063"
  },
  {
    "id": "2411",
    "platform": "WhatsApp",
    "category": "Followers / Members",
    "description": "أعضاء / متابعين قناة واتساب | جودة حقيقية | البرازيل 🇧🇷 | سرعة فائقة 100 ألف في اليوم | بدون نقص | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.4063"
  },
  {
    "id": "2413",
    "platform": "WhatsApp",
    "category": "Followers / Members",
    "description": "أعضاء / متابعين قناة واتساب | جودة حقيقية | باكستان 🇵🇰 | سرعة فائقة 100 ألف في اليوم | بدون نقص | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.4063"
  },
  {
    "id": "3209",
    "platform": "WhatsApp",
    "category": "Followers / Members",
    "description": "أعضاء / متابعين قناة واتساب | جودة حقيقية | الفلبين 🇵🇭 | سرعة فائقة 100 ألف في اليوم | بدون نقص | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.4063"
  },
  {
    "id": "3487",
    "platform": "WhatsApp",
    "category": "Followers / Members",
    "description": "أعضاء / متابعين قناة واتساب | جودة حقيقية | تايلاند 🇹🇭 | سرعة فائقة 100 ألف في اليوم | بدون نقص | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.4063"
  },
  {
    "id": "1474",
    "platform": "WhatsApp",
    "category": "Followers / Members",
    "description": "أعضاء / متابعين قناة واتساب | جودة حقيقية | نيجيريا 🇳🇬 | سرعة فائقة 100 ألف في اليوم | بدون نقص | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.4063"
  },
  {
    "id": "4726",
    "platform": "Facebook",
    "category": "Followers / Members",
    "description": "متابعين فيسبوك | الحد الأقصى 30 ألف | كل الأنواع بروفايل / صفحات | داتا بوت | 20 ألف في اليوم ~ فوري ~ | الضمان: بدون تعويض ⚠️ 🚀",
    "price": "0.1213"
  },
  {
    "id": "4940",
    "platform": "Facebook",
    "category": "Followers / Members",
    "description": "متابعين فيسبوك | الحد الأقصى 30 ألف | كل الأنواع بروفايل / صفحات | داتا بوت | 20 ألف في اليوم ~ فوري ~ | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.1347"
  },
  {
    "id": "4938",
    "platform": "Facebook",
    "category": "Followers / Members",
    "description": "متابعين فيسبوك | الحد الأقصى 30 ألف | كل الأنواع بروفايل / صفحات | داتا بوت | 20 ألف في اليوم ~ فوري ~ | [الضمان: 30 يوم] ♻️ 🚀",
    "price": "0.1282"
  },
  {
    "id": "5924",
    "platform": "Facebook",
    "category": "Followers / Members",
    "description": "متابعين فيسبوك مصريين 100% 🎯 | بروفايل + صفحة | 💥 السرعة 10 ألف في اليوم | [الضمان: مدى الحياة] ♻️ 🚀",
    "price": "1.1185"
  },
  {
    "id": "4725",
    "platform": "Facebook",
    "category": "Followers / Members",
    "description": "متابعين فيسبوك | الحد الأقصى 30 ألف | كل الأنواع بروفايل / صفحات | داتا بوت | 20 ألف في اليوم ~ فوري ~ | الضمان: بدون تعويض ⚠️ 🚀",
    "price": "0.118"
  },
  {
    "id": "5925",
    "platform": "Instagram",
    "category": "Shares / Reposts",
    "description": "Instagram Shares - [ 𝗦𝘂𝗽𝗲𝗿 𝗙𝗮𝘀𝘁 ]",
    "price": "0.0005"
  },
  {
    "id": "5926",
    "platform": "Instagram",
    "category": "Shares / Reposts",
    "description": "Instagram Story Shares - [ 𝗦𝘂𝗽𝗲𝗿 𝗙𝗮𝘀𝘁 ]",
    "price": "0.0275"
  },
  {
    "id": "5927",
    "platform": "Instagram",
    "category": "Shares / Reposts",
    "description": "🇮🇷 Instagram Shares - [ IRAN ] 🇮🇷",
    "price": "0.0825"
  },
  {
    "id": "5928",
    "platform": "Instagram",
    "category": "Shares / Reposts",
    "description": "🇮🇳 Instagram Shares - [ INDIA ] 🇮🇳",
    "price": "0.0825"
  },
  {
    "id": "5929",
    "platform": "Instagram",
    "category": "Shares / Reposts",
    "description": "🇹🇷 Instagram Shares - [ TURKEY ] 🇹🇷",
    "price": "0.0825"
  },
  {
    "id": "5930",
    "platform": "Instagram",
    "category": "Shares / Reposts",
    "description": "🇷🇺 Instagram Shares - [ RUSSIA ] 🇷🇺",
    "price": "0.0825"
  },
  {
    "id": "5931",
    "platform": "Instagram",
    "category": "Shares / Reposts",
    "description": "🇧🇷 Instagram Shares - [ BRAZIL ] 🇧🇷",
    "price": "0.0825"
  },
  {
    "id": "5932",
    "platform": "Instagram",
    "category": "Shares / Reposts",
    "description": "🇪🇸 Instagram Shares - [ SPAIN ] 🇪🇸",
    "price": "0.0825"
  },
  {
    "id": "5933",
    "platform": "Instagram",
    "category": "Shares / Reposts",
    "description": "🇸🇦 Instagram Shares - [ SAUDI ARABIA ] 🇸🇦",
    "price": "0.0825"
  },
  {
    "id": "5934",
    "platform": "Instagram",
    "category": "Shares / Reposts",
    "description": "🇺🇸 Instagram Shares - [ UNITED STATE ] 🇺🇸",
    "price": "0.0825"
  },
  {
    "id": "5935",
    "platform": "Instagram",
    "category": "Shares / Reposts",
    "description": "🇨🇳 Instagram Shares - [ CHINA ] 🇨🇳",
    "price": "0.0825"
  },
  {
    "id": "5936",
    "platform": "Instagram",
    "category": "Shares / Reposts",
    "description": "🇮🇹 Instagram Shares - [ ITALY ] 🇮🇹",
    "price": "0.0825"
  },
  {
    "id": "5937",
    "platform": "Instagram",
    "category": "Shares / Reposts",
    "description": "🇩🇪 Instagram Shares - [ GERMANY ] 🇩🇪",
    "price": "0.0825"
  },
  {
    "id": "5938",
    "platform": "Instagram",
    "category": "Shares / Reposts",
    "description": "🇫🇷 Instagram Shares - [ FRANCE ] 🇫🇷",
    "price": "0.0825"
  },
  {
    "id": "5939",
    "platform": "Instagram",
    "category": "Shares / Reposts",
    "description": "🇮🇩 Instagram Shares - [ INDONESIA ] 🇮🇩",
    "price": "0.0825"
  },
  {
    "id": "5942",
    "platform": "YouTube",
    "category": "Followers / Members",
    "description": "YouTube Subscribers | Country/Quality: Jordan JO 🇯🇴 | Start Time: Within 24 Hours | Speed: Up to 1-5K /Days | 30 Days Refill ♻️ 🚀",
    "price": "35.2373"
  },
  {
    "id": "5943",
    "platform": "YouTube",
    "category": "Followers / Members",
    "description": "YouTube Subscribers | Country/Quality: Libya LY 🇱🇾 | Start Time: Within 24 Hours | Speed: Up to 1-5K /Days | 30 Days Refill ♻️ 🚀",
    "price": "35.2373"
  },
  {
    "id": "5944",
    "platform": "YouTube",
    "category": "Followers / Members",
    "description": "YouTube Subscribers | Country/Quality: Syria SY 🇸🇾 | Start Time: Within 24 Hours | Speed: Up to 1-5K /Days | 30 Days Refill ♻️ 🚀",
    "price": "35.2373"
  },
  {
    "id": "5945",
    "platform": "YouTube",
    "category": "Followers / Members",
    "description": "YouTube Subscribers | Country/Quality: Yemen YE 🇾🇪 | Start Time: Within 24 Hours | Speed: Up to 1-5K /Days | 30 Days Refill ♻️ 🚀",
    "price": "35.2373"
  },
  {
    "id": "5946",
    "platform": "YouTube",
    "category": "Followers / Members",
    "description": "YouTube Subscribers | Country/Quality: Kuwait KW 🇰🇼 | Start Time: Within 24 Hours | Speed: Up to 1-5K /Days | 30 Days Refill ♻️ 🚀",
    "price": "35.2373"
  },
  {
    "id": "5947",
    "platform": "YouTube",
    "category": "Followers / Members",
    "description": "YouTube Subscribers | Country/Quality: Qatar QA 🇶🇦 | Start Time: Within 24 Hours | Speed: Up to 1-5K /Days | 30 Days Refill ♻️ 🚀",
    "price": "35.2373"
  },
  {
    "id": "5940",
    "platform": "Facebook",
    "category": "Shares / Reposts",
    "description": "Facebook Post Shares | [Hidden] | Posts Only | 💥 Speed: 20K /Days | Lifetime Refill ♻️",
    "price": "0.2059"
  },
  {
    "id": "5941",
    "platform": "Facebook",
    "category": "Shares / Reposts",
    "description": "Facebook Post Shares | [Hidden] | Posts + Videos | 💥 Speed: 20K /Days | Lifetime Refill ♻️",
    "price": "0.4117"
  },
  {
    "id": "5948",
    "platform": "Marketing Tools",
    "category": "Subscriptions / Tools",
    "description": "Gemini Pro Subscription | 18 Months | No Refill ⚠️ 🚀",
    "price": "4.00"
  },
  {
    "id": "5791",
    "platform": "Facebook",
    "category": "Followers / Members",
    "description": "Facebook Followers | Page / Profile | 🎯 100 Pages 💯 | Speed: +10K /Days | 30 Days Refill ♻️ 🚀",
    "price": "2.0143"
  },
  {
    "id": "5792",
    "platform": "Facebook",
    "category": "Followers / Members",
    "description": "Facebook Followers Egyptian 🎯 | Profile / Pages | 30 Days Refill ♻️ 🚀",
    "price": "2.1816"
  },
  {
    "id": "5654",
    "platform": "TikTok",
    "category": "Followers / Members",
    "description": "TikTok Followers | Arabs & Egyptians SA EG | 100% Active Accounts | Sponsored Ads | No Refill ⛔ ⚠️ 🚀",
    "price": "3.3608"
  },
  {
    "id": "5655",
    "platform": "TikTok",
    "category": "Followers / Members",
    "description": "TikTok Followers | Arabs & Egyptians SA EG | 100% Active Accounts | Sponsored Ads | 30 Days Refill ♻️ 🚀",
    "price": "3.5269"
  },
  {
    "id": "5656",
    "platform": "TikTok",
    "category": "Followers / Members",
    "description": "TikTok Followers | Arabs & Egyptians SA EG | 100% Active Accounts | Sponsored Ads | 60 Days Refill ♻️ 🚀",
    "price": "3.6166"
  },
  {
    "id": "5657",
    "platform": "TikTok",
    "category": "Followers / Members",
    "description": "TikTok Followers | Arabs & Egyptians SA EG | 100% Active Accounts | Sponsored Ads | 90 Days Refill ♻️ 🚀",
    "price": "3.7063"
  },
  {
    "id": "5949",
    "platform": "Facebook",
    "category": "Followers / Members",
    "description": "Pack 5K Facebook Followers Egyptian 🎯 | Non Drop 🔥 | Speed 1000/5000 /Days | Lifetime Refill ♻️ 🚀",
    "price": "1.334"
  },
  {
    "id": "5950",
    "platform": "Facebook",
    "category": "Followers / Members",
    "description": "Pack 10K Facebook Followers | 100% Egyptian Pages 🎯 | Profile+Page | 💥 Speed 50K /Days | Lifetime Refill ♻️ 🚀",
    "price": "1.2314"
  },
  {
    "id": "4879",
    "platform": "Facebook",
    "category": "Followers / Members",
    "description": "Facebook Followers | Page Likes + Followers | Real Accounts | Low Drop | Instant Speed | Lifetime Refill ♻️ 🚀",
    "price": "0.35"
  },
  {
    "id": "4244",
    "platform": "YouTube",
    "category": "Subscriptions / Tools",
    "description": "YouTube WatchTime [100 - 4000 hours] | SLOW | 30 Days Refill ♻️ 🚀",
    "price": "17.50"
  },
  {
    "id": "4243",
    "platform": "YouTube",
    "category": "Subscriptions / Tools",
    "description": "YouTube WatchTime [4000 hours] | 30 Days Refill ♻️ 🚀",
    "price": "18.75"
  },
  {
    "id": "4242",
    "platform": "YouTube",
    "category": "Subscriptions / Tools",
    "description": "YouTube WatchTime [2000 hours] | 30 Days Refill ♻️ 🚀",
    "price": "22.50"
  },
  {
    "id": "2632",
    "platform": "YouTube",
    "category": "Views",
    "description": "YouTube Views | Speed 2000-4000 per day | No Refill ⚠️ 🔴 🚀",
    "price": "0.40"
  },
  {
    "id": "2633",
    "platform": "YouTube",
    "category": "Views",
    "description": "YouTube Views | 👤 Real | Speed 10K /Days | 30 Days Refill ♻️ ⚡ 🚀",
    "price": "0.80"
  },
  {
    "id": "2224",
    "platform": "YouTube",
    "category": "Views",
    "description": "YouTube Views | 5K-10K /Days | Non Drop | Lifetime Refill ♻️ 🔮 🏆 🚀",
    "price": "0.85"
  },
  {
    "id": "2634",
    "platform": "YouTube",
    "category": "Views",
    "description": "YouTube Views | Min: 10 | Non Drop | Speed: 3K/Day | Lifetime Refill ♻️ 🍿 🚀",
    "price": "0.875"
  },
  {
    "id": "5951",
    "platform": "Facebook",
    "category": "Followers / Members",
    "description": "Facebook Followers [ All Types ] [ Max 1M ] | Hidden Profiles | Low Drop | No Refill ⚠️ | Instant Start | 25K /Days 🚀",
    "price": "0.125"
  },
  {
    "id": "5952",
    "platform": "Facebook",
    "category": "Followers / Members",
    "description": "Facebook Followers [ All Types ] [ Max 1M ] | Hidden Profiles | Low Drop | 30 Days Refill ♻️ | Instant Start | 25K /Days 🚀",
    "price": "0.1313"
  },
  {
    "id": "5953",
    "platform": "Facebook",
    "category": "Followers / Members",
    "description": "Facebook Followers [ All Types ] [ Max 1M ] | Hidden Profiles | Low Drop | 60 Days Refill ♻️ | Instant Start | 25K /Days 🚀",
    "price": "0.1338"
  },
  {
    "id": "5954",
    "platform": "Facebook",
    "category": "Followers / Members",
    "description": "Facebook Followers [ All Types ] [ Max 1M ] | Hidden Profiles | Low Drop | 90 Days Refill ♻️ | Instant Start | 25K /Days 🚀",
    "price": "0.1375"
  },
  {
    "id": "5955",
    "platform": "Facebook",
    "category": "Followers / Members",
    "description": "Facebook Followers [ All Types ] [ Max 1M ] | Hidden Profiles | Low Drop | 365 Days Refill ♻️ | Instant Start | 25K /Days 🚀",
    "price": "0.14"
  },
  {
    "id": "5956",
    "platform": "Facebook",
    "category": "Followers / Members",
    "description": "Facebook Followers [ All Types ] [ Max 1M ] | Hidden Profiles | Low Drop | Lifetime Refill ♻️ | Instant Start | 25K /Days 🚀",
    "price": "0.1425"
  },
  {
    "id": "4900",
    "platform": "Facebook",
    "category": "Likes / Reactions",
    "description": "Facebook Post Likes | Hidden Accounts | 5K /Days | Likes 👍 | No Refill ⚠️ 🚀",
    "price": "0.2113"
  },
  {
    "id": "5226",
    "platform": "Facebook",
    "category": "Likes / Reactions",
    "description": "Facebook Post Reaction | Hidden Accounts | 5K /Days | Love 💖 | No Refill ⚠️ 🚀",
    "price": "0.2113"
  },
  {
    "id": "5464",
    "platform": "Facebook",
    "category": "Likes / Reactions",
    "description": "Facebook Post Reaction | Hidden Accounts | 5K /Days | Wow 😲 | No Refill ⚠️ 🚀",
    "price": "0.2113"
  },
  {
    "id": "5228",
    "platform": "Facebook",
    "category": "Likes / Reactions",
    "description": "Facebook Post Reaction | Hidden Accounts | 5K /Days | Haha 😂 | No Refill ⚠️ 🚀",
    "price": "0.2113"
  },
  {
    "id": "5227",
    "platform": "Facebook",
    "category": "Likes / Reactions",
    "description": "Facebook Post Reaction | Hidden Accounts | 5K /Days | Sad 😭 | No Refill ⚠️ 🚀",
    "price": "0.2113"
  },
  {
    "id": "5229",
    "platform": "Facebook",
    "category": "Likes / Reactions",
    "description": "Facebook Post Reaction | Hidden Accounts | 5K /Days | Angry 😡 | No Refill ⚠️ 🚀",
    "price": "0.2113"
  },
  {
    "id": "4899",
    "platform": "Facebook",
    "category": "Likes / Reactions",
    "description": "Facebook Post React | Arab | Angry 🤬 | Non Drop | +500/Day | Lifetime Refill 🔥 🚀",
    "price": "2.235"
  },
  {
    "id": "4901",
    "platform": "Facebook",
    "category": "Likes / Reactions",
    "description": "Facebook Post React | Arab | Mix React 👍 ❤️ 🥰 | +500/Day | Lifetime Refill 🔥 🚀",
    "price": "2.235"
  },
  {
    "id": "5957",
    "platform": "TikTok",
    "category": "Views",
    "description": "TikTok Views | HQ | Fast | Instant | No Refill ⚠️ 🚀",
    "price": "0.003"
  },
  {
    "id": "5958",
    "platform": "TikTok",
    "category": "Views",
    "description": "TikTok Views | HQ | Fast | Instant | 30 Days Refill ♻️ 🚀",
    "price": "0.0039"
  },
  {
    "id": "5784",
    "platform": "YouTube",
    "category": "Likes / Reactions",
    "description": "YouTube Like | Max 5k | 5k /Days | Instant | No Refill ⚠️ 🚀",
    "price": "0.2448"
  },
  {
    "id": "5960",
    "platform": "Facebook",
    "category": "Followers / Members",
    "description": "Facebook Followers 100% Egyptian 🎯 | Profile + Page | 💥 Speed: 10K /Days | Lifetime Refill ♻️ 🚀",
    "price": "0.673"
  },
  {
    "id": "5959",
    "platform": "Facebook",
    "category": "Followers / Members",
    "description": "Facebook Followers 100% Egyptian 🎯 | Profile + Page | 💥 Speed: 10K /Days | 30 Days Refill ♻️ 🚀",
    "price": "0.7408"
  }
]; SESSIONS={}
PLATFORMS=sorted(set(s['platform'] for s in SERVICES)); CATEGORIES={p:sorted(set(s['category'] for s in SERVICES if s['platform']==p)) for p in PLATFORMS}

def post(url,data,timeout=60):
 req=urllib.request.Request(url,data=urllib.parse.urlencode(data).encode(),method='POST'); req.add_header('Content-Type','application/x-www-form-urlencoded')
 with urllib.request.urlopen(req,timeout=timeout) as r:return json.loads(r.read().decode())
def tg(method,data): return post(f"{TG}/{method}",data)
def send(cid,text,markup=None):
 d={'chat_id':str(cid),'text':text}; 
 if markup:d['reply_markup']=json.dumps({'inline_keyboard':markup},ensure_ascii=False)
 tg('sendMessage',d)
def edit(cid,mid,text,markup=None):
 d={'chat_id':str(cid),'message_id':str(mid),'text':text}
 if markup:d['reply_markup']=json.dumps({'inline_keyboard':markup},ensure_ascii=False)
 tg('editMessageText',d)
def answer(qid):
 try:tg('answerCallbackQuery',{'callback_query_id':qid})
 except:pass
def button(text,data):return {'text':text,'callback_data':data}
def platform_menu():
 return [[button(p,f'p:{i}') for i,p in enumerate(PLATFORMS[j:j+2])] for j in range(0,len(PLATFORMS),2)]
def category_menu(pi):
 cs=CATEGORIES[PLATFORMS[pi]]; return [[button(c,f'c:{pi}:{i}')] for i,c in enumerate(cs)]+[[button('⬅️ رجوع','home')]]
def service_menu(pi,ci,page=0):
 p=PLATFORMS[pi]; c=CATEGORIES[p][ci]; items=[s for s in SERVICES if s['platform']==p and s['category']==c]; size=8; part=items[page*size:(page+1)*size]
 rows=[[button(f"{s['id']} | {s['price']}$",f"s:{pi}:{ci}:{s['id']}") ] for s in part]
 nav=[]
 if page>0:nav.append(button('⬅️ السابق',f'pg:{pi}:{ci}:{page-1}'))
 if (page+1)*size<len(items):nav.append(button('التالي ➡️',f'pg:{pi}:{ci}:{page+1}'))
 if nav:rows.append(nav)
 rows.append([button('⬅️ الأقسام','pback'),button('🏠 الرئيسية','home')]); return rows,len(items),part

def home(cid,mid=None):
 text='أهلًا بك في @AlEzzMediaBot\n\nاختر المنصة المطلوبة:'; m=platform_menu()
 if mid:edit(cid,mid,text,m)
 else:send(cid,text,m)
def handle_callback(q):
 answer(q.get('id')); d=q.get('data',''); msg=q.get('message',{}); cid=msg.get('chat',{}).get('id'); mid=msg.get('message_id')
 if cid is None:return
 if d=='home':home(cid,mid);return
 if d=='pback':home(cid,mid);return
 if d.startswith('p:'):
  pi=int(d.split(':')[1]); edit(cid,mid,f"منصة {PLATFORMS[pi]}\nاختر القسم:",category_menu(pi));return
 if d.startswith('c:'):
  _,pi,ci=d.split(':'); pi=int(pi);ci=int(ci); m,n,part=service_menu(pi,ci); edit(cid,mid,f"{PLATFORMS[pi]} — {CATEGORIES[PLATFORMS[pi]][ci]}\nاختر الخدمة (السعر لكل 1000):",m);return
 if d.startswith('pg:'):
  _,pi,ci,page=d.split(':');m,n,part=service_menu(int(pi),int(ci),int(page));edit(cid,mid,f"اختر الخدمة ({n} خدمة):",m);return
 if d.startswith('s:'):
  _,pi,ci,sid=d.split(':'); s=next(x for x in SERVICES if x['id']==sid); SESSIONS[cid]={'step':'link','service':sid,'description':s['description']}; edit(cid,mid,f"الخدمة المختارة:\n{s['description']}\n\nأرسل الرابط أو اسم المستخدم.",[ [button('❌ إلغاء','cancel')] ]);return
 if d=='cancel':SESSIONS.pop(cid,None);edit(cid,mid,'تم إلغاء الطلب.');return

def handle_message(m):
 cid=m.get('chat',{}).get('id'); text=(m.get('text') or '').strip()
 if cid is None:return
 if text in ('/start','/help'):home(cid);return
 if text=='/cancel':SESSIONS.pop(cid,None);send(cid,'تم إلغاء الطلب.');return
 s=SESSIONS.get(cid)
 if not s:send(cid,'اضغط /start للبدء.');return
 if s['step']=='link':
  if not text:send(cid,'أرسل الرابط أو اسم المستخدم.');return
  s['link']=text;s['step']='quantity';send(cid,'أرسل الكمية بالأرقام.');return
 if s['step']=='quantity':
  try:q=int(text);assert 1<=q<=1000000
  except:send(cid,'أرسل كمية صحيحة بين 1 و 1,000,000.');return
  send(cid,'جارٍ إرسال الطلب...')
  try:
   r=post(API_URL,{'key':API_KEY,'action':'add','service':s['service'],'link':s['link'],'quantity':str(q)})
   send(cid,f"تم الطلب بنجاح ✅\nرقم الطلب: {r['order']}" if r.get('order') else 'لم يتم إنشاء الطلب: '+str(r.get('error',r)))
  except Exception:log.exception('order failed');send(cid,'تعذر الاتصال بمنصة الطلبات. تحقق من مفتاح ترنداوي.')
  finally:SESSIONS.pop(cid,None)

def main():
 off=0;log.info('started with %s services',len(SERVICES))
 while True:
  try:
   r=post(f"{TG}/getUpdates",{'offset':str(off),'timeout':'50','allowed_updates':json.dumps(['message','callback_query'])},65)
   for u in r.get('result',[]):
    off=u['update_id']+1
    if u.get('callback_query'):handle_callback(u['callback_query'])
    elif u.get('message'):
     try:handle_message(u['message'])
     except Exception:log.exception('handler failed')
  except Exception:log.exception('poll failed');time.sleep(5)
if __name__=='__main__':main()
