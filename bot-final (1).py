import os
import json
import time
import logging
import urllib.parse
import urllib.request
import urllib.error

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("al-ezz-bot")

# Secrets must be entered in Railway Variables, never inside this file.
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"].strip()
SMMGEN_API_KEY = os.environ["SMMGEN_API_KEY"].strip()
SMMGEN_API_URL = os.getenv("SMMGEN_API_URL", "https://my.smmgen.com/api/v2").strip()
LIKES_SERVICE_ID = os.getenv("FB_LIKES_SERVICE_ID", "17347").strip()
FOLLOWERS_SERVICE_ID = os.getenv("FB_FOLLOWERS_SERVICE_ID", "17443").strip()
BOT_USERNAME = "@Aziz771400_bot"

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"
sessions = {}


def post_form(url, data, timeout=60):
    body = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(url, data=body, method="POST")
    request.add_header("Content-Type", "application/x-www-form-urlencoded")
    request.add_header("User-Agent", "AlEzzMediaBot/1.0")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
            return json.loads(raw)
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {raw[:300]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from exc


def telegram(method, data):
    result = post_form(f"{TELEGRAM_API}/{method}", data)
    if not result.get("ok", False):
        raise RuntimeError(f"Telegram API error: {result}")
    return result


def send(chat_id, text):
    telegram("sendMessage", {"chat_id": str(chat_id), "text": text})


def start_message(chat_id):
    sessions[chat_id] = {"step": "service"}
    send(
        chat_id,
        f"أهلًا بك في {BOT_USERNAME}.\n\n"
        "اختر الخدمة بإرسال رقمها:\n"
        "1 - إعجابات فيسبوك\n"
        "2 - متابعو فيسبوك\n\n"
        "أرسل /cancel للإلغاء."
    )


def handle_message(message):
    chat_id = message.get("chat", {}).get("id")
    text = (message.get("text") or "").strip()
    if chat_id is None:
        return

    if text in ("/start", "/help"):
        start_message(chat_id)
        return

    if text == "/cancel":
        sessions.pop(chat_id, None)
        send(chat_id, "تم إلغاء العملية.")
        return

    session = sessions.get(chat_id)
    if not session:
        send(chat_id, "أرسل /start للبدء.")
        return

    if session["step"] == "service":
        if text == "1":
            session.update(service=LIKES_SERVICE_ID, name="إعجابات فيسبوك")
        elif text == "2":
            session.update(service=FOLLOWERS_SERVICE_ID, name="متابعو فيسبوك")
        else:
            send(chat_id, "أرسل 1 لإعجابات فيسبوك أو 2 لمتابعي فيسبوك.")
            return
        session["step"] = "link"
        send(chat_id, "أرسل رابط صفحة أو منشور فيسبوك العام.")
        return

    if session["step"] == "link":
        if not text.startswith(("http://", "https://")):
            send(chat_id, "أرسل رابطًا صحيحًا يبدأ بـ http:// أو https://")
            return
        session["link"] = text
        session["step"] = "quantity"
        send(chat_id, "أرسل الكمية المطلوبة بالأرقام، مثل: 100")
        return

    if session["step"] == "quantity":
        try:
            quantity = int(text)
            if not 1 <= quantity <= 1_000_000:
                raise ValueError
        except ValueError:
            send(chat_id, "أرسل كمية صحيحة بين 1 و 1,000,000.")
            return

        send(chat_id, "جارٍ إرسال الطلب، انتظر قليلًا...")
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
                send(chat_id, "لم يتم إنشاء الطلب:\n" + str(result.get("error", result)))
        except Exception as exc:
            log.exception("SMMGen request failed: %s", exc)
            send(chat_id, "تعذر الاتصال بمنصة الطلبات. تأكد من مفتاح SMMGen ورابط API ثم حاول لاحقًا.")
        finally:
            sessions.pop(chat_id, None)


def main():
    offset = 0
    log.info("AlEzzMediaBot started")
    while True:
        try:
            result = post_form(
                f"{TELEGRAM_API}/getUpdates",
                {"offset": str(offset), "timeout": "50", "allowed_updates": json.dumps(["message"])},
                timeout=65,
            )
            for update in result.get("result", []):
                offset = update["update_id"] + 1
                if update.get("message"):
                    try:
                        handle_message(update["message"])
                    except Exception:
                        log.exception("Message handling failed")
        except Exception:
            log.exception("Polling failed")
            time.sleep(5)


if __name__ == "__main__":
    main()
