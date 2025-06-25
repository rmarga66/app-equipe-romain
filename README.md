
# Interface Équipe (Streamlit + Supabase)

## Fonctions
- Authentification par email (Supabase Auth)
- Interface Streamlit pour saisie d’humeur, RDV, idées, tâches
- Données stockées et sécurisées dans Supabase (PostgreSQL)

## Déploiement (Render ou local)
1. Cloner ce repo
2. Copier `.env.example` en `.env` et ajouter les vraies clés Supabase
3. Installer les dépendances :
```
pip install -r requirements.txt
```
4. Lancer l’app :
```
streamlit run app.py
```
