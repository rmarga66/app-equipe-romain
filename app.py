
import streamlit as st
from supabase import create_client
from datetime import date, datetime

SUPABASE_URL = "https://kmkrtxkxovcyhrezxche.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtta3J0eGt4b3ZjeWhyZXp4Y2hlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA4NTA3MDcsImV4cCI6MjA2NjQyNjcwN30.f3IkPlgUPuGauXMyOgmi5mWAfCTh_lWmw750X5jlveM"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def login():
    st.title("Connexion à l'Espace Équipe")
    email = st.text_input("Messagerie électronique")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        try:
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            st.session_state['user'] = user
            st.success("Connecté !")
            st.experimental_rerun()
        except Exception as e:
            st.error("Erreur de connexion")

if "user" not in st.session_state:
    login()
else:
    user_email = st.session_state['user']['user']['email']
    user_id = st.session_state['user']['user']['id']
    st.sidebar.success(f"Connecté : {user_email}")
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
                "user_id": user_id,
                "date": str(date.today()),
                "humeur": humeur,
                "commentaire": commentaire
            }).execute()
            st.success("Humeur enregistrée !")

    elif choix == "Boîte à idées":
        st.title("💡 Boîte à idées")
        with st.form("idée_form"):
            donnee = st.text_input("1. Donnée (constat)")
            action = st.text_input("2. Action proposée")
            resultat = st.text_input("3. Résultat attendu")
            submitted = st.form_submit_button("Soumettre l'idée")
            if submitted:
                supabase.table("ideas").insert({
                    "user_id": user_id,
                    "donnee": donnee,
                    "action": action,
                    "resultat": resultat,
                    "status": "En attente"
                }).execute()
                st.success("Idée enregistrée !")

        st.subheader("📂 Idées de l'équipe")
        data = supabase.table("ideas").select("*").eq("user_id", user_id).execute()
        for row in data.data:
            st.markdown(f"**📝 Donnée :** {row['donnee']}  \n**⚙️ Action :** {row['action']}  \n**✅ Résultat :** {row['resultat']}  \n**Statut :** {row['status']}")
            st.markdown("---")

    elif choix == "Tâches":
        st.title("✅ Tâches")
        with st.form("form_task"):
            titre = st.text_input("Titre de la tâche")
            deadline = st.date_input("Deadline")
            assigne = st.text_input("Nom du collaborateur")
            if st.form_submit_button("Ajouter la tâche"):
                supabase.table("tasks").insert({
                    "titre": titre,
                    "deadline": str(deadline),
                    "assigné": assigne,
                    "statut": "À faire"
                }).execute()
                st.success("Tâche ajoutée.")

        st.subheader("📋 Tâches en cours")
        tasks = supabase.table("tasks").select("*").execute()
        for t in tasks.data:
            st.markdown(f"**🔹 {t['titre']}** — assigné à {t['assigné']} pour le {t['deadline']} — *{t['statut']}*")
            st.markdown("---")

    elif choix == "RDV":
        st.title("📅 Demande de RDV")
        sujet = st.text_input("Sujet du RDV")
        date_rdv = st.date_input("Date souhaitée")
        commentaire = st.text_area("Commentaires")
        if st.button("Demander RDV"):
            supabase.table("rdv").insert({
                "user_id": user_id,
                "sujet": sujet,
                "date": str(date_rdv),
                "commentaire": commentaire
            }).execute()
            st.success("RDV demandé. Visible uniquement par le manager.")

    elif choix == "Déconnexion":
        st.session_state.clear()
        st.experimental_rerun()
