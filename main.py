from flask import Flask, render_template, request, jsonify, send_from_directory
from bot import SmashKartsBgBot, bot_instance
import os

app = Flask(__name__, static_folder="static", template_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start-bot", methods=["POST"])
def start_bot():
    if bot_instance.start_bot():
        return jsonify({"status": "started"})
    return jsonify({"status": "already running"})

@app.route("/stop-bot", methods=["POST"])
def stop_bot():
    if bot_instance.stop_bot():
        return jsonify({"status": "stopped"})
    return jsonify({"status": "not running"})

@app.route('/novnc/<path:filename>')
def serve_novnc(filename):
    return send_from_directory('static/novnc', filename)

if __name__ == "__main__":
    bot_instance.setup_browser_bg()
    bot_instance.navigate_and_setup()
    app.run(host="0.0.0.0", port=5000) 