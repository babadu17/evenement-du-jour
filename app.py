from flask import Flask, render_template
from datetime import datetime
import json

app = Flask(__name__)

@app.route("/")
def index():
    # Récupérer la date du jour au format MM-DD
    today = datetime.today().strftime("%m-%d")

    # Charger le fichier JSON
    with open("evenement.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Chercher l’événement correspondant
    event = data.get(today, "Aucun événement enregistré pour aujourd'hui.")

    return render_template("index.html", event=event)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
