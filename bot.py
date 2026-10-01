import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
SMMGEN_API_KEY = os.environ["SMMGEN_API_KEY"]
SMMGEN_API_URL = os.getenv("SMMGEN_API_URL", "https://my.smmgen.com/api/v2")
FB_LIKES_SERVICE_ID = os.getenv("FB_LIKES_SERVICE_ID", "17347")
FB_FOLLOWERS_SERVICE_ID = os.getenv("FB_FOLLOWERS_SERVICE_ID", "17443")

SERVICE, LINK, QUANTITY = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلًا بك في AlEzzMediaBot.\n\n"
        "اختر الخدمة بإرسال رقمها:\n"
        "1 - إعجابات فيسبوك\n"
        "2 - متابعو فيسبوك\n\n"
        "اكتب /cancel للإلغاء."
    )
    return SERVICE

async def receive_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text.strip()
    if choice == "1":
        context.user_data["service"] = FB_LIKES_SERVICE_ID
        context.user_data["service_name"] = "إعجابات فيسبوك"
    elif choice == "2":
        context.user_data["service"] = FB_FOLLOWERS_SERVICE_ID
        context.user_data["service_name"] = "متابعو فيسبوك"
    else:
        await update.message.reply_text("أرسل 1 لإعجابات فيسبوك أو 2 لمتابعي فيسبوك.")
        return SERVICE
    await update.message.reply_text("أرسل رابط صفحة أو منشور فيسبوك العام.")
    return LINK

async def receive_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text.strip()
    if not (link.startswith("http://") or link.startswith("https://")):
        await update.message.reply_text("أرسل رابطًا صحيحًا يبدأ بـ http:// أو https://")
        return LINK
    context.user_data["link"] = link
    await update.message.reply_text("أرسل الكمية المطلوبة بالأرقام (مثال: 100).")
    return QUANTITY

async def receive_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        quantity = int(update.message.text.strip())
        if quantity <= 0 or quantity > 1_000_000:
            raise ValueError
    except ValueError:
        await update.message.reply_text("أرسل كمية صحيحة بين 1 و 1,000,000.")
        return QUANTITY

    payload = {
        "key": SMMGEN_API_KEY,
        "action": "add",
        "service": context.user_data["service"],
        "link": context.user_data["link"],
        "quantity": quantity,
    }
    try:
        response = requests.post(SMMGEN_API_URL, data=payload, timeout=20)
        response.raise_for_status()
        result = response.json()
    except Exception:
        log.exception("SMMGen request failed")
        await update.message.reply_text("تعذر الاتصال بمنصة الطلبات. حاول لاحقًا.")
        return ConversationHandler.END

    if result.get("order"):
        await update.message.reply_text(
            f"تم استلام طلب {context.user_data['service_name']} بنجاح.\n"
            f"رقم الطلب: {result['order']}"
        )
    else:
        await update.message.reply_text(f"لم يتم إنشاء الطلب: {result.get('error', 'خطأ غير معروف')}")
    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("تم إلغاء العملية.")
    return ConversationHandler.END

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("استخدم /start لإنشاء طلب، أو /cancel للإلغاء.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conversation = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_service)],
            LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_link)],
            QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_quantity)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conversation)
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("cancel", cancel))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
