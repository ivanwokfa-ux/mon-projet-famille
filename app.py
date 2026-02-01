import streamlit as st
import sqlite3
import pandas as pd
import os

st.set_page_config(page_title="Mon Réseau Personnel", layout="centered")

def init_db():
    conn = sqlite3.connect('famille.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS membres 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prenom TEXT, role TEXT)''')
    conn.commit()
    conn.close()

init_db()

st.title("Système d'Authentification Personnel")
st.write("Veuillez entrer vos informations pour vérifier votre lien avec moi.")

# --- Zone de vérification ---
with st.container():
    nom_input = st.text_input("Nom :").upper().strip()
    prenom_input = st.text_input("Prénom :").capitalize().strip()
    
    if st.button("Lancer la vérification"):
        if nom_input and prenom_input:
            conn = sqlite3.connect('famille.db')
            query = "SELECT role FROM membres WHERE UPPER(nom) = ? AND PRENOM = ?"
            res = pd.read_sql_query(query, conn, params=(nom_input, prenom_input))
            conn.close()

            if not res.empty:
                resultat = res.iloc[0]['role']
                st.balloons()
                st.success(f"Identification réussie : {prenom_input}, tu es pour moi : **{resultat}**.")
            else:
                st.error("Identité non reconnue dans mon système.")
        else:
            st.warning("Informations manquantes.")

# --- Administration ---
with st.expander("Paramètres Système"):
    access_key = st.text_input("Clé d'accès :", type="password")
    if access_key == "ivan2024":
        st.subheader("Gestion des accès")
        with st.form("ajout_membre"):
            n_nom = st.text_input("Nom")
            n_prenom = st.text_input("Prénom")
            n_role = st.text_input("Définir le lien (ex: Amie, Cousin, etc.)")
            if st.form_submit_button("Enregistrer"):
                if n_nom and n_prenom and n_role:
                    conn = sqlite3.connect('famille.db')
                    c = conn.cursor()
                    c.execute('INSERT INTO membres (nom, prenom, role) VALUES (?,?,?)', 
                              (n_nom.upper().strip(), n_prenom.capitalize().strip(), n_role))
                    conn.commit()
                    conn.close()
                    st.success("Enregistrement effectué.")
        
        if st.checkbox("Voir la base de données"):
            conn = sqlite3.connect('famille.db')
            df = pd.read_sql_query("SELECT nom, prenom, role FROM membres", conn)
            conn.close()
            st.dataframe(df)
