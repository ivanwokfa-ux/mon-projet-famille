import streamlit as st
import sqlite3
import pandas as pd
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Qui es-tu pour Ivan ?", layout="centered")

def get_connection():
    return sqlite3.connect('famille.db')

# Initialisation silencieuse de la base
conn = get_connection()
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS membres 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prenom TEXT, role TEXT)''')
conn.commit()
conn.close()

# --- INTERFACE D'AUTHENTIFICATION (Ce que les autres voient) ---
st.title("🕵️ Système de Reconnaissance d'Ivan")
st.write("Entre tes coordonnées pour découvrir notre lien.")

with st.container():
    auth_nom = st.text_input("Ton Nom de famille :").upper().strip()
    auth_prenom = st.text_input("Ton Prénom :").capitalize().strip()
    btn_auth = st.button("Vérifier mon identité")

if btn_auth:
    if auth_nom and auth_prenom:
        conn = get_connection()
        # On cherche si la personne existe dans ta liste pré-établie
        query = "SELECT role FROM membres WHERE UPPER(nom) = ? AND PRENOM = ?"
        res = pd.read_sql_query(query, conn, params=(auth_nom, auth_prenom))
        conn.close()

        if not res.empty:
            mon_lien = res.iloc[0]['role']
            st.balloons()
            st.success(f"### Analyse terminée : \n\n **{auth_prenom}**, tu es pour moi : **{mon_lien}** ! ✨")
        else:
            st.error("Désolé, tu ne fais pas encore partie de mon cercle reconnu. 🧐")
    else:
        st.warning("Veuillez remplir les deux champs.")

# --- SECTION ADMIN (Pour que TOI tu puisses enregistrer les gens au départ) ---
with st.expander("⚙️ Zone Administrateur (Pour Ivan uniquement)"):
    st.write("C'est ici que tu définis qui est qui.")
    with st.form("admin_form"):
        new_nom = st.text_input("Nom du proche")
        new_prenom = st.text_input("Prénom du proche")
        new_role = st.selectbox("Lien secret avec moi", [
            "Ma chère Maman ❤️", 
            "Mon super Papa 👑", 
            "Ma grande sœur adorée ✨", 
            "Une amie personnelle très proche 🌹", 
            "Une simple connaissance", 
            "Un de mes meilleurs amis 🎮",
            "C'est moi, Ivan ! 🚀"
        ])
        submit_admin = st.form_submit_button("Enregistrer ce lien")

    if submit_admin and new_nom and new_prenom:
        conn = get_connection()
        c = conn.cursor()
        c.execute('INSERT INTO membres (nom, prenom, role) VALUES (?,?,?)', 
                  (new_nom.upper().strip(), new_prenom.capitalize().strip(), new_role))
        conn.commit()
        conn.close()
        st.success(f"Lien établi pour {new_prenom} !")

    # Option pour voir ta liste actuelle
    if st.checkbox("Afficher ma liste de contacts"):
        conn = get_connection()
        df = pd.read_sql_query("SELECT nom, prenom, role FROM membres", conn)
        conn.close()
        st.dataframe(df)
