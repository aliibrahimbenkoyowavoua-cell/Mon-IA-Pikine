 import streamlit as st
from groq import Groq

st.set_page_config(page_title="Mon IA Perso", page_icon="🤖")
st.title("🤖 Mon IA Perso - Pikine")

# Récupère la clé de façon sécurisée
# En local: depuis la barre à gauche, en ligne: depuis les Secrets
api_key = st.secrets.get("GROQ_API_KEY") if "GROQ_API_KEY" in st.secrets else None

if not api_key:
    api_key = st.sidebar.text_input("Mets ta clé Groq ici", type="password")
    st.sidebar.info("Ta clé est cachée et sécurisée.")

if not api_key:
    st.warning("👈 Mets ta clé Groq à gauche pour commencer!")
    st.stop()

client = Groq(api_key=api_key)

# Mémoire de la conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Pose ta question ici...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role": "user", "content": prompt}],
            )
            reponse = completion.choices[0].message.content
            st.markdown(reponse)
            st.session_state.messages.append({"role": "assistant", "content": reponse})
        except Exception as e:
            st.error(f"Erreur : {e}")