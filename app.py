from flask import *
from datetime import datetime
import json
import sqlite3

app = Flask(__name__)

# Charger les événements depuis events.json
with open("events.json", "r", encoding="utf-8") as f:
    events = json.load(f)

@app.route("/")
def home():
    # Date du jour (jour et mois)
    today = datetime.now().strftime("%d-%m")
    # Récupérer les événements correspondant
    todays_events = events.get(today, ["Aucun événement pour aujourd'hui"])
    return render_template("index.html", events=todays_events)

@app.route("/enregistrer_avis", methods=["POST"])
def enregistrer_avis():
    texte = request.form["avi"]

    with sqlite3.connect("avis.db", timeout=5) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS donnees (id INTEGER PRIMARY KEY, texte TEXT)")
        cur.execute("INSERT INTO donnees (texte) VALUES (?)", (texte,))
        conn.commit()

    return redirect(url_for("/"))

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
