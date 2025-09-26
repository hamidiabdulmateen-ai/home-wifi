from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_TOKEN = "8416601223:AAFR42VtKLQivbihzQNSutUS-hQ4nTNy_oQ"
CHAT_ID = "6689313262"

def send_to_telegram(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

@app.route("/notify", methods=["GET", "POST"])
def notify():
    if request.method == "POST":
        data = request.get_json(force=True, silent=True) or {}
        action = data.get("action", "Unknown Action")
        name = data.get("name", "")
        ip = data.get("ip", "")
        extra = data.get("extra", "")
        time = data.get("time", "")
        msg = f"📢 {action}\n👤 {name}\n🌐 {ip}\n🕒 {time}\nℹ️ {extra}"
    else:
        msg = request.args.get("msg", "No message")
    
    send_to_telegram(msg)
    return jsonify({"status": "ok", "sent": msg})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
