from flask import Flask, render_template
from datetime import datetime
import json

app = Flask(__name__)

# Charger les événements depuis events.json
with open("events.json", "r", encoding="utf-8") as f:
    events = json.load(f)

@app.route("/")
def home():
    # Date du jour (jour et mois)
    today = datetime.now().strftime("%d-%m")
    # Récupérer les événements correspondant
    todays_events = events.get(today, [])
    return render_template("index.html", events=todays_events)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
