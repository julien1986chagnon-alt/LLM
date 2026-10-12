import os
import streamlit as st
from pypdf import PdfReader
import collections

# Configurer la page web Streamlit
st.set_page_config(page_title="Scanner Universel IA", page_icon="🔍", layout="wide")
st.title("🔍 Votre Scanner Documentaire Universel")
st.subheader("Algorithme local - Extraction automatique des points forts de vos PDF")

# INTERFACE DE TÉLÉCHARGEMENT
fichier_uploade = st.file_uploader("Déposez votre rapport ou contrat (Format PDF)", type=["pdf"])

question_utilisateur = st.text_input(
    "Que voulez-vous extraire ou comprendre de ce document ?",
    value="Fais-moi un résumé exécutif des points forts et des risques majeurs."
)

# Moteur de résumé local et gratuit (sans clé API)
def generer_resume_local(texte, nb_phrases=5):
    # Nettoyage rapide du texte
    mots = [mot.lower() for mot in texte.split() if mot.isalnum() and len(mot) > 3]
    # Compter la fréquence des mots pour trouver les sujets importants
    frequence_mots = collections.Counter(mots)
    
    if not frequence_mots:
        return "Le document ne contient pas assez de texte lisible."
        
    frequence_max = max(frequence_mots.values())
    
    # Noter l'importance de chaque mot
    for mot in frequence_mots:
        frequence_mots[mot] = frequence_mots[mot] / frequence_max
        
    # Découpage grossier en phrases
    phrases = texte.split('.')
    score_phrases = {}
    
    for phrase in phrases:
        for mot in phrase.lower().split():
            if mot in frequence_mots:
                if phrase not in score_phrases:
                    score_phrases[phrase] = frequence_mots[mot]
                else:
                    score_phrases[phrase] += frequence_mots[mot]
                    
    # Sélectionner les meilleures phrases du document
    meilleures_phrases = sorted(score_phrases, key=score_phrases.get, reverse=True)[:nb_phrases]
    return "\n\n".join([f"• {p.strip()}" for p in meilleures_phrases if p.strip()])

if fichier_uploade is not None:
    if st.button("Lancer le scan flash ⚡"):
        with st.spinner("⚡ Analyse mathématique locale du document en cours..."):
            try:
                # EXTRACTION DU TEXTE DU PDF
                lecteur = PdfReader(fichier_uploade)
                texte_complet = ""
                for page in lecteur.pages:
                    texte_complet += page.extract_text() + "\n"
                
                # Génération du résumé directement sur la machine
                output = generer_resume_local(texte_complet)
                
                # AFFICHAGE DU RÉSULTAT
                st.markdown("### 📊 Synthèse Exécutive Directe")
                st.write(output)
                
            except Exception as e:
                st.error(f"Une erreur est survenue lors de l'analyse : {e}")
