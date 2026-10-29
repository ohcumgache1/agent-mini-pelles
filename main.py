import streamlit as st

st.title("🚜 Agent de Recherche Mini-Pelles")
st.markdown("Recherche automatisée, filtrée et ciblée près de chez vous.")

st.header("🎯 Critères de recherche")

# Fourchettes de prix et de poids sur deux colonnes pour que ce soit propre
col1, col2 = st.columns(2)
with col1:
    prix_min = st.number_input("Prix Min (€)", value=0, step=500)
    prix_max = st.number_input("Prix Max (€)", value=13000, step=500)
with col2:
    poids_min = st.number_input("Poids Min (Tonnes)", value=1.0, step=0.5)
    poids_max = st.number_input("Poids Max (Tonnes)", value=6.5, step=0.5)

ville = st.text_input("Ville / Région / Code Postal", value="Bordeaux")
keyword = st.text_input("Mot-clé optionnel (ex: Kubota, pouce, attache rapide)")

with st.expander("📲 Configuration des alertes Telegram"):
    telegram_token = st.text_input("Token du Bot Telegram", type="password")
    chat_id = st.text_input("Chat ID Telegram", value="9245058131")

if st.button("🔍 Lancer la recherche ciblée"):
    st.success("Recherche lancée avec les nouveaux filtres !")
