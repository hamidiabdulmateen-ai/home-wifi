from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "8416601223:AAFR42VtKLQivbihzQNSutUS-hQ4nTNy_oQ"
CHAT_ID = "6689313262"

def send_to_telegram(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

@app.route("/notify")
def notify():
    msg = request.args.get("msg", "No message")
    send_to_telegram(f"📢 {msg}")
    return {"status": "ok", "sent": msg}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
