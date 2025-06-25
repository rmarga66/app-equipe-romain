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
    st.write("👋 Interface encore en construction... modules à venir !")
