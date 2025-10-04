from flask import *
from datetime import datetime
import json
import sqlite3
import webbrowser
import os
import psycopg2

app = Flask(__name__)
app.secret_key = "une_cle_secrete"  # Obligatoire pour flash

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
    avis = request.form.get("star")       # texte de l'avis
    note = request.form.get("avis")       # nombre d'étoiles

    if avis or note:
        contenu = f"{note} étoiles : {avis}"

        conn = sqlite3.connect("postgresql://avis_5iyd_user:mFFNunuA1B0ymaJ60VlhtiFLdjEYhatZ@dpg-d3gjlhe3jp1c73er6ptg-a/avis_5iyd")
        conn.execute("INSERT INTO avis (texte) VALUES (?)", (contenu,))
        conn.commit()
        conn.close()
        
    return redirect("/")

@app.route("/avis")
def afficher_avis():
    conn = sqlite3.connect("postgresql://avis_5iyd_user:mFFNunuA1B0ymaJ60VlhtiFLdjEYhatZ@dpg-d3gjlhe3jp1c73er6ptg-a/avis_5iyd")
    cur = conn.cursor()
    cur.execute("SELECT texte FROM avis ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()
    return render_template("avis.html", avis_list=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
