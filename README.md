import streamlit as st
from groq import Groq
st.set_page_config(page_title="Mon IA Pikine", page_icon="🤖")
st.title("🤖 Mon IA Perso - Pikine")
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("Clé GROQ_API_KEY manquante!")
    st.stop()
client = Groq(api_key=api_key)
if "messages" not in st.session_state:
    st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
if prompt := st.chat_input("Pose ta question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=st.session_state.messages)
        answer = response.choices[0].message.content
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer}) 
