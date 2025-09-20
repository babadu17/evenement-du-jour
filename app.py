from flask import Flask, render_template
from datetime import datetime
import json

app = Flask(__name__)

@app.route("/")
def index():
    today = datetime.today().strftime("%m-%d")
    
    # Charger le fichier JSON
    with open("events.json", "r", encoding="utf-8") as f:
        events = json.load(f)
    
    # Récupérer la liste d'événements du jour
    todays_events = events.get(today, ["Aucun événement trouvé pour aujourd'hui."])
    
    return render_template("index.html", events=todays_events)
