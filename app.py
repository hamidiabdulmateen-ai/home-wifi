from flask import Flask, request, jsonify
import requests
import os
import time
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# بهتره توکن و chat id را در متغیر محیطی ذخیره کنی (در render/fly/… تنظیم کنید)
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8416601223:AAFR42VtKLQivbihzQNSutUS-hQ4nTNy_oQ")
CHAT_ID = os.environ.get("CHAT_ID", "6689313262")

TELEGRAM_TIMEOUT = 5  # ثانیه، جلوگیری از بلوکه شدن درخواست‌ها

def send_to_telegram(message: str):
    """
    ارسال پیام به تلگرام با timeout و هندل ارور ساده
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        resp = requests.post(url, data=data, timeout=TELEGRAM_TIMEOUT)
        resp.raise_for_status()
        logging.info("Telegram sent: %s", message[:80])
        return True
    except Exception as e:
        logging.warning("Failed to send to telegram: %s", e)
        return False

@app.route("/notify", methods=["GET", "POST"])
def notify():
    """
    مسیر اصلی که کلاینت‌ها برای ارسال اطلاعیه‌ها ازش استفاده می‌کنند.
    """
    if request.method == "POST":
        data = request.get_json(force=True, silent=True) or {}
        action = data.get("action", "Unknown Action")
        name = data.get("name", "")
        ip = data.get("ip", "")
        extra = data.get("extra", "")
        time_str = data.get("time", "")
        msg = f"📢 {action}\n👤 {name}\n🌐 {ip}\n🕒 {time_str}\nℹ️ {extra}"
    else:
        msg = request.args.get("msg", "No message")

    ok = send_to_telegram(msg)
    return jsonify({"status": "ok" if ok else "failed", "sent": msg})

@app.route("/health", methods=["GET"])
def health():
    """
    مسیر سلامت بسیار سبک — فقط 200 OK و یک JSON کوچک.
    این مسیر را در UptimeRobot یا سرویس پینگ هر 5 دقیقه قرار بده.
    """
    return jsonify({"status": "ok", "time": int(time.time())}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # در محیط توسعه فقط debug=True; در پروداکشن از gunicorn/uvicorn یا render استفاده کن
    app.run(host="0.0.0.0", port=port)
