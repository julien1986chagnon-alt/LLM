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
        # Utilisation d'un excellent modèle open-source gratuit
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
                prompt_pilote = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
Tu es un expert en synthèse documentaire. Réponds en français en te basant UNIQUEMENT sur le texte fourni. Va droit au but.<|eot_id|><|start_header_id|>user<|end_header_id|>
DOCUMENT :
{texte_complet}

QUESTION :
{question_utilisateur}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

                # APPEL AU MODÈLE HUGGING FACE
                output = ia_client.text_generation(prompt_pilote, max_new_tokens=1024)
                
                # AFFICHAGE DU RÉSULTAT
                st.markdown("### 📊 Synthèse Exécutive")
                st.write(output)
                
            except Exception as e:
                st.error(f"Une erreur est survenue lors de l'analyse : {e}")
