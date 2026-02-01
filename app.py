import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Mon Réseau Personnel", layout="centered")

def get_connection():
    return sqlite3.connect('famille.db')

# Initialisation
conn = get_connection()
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS membres 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prenom TEXT, role TEXT)''')
conn.commit()
conn.close()

st.title("Système d'Authentification Personnel")
st.write("Veuillez entrer vos informations pour vérifier votre lien avec moi.")

# --- Zone de vérification ---
with st.container():
    nom_input = st.text_input("Nom :").upper().strip()
    prenom_input = st.text_input("Prénom :").capitalize().strip()
    
    if st.button("Lancer la vérification"):
        if nom_input and prenom_input:
            conn = get_connection()
            query = "SELECT role FROM membres WHERE UPPER(nom) = ? AND PRENOM = ?"
            res = pd.read_sql_query(query, conn, params=(nom_input, prenom_input))
            conn.close()

            if not res.empty:
                resultat = res.iloc[0]['role']
                st.balloons()
                st.success(f"Identification réussie : {prenom_input}, tu es pour moi : **{resultat}**.")
            else:
                st.error("Identité non reconnue dans mon système.")

# --- Paramètres Système (ADMIN) ---
with st.expander("Paramètres Système"):
    access_key = st.text_input("Clé d'accès :", type="password")
    if access_key == "ivan2024":
        
        tab1, tab2, tab3 = st.tabs(["Ajouter", "Modifier", "Supprimer"])

        # TAB 1 : AJOUTER
        with tab1:
            with st.form("ajout"):
                n_nom = st.text_input("Nom")
                n_prenom = st.text_input("Prénom")
                n_role = st.text_input("Lien")
                if st.form_submit_button("Enregistrer"):
                    conn = get_connection()
                    c = conn.cursor()
                    c.execute('INSERT INTO membres (nom, prenom, role) VALUES (?,?,?)', 
                              (n_nom.upper().strip(), n_prenom.capitalize().strip(), n_role))
                    conn.commit()
                    conn.close()
                    st.success("Ajouté !")

        # TAB 2 : MODIFIER
        with tab2:
            conn = get_connection()
            df_mod = pd.read_sql_query("SELECT * FROM membres", conn)
            conn.close()
            if not df_mod.empty:
                liste_noms = df_mod['prenom'] + " " + df_mod['nom']
                choix = st.selectbox("Qui modifier ?", liste_noms)
                id_membre = df_mod.iloc[liste_noms.tolist().index(choix)]['id']
                
                new_role = st.text_input("Nouveau lien pour " + choix)
                if st.button("Mettre à jour"):
                    conn = get_connection()
                    c = conn.cursor()
                    c.execute('UPDATE membres SET role = ? WHERE id = ?', (new_role, int(id_membre)))
                    conn.commit()
                    conn.close()
                    st.success("Modifié !")
            else:
                st.info("Aucun membre.")

        # TAB 3 : SUPPRIMER
        with tab3:
            conn = get_connection()
            df_del = pd.read_sql_query("SELECT * FROM membres", conn)
            conn.close()
            if not df_del.empty:
                liste_del = df_del['prenom'] + " " + df_del['nom']
                a_supprimer = st.selectbox("Qui supprimer ?", liste_del)
                id_del = df_del.iloc[liste_del.tolist().index(a_supprimer)]['id']
                
                if st.button("Supprimer définitivement"):
                    conn = get_connection()
                    c = conn.cursor()
                    c.execute('DELETE FROM membres WHERE id = ?', (int(id_del),))
                    conn.commit()
                    conn.close()
                    st.warning("Membre supprimé.")
                    st.rerun()
