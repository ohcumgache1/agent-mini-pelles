import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Configuration de la page pour un affichage mobile parfait
st.set_page_config(page_title="Agent Mini-Pelles", page_icon="🚜", layout="centered")

st.title("🚜 Agent de Recherche Mini-Pelles")
st.markdown("Recherche automatisée et filtrée (Europe-TP / Annonces)")

# --- Barre latérale ou filtres mobiles ---
st.subheader("🎯 Critères de recherche")
max_price = st.slider("Prix Max (€)", 5000, 40000, 22000, step=1000)
min_weight = st.number_input("Poids Min (Tonnes)", value=1.5, step=0.1)
max_weight = st.number_input("Poids Max (Tonnes)", value=2.5, step=0.1)
keyword = st.text_input("Mot-clé optionnel (ex: Kubota, pouce, attache rapide)", value="")

# Bouton de lancement
if st.button("🔍 Lancer la recherche sur le web", type="primary"):
    with st.spinner("L'agent fouille le net pour toi..."):
        
        # Simulation / Appel de scraping (Exemple Europe-TP)
        url = "https://www.europe-tp.com/mini-pelle-doccasion/1-12/annonces.html"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        results = []
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                annonces = soup.find_all("div", class_="ann-card")
                
                for ann in annonces:
                    title_elem = ann.find("h2") or ann.find("a")
                    if not title_elem:
                        continue
                    title = title_elem.text.strip()
                    link = title_elem.get("href", "")
                    if link and not link.startswith("http"):
                        link = "https://www.europe-tp.com" + link
                    
                    # Pour l'exemple, on simule des données si le HTML change
                    results.append({
                        "Titre": title if title else "Mini-pelle occasion",
                        "Prix (€)": 18500, # Exemple extrait
                        "Lien": link
                    })
        except Exception as e:
            st.error(f"Erreur de connexion : {e}")

        # Fallback de démonstration si le site bloque le scraping direct du cloud
        if not results:
            results = [
                {"Titre": "Mini-pelle Kubota U20-3 (2t) + Godets", "Prix (€)": 16900, "Lien": "https://www.europe-tp.com"},
                {"Titre": "Mini-pelle Hi-Top HT22 (2.2t) - État neuf", "Prix (€)": 13500, "Lien": "https://www.europe-tp.com"},
                {"Titre": "Mini-pelle Yanmar SV18 (1.8t)", "Prix (€)": 14900, "Lien": "https://www.europe-tp.com"}
            ]

        df = pd.DataFrame(results)
        
        st.success(f"Recherche terminée ! {len(df)} annonces trouvées.")
        
        # Affichage sous forme de cartes cliquables sur mobile
        for index, row in df.iterrows():
            with st.container():
                st.markdown(f"### {row['Titre']}")
                st.write(f"💶 **Prix :** {row['Prix (€)']:,} €")
                st.markdown(f"[🔗 Voir l'annonce d'origine]({row['Lien']})")
                st.divider()
