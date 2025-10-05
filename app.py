from flask import *
from datetime import datetime
import json
import sqlite3
import webbrowser
import os
import psycopg2

app = Flask(__name__)
DB_URL = "postgresql://avis_5iyd_user:mFFNunuA1B0ymaJ60VlhtiFLdjEYhatZ@dpg-d3gjlhe3jp1c73er6ptg-a/avis_5iyd"  # Obligatoire pour flash
app.secret_key = "une_cle_secrete"

def get_connection():
    return psycopg2.connect(DB_URL)

# Créer la table "avis" si elle n'existe pas
def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS avis (
            id SERIAL PRIMARY KEY,
            texte TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

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
    avis = request.form.get("star")
    note = request.form.get("note")

    if avis or note:
        contenu = f"{avis} étoiles : {note}"

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO avis (texte) VALUES (%s)", (contenu,))
        conn.commit()
        conn.close()

        flash("✅ Votre avis a bien été enregistré !", "success")

    return redirect("/")

@app.route("/avis")
def afficher_avis():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT texte FROM avis ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()
    
    return render_template("avis.html", avis_list=data)

@app.route("/reset_avis")
def reset_avis():
    try:
        DB_URL = "postgresql://avis_5iyd_user:mFFNunuA1B0ymaJ60VlhtiFLdjEYhatZ@dpg-d3gjlhe3jp1c73er6ptg-a/avis_5iyd"
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("TRUNCATE TABLE avis RESTART IDENTITY;")
        conn.commit()
        conn.close()
        flash("✅ Tous les avis ont été supprimés avec succès !")
    except Exception as e:
        flash(f"⚠️ Erreur : {e}")
    return redirect("/avis")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
