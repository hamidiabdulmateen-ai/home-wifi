from flask import Flask, request, jsonify
import requests
from datetime import datetime
import os
import html

app = Flask(__name__)

# ====== این مقادیر را با مقادیر خودت جایگزین کن ======
BOT_TOKEN = "توکن ربات"
CHAT_ID = "چت آی‌دی"
# ======================================================

LOG_FILE = "events_log.txt"

def write_log(text: str):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{ts}] {text}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)

def send_to_telegram(message: str, parse_mode: str = "Markdown"):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True
    }
    try:
        resp = requests.post(url, data=payload, timeout=8)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        write_log(f"Telegram send error: {e} | payload: {message}")
        return {"ok": False, "error": str(e)}

def escape_md(text: str) -> str:
    if text is None:
        return ""
    return text.replace("_", "\\_").replace("*", "\\*").replace("`", "\\`").replace("[", "\\[").replace("]", "\\]")

@app.route("/notify", methods=["GET", "POST"])
def notify():
    if request.method == "GET":
        msg = request.args.get("msg", "No message")
        write_log(f"GET notify: {msg}")
        send_to_telegram(f"📢 {escape_md(msg)}", parse_mode="Markdown")
        return jsonify(status="ok", sent=msg)

    data = {}
    try:
        data = request.get_json(force=True)
    except Exception:
        data = request.form.to_dict() or {}

    action = data.get("action", data.get("msg", "unknown"))
    name = data.get("name", "")
    ip = data.get("ip", "")
    ts = data.get("time", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"))
    extra = data.get("extra", "")

    msg_lines = [
        "⚡ *Device Activity*",
        f"*Action:* {escape_md(action)}"
    ]
    if name:
        msg_lines.append(f"*Name:* {escape_md(name)}")
    if ip:
        msg_lines.append(f"*IP:* `{escape_md(ip)}`")
    msg_lines.append(f"*Time:* {escape_md(ts)}")
    if extra:
        msg_lines.append(f"*Info:* {escape_md(extra)}")

    message = "\n".join(msg_lines)

    write_log(f"POST notify -> action={action} name={name} ip={ip} time={ts} extra={extra}")

    result = send_to_telegram(message, parse_mode="Markdown")

    return jsonify(status="ok", sent={"action": action, "name": name, "ip": ip, "time": ts}, telegram=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
