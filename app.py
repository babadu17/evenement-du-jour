from flask import Flask, render_template
from datetime import datetime
import json

app = Flask(__name__)

@app.route("/")
def index():
    today = datetime.today().strftime("%m-%d")
    with open("events.json", "r", encoding="utf-8") as f:
        events = json.load(f)
    todays_events = events.get(today, ["Aucun annivairesaire enregistrer aujourd'hui",""])
    return render_template("index.html", events=todays_events)
