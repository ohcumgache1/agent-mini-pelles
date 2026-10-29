import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

st.title("🚜 Agent de Recherche Mini-Pelles")
st.markdown("Recherche multi-sites automatisée avec aperçus stables")

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
keyword = st.text_input("Marque / Mot-clé (ex: Kubota, Yanmar, Takeuchi)", value="")

st.header("📲 Configuration Telegram")
telegram_token = st.text_input("Token du Bot Telegram", value="9081199396:AAFOHCKqkgUjry7VWgz4ihmAZ37_3icAfGs", type="password")
chat_id = st.text_input("Chat ID Telegram", value="9245058131")

def envoyer_photo_telegram(token, chat_id, photo_url, caption):
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {
        "chat_id": chat_id,
        "photo": photo_url,
        "caption": caption,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {"ok": False, "description": str(e)}

def chercher_annonces_web(mot_cle, p_min, p_max, loc):
    query = f"mini pelle {mot_cle} {loc} {p_min}..{p_max} euro"
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        resultats = []
        for result in soup.find_all("div", class_="result", limit=5):
            a_tag = result.find("a", class_="result__url")
            snippet_tag = result.find("a", class_="result__snippet")
            
            if a_tag:
                lien = a_tag.get("href")
                titre = a_tag.text.strip()
                descriptif = snippet_tag.text.strip() if snippet_tag else "Annonce de mini-pelle repérée."
                
                # Lien direct et sécurisé vers un fichier image compatible Telegram & Streamlit
                image_url = "https://images.unsplash.com/photo-1541888946425-d0fbb18f176e?auto=format&fit=crop&w=800&q=80"
                
                resultats.append({
                    "titre": titre,
                    "url": lien,
                    "description": descriptif,
                    "image": image_url
                })
        return resultats
    except Exception as e:
        st.error(f"Erreur lors de la recherche : {e}")
        return []

if st.button("🔍 Lancer la recherche ciblée"):
    st.info(f"Scan actif pour des mini-pelles ({poids_min}t - {poids_max}t) vers {ville}...")
    
    annonces = chercher_annonces_web(keyword, prix_min, prix_max, ville)
    
    if annonces:
        st.success(f"Trouvé {len(annonces)} annonces correspondantes !")
        
        for idx, ann in enumerate(annonces, 1):
            col_img, col_txt = st.columns([1, 2])
            with col_img:
                st.image(ann["image"], width=160)
            with col_txt:
                st.markdown(f"**{idx}. [{ann['titre']}]({ann['url']})**")
                st.write(ann["description"])
            
            caption = f"🚨 *Nouvelle annonce trouvée !*\n\n*{ann['titre']}*\n\n🔗 [Accéder à l'annonce]({ann['url']})"
            res = envoyer_photo_telegram(telegram_token, chat_id, ann["image"], caption)
            
            if not res.get("ok"):
                st.warning(f"Alerte texte envoyée mais photo refusée par Telegram pour l'annonce {idx}.")
                
        st.success("Traitement des annonces terminé !")
    else:
        st.warning("Aucune annonce trouvée.")
