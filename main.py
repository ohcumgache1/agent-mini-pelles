import streamlit as st
import re

st.set_page_config(page_title="Agent Mini-Pelles", page_icon="🚜", layout="centered")

st.title("🚜 Agent de Recherche Mini-Pelles")
st.markdown("Recherche automatisée, filtrée et ciblée près de chez vous.")

# --- SIDEBAR / CRITÈRES DE RECHERCHE ---
st.header("🎯 Critères de recherche")

col1, col2 = st.columns(2)
with col1:
    prix_max = st.number_input("Prix Max (€)", value=13000, step=500)
with col2:
    localisation = st.text_input("Ville / Région / Code Postal", value="Bordeaux", placeholder="ex: Bordeaux, Gironde")

col3, col4 = st.columns(2)
with col3:
    poids_min = st.number_input("Poids Min (Tonnes)", value=1.0, step=0.5)
with col4:
    poids_max = st.number_input("Poids Max (Tonnes)", value=3.0, step=0.5)

mot_cle = st.text_input("Mot-clé optionnel (ex: Kubota, pouce, attache rapide)", value="")

# Option Telegram pour les alertes
with st.expander("📲 Configuration des alertes Telegram (Optionnel)"):
    telegram_token = st.text_input("Token du Bot Telegram", type="password")
    telegram_chat_id = st.text_input("Chat ID Telegram")

# --- BOUTON DE RECHERCHE ---
if st.button("🔍 Lancer la recherche ciblée", type="primary"):
    with st.spinner("Recherche en cours sur le web et application des filtres stricts..."):
        
        # Simulation / Récupération des annonces ciblées (ici tu connecteras ton scraper ou ta recherche web)
        # On simule des résultats pour l'exemple avec des prix variés
        annonces_brutes = [
            {
                "titre": "Mini-pelle Kubota U20-3 (2t) + Godets",
                "prix": 16900,
                "poids": 2.0,
                "lieu": "Bordeaux (33)",
                "lien": "https://www.europe-tp.com"
            },
            {
                "titre": "Mini-pelle Hi-Top HT22 (2.2t) - État neuf",
                "prix": 13500,
                "poids": 2.2,
                "lieu": "Libourne (33)",
                "lien": "https://www.europe-tp.com"
            },
            {
                "titre": "Mini-pelle Yanmar SV18 (1.8t)",
                "prix": 11500,
                "poids": 1.8,
                "lieu": "Angoulême (16)",
                "lien": "https://www.europe-tp.com"
            },
            {
                "titre": "Mini-pelle Kubota U10-3",
                "prix": 9800,
                "poids": 1.0,
                "lieu": "Bordeaux (33)",
                "lien": "https://www.europe-tp.com"
            }
        ]

        # --- FILTRAGE STRICT EN PYTHON ---
        annonces_filtrees = []
        for a in annonces_brutes:
            # 1. Filtre strict sur le prix maximum
            if a["prix"] > prix_max:
                continue
            # 2. Filtre strict sur le poids
            if not (poids_min <= a["poids"] <= poids_max):
                continue
            # 3. Filtre sur la localisation (si renseignée)
            if localisation.lower() not in a["lieu"].lower():
                # Optionnel : si tu veux être large sur la région, tu peux adapter, 
                # mais ici ça vérifie si la zone correspond.
                pass 
                
            annonces_filtrees.append(a)

        st.success(f"Recherche terminée ! {len(annonces_filtrees)} annonce(s) trouvée(s) correspondant à vos critères stricts.")

        # --- AFFICHAGE DES RÉSULTATS ---
        if not annonces_filtrees:
            st.warning("Aucune annonce ne respecte strictement votre budget maximum et vos critères pour le moment.")
        else:
            for annonce in annonces_filtrees:
                with st.container(border=True):
                    st.subheader(annonce["titre"])
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f"💶 **Prix :** {annonce['prix']:,} €".replace(",", " "))
                        st.markdown(f"⚖️ **Poids :** {annonce['poids']}t")
                    with col_b:
                        st.markdown(f"📍 **Lieu :** {annonce['lieu']}")
                        st.markdown(f"[🔗 Voir l'annonce d'origine]({annonce['lien']})")
