import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def login():
    st.title("Connexion à l'Espace Équipe")
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        try:
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            st.session_state['user'] = user
            st.success("Connecté !")
        except Exception as e:
            st.error("Erreur de connexion")

if "user" not in st.session_state:
    login()
else:
        st.success(f"Bienvenue {st.session_state['user']['user']['email']}")
    choix = st.sidebar.radio("📋 Menu", ["Accueil", "Humeur du jour", "Boîte à idées", "Tâches", "RDV", "Déconnexion"])

    if choix == "Accueil":
        st.title("🏠 Tableau de bord")
        st.write("Bienvenue dans l’espace manager.")
    
    elif choix == "Humeur du jour":
        st.title("🧠 Humeur du jour")
        humeur = st.slider("Ton humeur aujourd'hui ?", 1, 5, 3)
        commentaire = st.text_area("Un mot à dire ?")
        if st.button("Envoyer"):
            supabase.table("mood").insert({
                "user_id": st.session_state["user"]["user"]["id"],
                "date": str(date.today()),
                "humeur": humeur,
                "commentaire": commentaire
            }).execute()
            st.success("Humeur enregistrée !")
    
    elif choix == "Boîte à idées":
        st.title("💡 Boîte à idées")
        st.write("À venir : Donnée → Action → Résultat")

    elif choix == "Tâches":
        st.title("✅ Tâches")
        st.write("Module en cours de développement…")

    elif choix == "RDV":
        st.title("📅 Demande de RDV")
        st.write("Interface de demande de RDV ici…")

    elif choix == "Déconnexion":
        st.session_state.clear()
        st.experimental_rerun()
