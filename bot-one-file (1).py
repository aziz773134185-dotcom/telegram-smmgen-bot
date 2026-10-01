import os
import json
import time
import logging
import urllib.parse
import urllib.request
import urllib.error

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
SMMGEN_API_KEY = os.environ["SMMGEN_API_KEY"]
SMMGEN_API_URL = os.getenv("SMMGEN_API_URL", "https://my.smmgen.com/api/v2")
LIKES_SERVICE_ID = os.getenv("FB_LIKES_SERVICE_ID", "17347")
FOLLOWERS_SERVICE_ID = os.getenv("FB_FOLLOWERS_SERVICE_ID", "17443")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

sessions = {}


def post_form(url, data, timeout=35):
    body = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(url, data=body, method="POST")
    request.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def telegram(method, data):
    return post_form(f"{TELEGRAM_API}/{method}", data)


def send(chat_id, text):
    telegram("sendMessage", {"chat_id": str(chat_id), "text": text})


def handle_message(message):
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = (message.get("text") or "").strip()
    if chat_id is None:
        return

    if text == "/cancel":
        sessions.pop(chat_id, None)
        send(chat_id, "تم إلغاء العملية.")
        return

    if text in ("/start", "/help"):
        sessions[chat_id] = {"step": "service"}
        send(chat_id, "أهلًا بك في AlEzzMediaBot.\n\nاختر الخدمة بإرسال رقمها:\n1 - إعجابات فيسبوك\n2 - متابعو فيسبوك\n\nاكتب /cancel للإلغاء.")
        return

    session = sessions.get(chat_id)
    if not session:
        send(chat_id, "أرسل /start للبدء.")
        return

    if session["step"] == "service":
        if text == "1":
            session["service"] = LIKES_SERVICE_ID
            session["name"] = "إعجابات فيسبوك"
        elif text == "2":
            session["service"] = FOLLOWERS_SERVICE_ID
            session["name"] = "متابعو فيسبوك"
        else:
            send(chat_id, "أرسل 1 لإعجابات فيسبوك أو 2 لمتابعي فيسبوك.")
            return
        session["step"] = "link"
        send(chat_id, "أرسل رابط صفحة أو منشور فيسبوك العام.")
        return

    if session["step"] == "link":
        if not (text.startswith("http://") or text.startswith("https://")):
            send(chat_id, "أرسل رابطًا صحيحًا يبدأ بـ http:// أو https://")
            return
        session["link"] = text
        session["step"] = "quantity"
        send(chat_id, "أرسل الكمية المطلوبة بالأرقام، مثل: 100")
        return

    if session["step"] == "quantity":
        try:
            quantity = int(text)
            if quantity < 1 or quantity > 1000000:
                raise ValueError
        except ValueError:
            send(chat_id, "أرسل كمية صحيحة بين 1 و 1,000,000.")
            return

        try:
            result = post_form(SMMGEN_API_URL, {
                "key": SMMGEN_API_KEY,
                "action": "add",
                "service": session["service"],
                "link": session["link"],
                "quantity": str(quantity),
            })
            if result.get("order"):
                send(chat_id, f"تم استلام طلب {session['name']} بنجاح.\nرقم الطلب: {result['order']}")
            else:
                send(chat_id, "لم يتم إنشاء الطلب: " + str(result.get("error", "خطأ غير معروف")))
        except Exception:
            logging.exception("SMMGen request failed")
            send(chat_id, "تعذر الاتصال بمنصة الطلبات. حاول لاحقًا.")
        finally:
            sessions.pop(chat_id, None)


def main():
    offset = 0
    logging.info("Bot started")
    while True:
        try:
            result = post_form(f"{TELEGRAM_API}/getUpdates", {
                "offset": str(offset),
                "timeout": "50",
                "allowed_updates": json.dumps(["message"]),
            }, timeout=60)
            for update in result.get("result", []):
                offset = update["update_id"] + 1
                if update.get("message"):
                    handle_message(update["message"])
        except Exception:
            logging.exception("Polling error")
            time.sleep(5)


if __name__ == "__main__":
    main()
