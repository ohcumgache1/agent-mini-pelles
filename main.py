import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

st.title("🚜 Agent de Recherche Mini-Pelles")
st.markdown("Recherche multi-sites automatisée (Agriaffaires, Mascus, Europe-TP, LBC...)")

st.header("🎯 Critères de recherche")

# Fourchettes de prix et de poids
col1, col2 = st.columns(2)
with col1:
    prix_min = st.number_input("Prix Min (€)", value=3000, step=500)
    prix_max = st.number_input("Prix Max (€)", value=13000, step=500)
with col2:
    poids_min = st.number_input("Poids Min (Tonnes)", value=2.0, step=0.5)
    poids_max = st.number_input("Poids Max (Tonnes)", value=3.5, step=0.5)

ville = st.text_input("Ville / Région / Code Postal", value="Gironde")
keyword = st.text_input("Marque / Mot-clé (ex: Kubota, Yanmar, Takeuchi)", value="Kubota")

st.header("📲 Configuration Telegram")
telegram_token = st.text_input("Token du Bot Telegram", value="9081199396:AAFOHCKqkgUjry7VWgz4ihmAZ37_3icAfGs", type="password")
chat_id = st.text_input("Chat ID Telegram", value="9245058131")

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {"ok": False, "description": str(e)}

def chercher_annonces_web(mot_cle, p_min, p_max, loc):
    # Formate la requête pour cibler les sites de vente de matériel BTP / Agricole
    query = f"mini pelle {mot_cle} {loc} {p_min}..{p_max} euro (site:agriaffaires.com OR site:europe-tp.com OR site:mascus.fr OR site:leboncoin.fr)"
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        resultats = []
        for a in soup.find_all("a", class_="result__url", limit=5):
            lien = a.get("href")
            titre = a.text.strip()
            if lien:
                resultats.append({"titre": titre, "url": lien})
        return resultats
    except Exception as e:
        st.error(f"Erreur lors de la recherche : {e}")
        return []

if st.button("🔍 Lancer la recherche ciblée"):
    st.info(f"Scan du web pour mini-pelles {keyword} ({poids_min}t-{poids_max}t) autour de {ville}...")
    
    annonces = chercher_annonces_web(keyword, prix_min, prix_max, ville)
    
    if annonces:
        st.success(f"Déniché {len(annonces)} résultat(s) sur le web !")
        
        message_telegram = f"🚨 *Trouvé sur le Web ({ville}) :*\n\n"
        for idx, ann in enumerate(annonces, 1):
            st.write(f"**{idx}.** [{ann['titre']}]({ann['url']})")
            message_telegram += f"🔹 [{ann['titre']}]({ann['url']})\n"
        
        # Envoi sur Telegram
        res = send_telegram_message(telegram_token, chat_id, message_telegram)
        if res.get("ok"):
            st.success("Alertes envoyées sur Telegram !")
        else:
            st.warning("Résultats affichés, mais échec d'envoi Telegram.")
    else:
        st.warning("Aucune nouvelle annonce exacte trouvée avec ces filtres stricts. Essaye d'élargir le mot-clé.")
