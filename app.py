from flask import *
from datetime import datetime
import json
import sqlite3
import webbrowser
import os

app = Flask(__name__)

@app.route("/")
def home():
    # Date du jour (jour et mois)
    today = datetime.now().strftime("%d-%m")
    # Charger les événements depuis events.json
    with open("events.json", "r", encoding="utf-8") as f:
       events = json.load(f)
    # Récupérer les événements correspondant
    todays_events = events.get(today, ["Aucun événement pour aujourd'hui"])
    return render_template("index.html", events=todays_events, message = message)

@app.route("/enregistrer_avis", methods=["POST"])
def enregistrer_avis():
    avis = request.form.get("avis")

    if avis:
        # Charger les avis existants
        if os.path.exists("avis.json"):
            with open("avis.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []

        # Ajouter le nouvel avis
        data.append({"avis": avis})

        # Sauvegarder dans le fichier
        with open("avis.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    return redirect("/")

@app.route("/liste")
def liste():
    with sqlite3.connect("avis.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM donnees")
        resultats = cur.fetchall()  # récupère toutes les lignes

    # On prépare une petite page HTML pour afficher
    html = "<h1>Liste des textes enregistrés</h1><ul>"
    for ligne in resultats:
        html += f"<li>{ligne[1]}</li>"  # ligne[0] = id, ligne[1] = texte
    html += "</ul>"

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
