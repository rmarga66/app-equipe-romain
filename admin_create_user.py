import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL=https://kmkrtxkxovcyhrezxche.supabase.co"), os.getenv("SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtta3J0eGt4b3ZjeWhyZXp4Y2hlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA4NTA3MDcsImV4cCI6MjA2NjQyNjcwN30.f3IkPlgUPuGauXMyOgmi5mWAfCTh_lWmw750X5jlveM
"))

st.title("👤 Création manuelle d’un utilisateur Supabase")

admin_email = st.text_input("Ton email Supabase (admin)")
admin_password = st.text_input("Ton mot de passe Supabase", type="password")

email = st.text_input("Email du nouvel utilisateur")
password = st.text_input("Mot de passe du nouvel utilisateur", type="password")

if st.button("Créer l'utilisateur"):
    try:
        admin_session = supabase.auth.sign_in_with_password({
            "email": admin_email,
            "password": admin_password
        })

        if admin_session:
            response = supabase.auth.admin.create_user({
                "email": email,
                "password": password,
                "email_confirm": True
            })
            st.success(f"Utilisateur {email} créé avec succès ✅")
        else:
            st.error("Connexion admin échouée")
    except Exception as e:
        st.error(f"Erreur : {e}")
