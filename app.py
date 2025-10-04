from flask import *
from datetime import datetime
import json
import sqlite3
import webbrowser
import os

# Créer la table si elle n'existe pas
conn = sqlite3.connect("database.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS avis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    texte TEXT
)
""")
conn.commit()
conn.close()

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
    return render_template("index.html", events=todays_events)

@app.route("/enregistrer_avis", methods=["POST"])
def enregistrer_avis():
    avis = request.form.get("avis")       # texte de l'avis
    note = request.form.get("note")       # nombre d'étoiles

    if avis and note:
        contenu = f"{note} étoiles : {avis}"

        conn = sqlite3.connect("database.db")
        conn.execute("INSERT INTO avis (texte) VALUES (?)", (contenu,))
        conn.commit()
        conn.close()

    return redirect("/")

@app.route("/avis")
def afficher_avis():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT texte FROM avis ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()
    return render_template("avis.html", avis_list=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
