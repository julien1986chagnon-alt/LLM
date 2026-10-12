import os
import streamlit as st
from pypdf import PdfReader
from google import genai
from google.genai import types

# Configurer la page web Streamlit
st.set_page_config(page_title="Scanner Universel IA", page_icon="🔍", layout="wide")
st.title("🔍 Votre Scanner Documentaire Universel")
st.subheader("Pilotez votre IA pour extraire les points forts de vos PDF")

# Initialisation directe avec la clé API Google Gemini
@st.cache_resource
def initialiser_ia():
    try:
        # Récupération sécurisée depuis les Secrets de Streamlit
        cle_api = st.secrets["GEMINI_API_KEY"]
        return genai.Client(api_key=cle_api)
    except Exception as e:
        st.error(f"Erreur d'initialisation de l'API : {e}")
        return None


gemini_client = initialiser_ia()

# 2. INTERFACE DE TÉLÉCHARGEMENT (PILOTAGE)
fichier_uploade = st.file_uploader("Déposez votre rapport ou contrat (Format PDF)", type=["pdf"])

question_utilisateur = st.text_input(
    "Que voulez-vous extraire ou comprendre de ce document ?",
    value="Fais-moi un résumé exécutif des points forts et des risques majeurs."
)

if fichier_uploade is not None and gemini_client is not None:
    if st.button("Lancer le scan flash ⚡"):
        with st.spinner("⚡ L'IA analyse le document en cours..."):
            try:
                # 3. EXTRACTION DU TEXTE DU PDF
                lecteur = PdfReader(fichier_uploade)
                texte_complet = ""
                for page in lecteur.pages:
                    texte_complet += page.extract_text() + "\n"
                
                # 4. PROMPT ENGINEERING DIRECT (Envoi du texte entier à Gemini)
                prompt_pilote = f"""
Tu es un expert en synthèse documentaire de haut niveau.
En te basant UNIQUEMENT sur le texte authentique fourni ci-dessous, réponds à la question de l'utilisateur.
Va droit au but, élimine le jargon inutile et utilise des puces claires (bullet points) pour structurer ta réponse.

EXTRAITS STRATÉGIQUES DU DOCUMENT :
{texte_complet}

QUESTION DE L'UTILISATEUR :
{question_utilisateur}
"""

                # 5. APPEL AU MODÈLE GEMINI FLASH
                reponse = gemini_client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt_pilote,
                )
                
                # 6. AFFICHAGE DU LIVRABLE À L'ÉCRAN
                st.markdown("### 📊 Synthèse Exécutive")
                st.write(reponse.text)
                
            except Exception as e:
                st.error(f"Une erreur est survenue lors de l'analyse : {e}")

