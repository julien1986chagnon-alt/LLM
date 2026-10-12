import os
import streamlit as st
from pypdf import PdfReader
from huggingface_hub import InferenceClient

# Configurer la page web Streamlit
st.set_page_config(page_title="Scanner Universel IA", page_icon="🔍", layout="wide")
st.title("🔍 Votre Scanner Documentaire Universel")
st.subheader("Pilotez votre IA pour extraire les points forts de vos PDF")

# Initialisation sécurisée pour Hugging Face
@st.cache_resource
def initialiser_ia():
    try:
        # Récupération du jeton gratuit depuis les Secrets de Streamlit
        token_hf = st.secrets["HF_TOKEN"]
        # Utilisation de l'API sans modèle forcé (sélectionne le meilleur modèle de chat disponible)
        return InferenceClient(token=token_hf)
    except Exception as e:
        st.error(f"Erreur d'initialisation de l'API : {e}")
        return None

ia_client = initialiser_ia()

# INTERFACE DE TÉLÉCHARGEMENT
fichier_uploade = st.file_uploader("Déposez votre rapport ou contrat (Format PDF)", type=["pdf"])

question_utilisateur = st.text_input(
    "Que voulez-vous extraire ou comprendre de ce document ?",
    value="Fais-moi un résumé exécutif des points forts et des risques majeurs."
)

if fichier_uploade is not None and ia_client is not None:
    if st.button("Lancer le scan flash ⚡"):
        with st.spinner("⚡ L'IA analyse le document en cours..."):
            try:
                # EXTRACTION DU TEXTE DU PDF
                lecteur = PdfReader(fichier_uploade)
                texte_complet = ""
                for page in lecteur.pages:
                    texte_complet += page.extract_text() + "\n"
                
                # PROMPT POUR LE MODÈLE
                prompt_pilote = f"""
Tu es un expert en synthèse documentaire. Réponds en français en te basant UNIQUEMENT sur le texte fourni ci-dessous. Va droit au but, élimine le jargon inutile et utilise des puces claires pour structurer ta réponse.

DOCUMENT :
{texte_complet}

QUESTION DE L'UTILISATEUR :
{question_utilisateur}
"""

                # CORRECTION MAJEURE : Utilisation de chat_completion au lieu de text_generation
                reponse = ia_client.chat_completion(
                    messages=[{"role": "user", "content": prompt_pilote}],
                    max_tokens=1024
                )
                output = reponse.choices[0].message.content
                
                # AFFICHAGE DU RÉSULTAT
                st.markdown("### 📊 Synthèse Exécutive")
                st.write(output)
                
            except Exception as e:
                st.error(f"Une erreur est survenue lors de l'analyse : {e}")
