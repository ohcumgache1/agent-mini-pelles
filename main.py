import streamlit as st
import requests

st.title("🚜 Agent de Recherche Mini-Pelles")
st.markdown("Recherche automatisée, filtrée et ciblée près de chez vous.")

st.header("🎯 Critères de recherche")

# Fourchettes de prix et de poids
col1, col2 = st.columns(2)
with col1:
    prix_min = st.number_input("Prix Min (€)", value=0, step=500)
    prix_max = st.number_input("Prix Max (€)", value=13000, step=500)
with col2:
    poids_min = st.number_input("Poids Min (Tonnes)", value=1.0, step=0.5)
    poids_max = st.number_input("Poids Max (Tonnes)", value=3.0, step=0.5)

ville = st.text_input("Ville / Région / Code Postal", value="Bordeaux")
keyword = st.text_input("Mot-clé optionnel (ex: Kubota, Hi-Top, Rippa)", value="")

st.header("📲 Configuration Telegram")
telegram_token = st.text_input("Token du Bot Telegram", value="9081199396:AAFOHKqKgUjry7VWGz4ihMAZ37_3icAFGs", type="password")
chat_id = st.text_input("Chat ID Telegram", value="9245058131")

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {"ok": False, "description": str(e)}

if st.button("🔍 Lancer la recherche ciblée"):
    st.info(f"Recherche en cours pour des mini-pelles entre {poids_min}t et {poids_max}t, de {prix_min}€ à {prix_max}€ autour de {ville}...")
    
    # Simulation du résultat ou appel de ton script de scraping
    # Ici, tu peux rajouter l'appel à ta fonction de recherche d'annonces
    
    result_message = f"🚜 *Recherche lancée* :\n- Localisation : {ville}\n- Poids : {poids_min}t - {poids_max}t\n- Budget max : {prix_max}€"
    
    # Envoi d'un test vers Telegram pour valider que tout est connecté
    res = send_telegram_message(telegram_token, chat_id, result_message)
    
    if res.get("ok"):
        st.success("Recherche effectuée et alerte Telegram bien envoyée !")
    else:
        st.warning(f"Recherche effectuée, mais l'envoi Telegram a échoué : {res.get('description')}")
