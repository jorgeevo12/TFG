import streamlit as st
import requests
from pathlib import Path

st.set_page_config(page_title="TFG Chatbot - Interfaz", layout="centered")
st.title("🤖 Chatbot TFG con Rasa")

st.markdown("Esta interfaz te permite interactuar con el modelo de Rasa entrenado para DIHANA o MULTIWOZ (PATH_A).")

# Selección de corpus
selected = st.selectbox("Selecciona el corpus:", ["DIHANA", "MULTIWOZ"])

# Definición del endpoint según corpus (puedes cambiar el puerto si los sirves por separado)
ENDPOINTS = {
    "DIHANA": "http://localhost:5005/webhooks/rest/webhook",
    "MULTIWOZ": "http://localhost:5006/webhooks/rest/webhook"
}

rasa_url = ENDPOINTS[selected]

st.subheader("📁 Archivos del chatbot")

# Mostrar domain.yml
domain_file = Path(f"../{selected.lower()}_chatbot/chatbot_generated/domain.yml").resolve()
if domain_file.exists():
    with st.expander("domain.yml"):
        st.code(domain_file.read_text(encoding="utf-8"), language="yaml")
else:
    st.warning("domain.yml no encontrado.")

# Mostrar archivos en data/
data_dir = Path(f"../{selected.lower()}_chatbot/chatbot_generated/data").resolve()
for name in ["nlu.yml", "rules.yml", "stories.yml"]:
    file_path = data_dir / name
    if file_path.exists():
        with st.expander(name):
            st.code(file_path.read_text(encoding="utf-8"), language="yaml")
    else:
        st.warning(f"{name} no encontrado.")

# Historial de conversación
if "chat" not in st.session_state:
    st.session_state.chat = []

st.subheader(f"💬 Conversación con el modelo {selected}")

# Entrada de usuario
user_input = st.text_input("Tu mensaje:", key="input")

def send_to_rasa(msg):
    payload = {
        "sender": "usuario_tfg",
        "message": msg
    }
    try:
        res = requests.post(rasa_url, json=payload)
        res.raise_for_status()
        data = res.json()
        return "\n".join([d["text"] for d in data if "text" in d])
    except Exception as e:
        return f"❌ Error al conectar con Rasa: {e}"

# Botón de envío
if st.button("Enviar") and user_input.strip():
    st.session_state.chat.append(("🧑 Tú", user_input))
    response = send_to_rasa(user_input)
    st.session_state.chat.append(("🤖 Bot", response))

# Mostrar conversación
for speaker, msg in st.session_state.chat:
    st.markdown(f"**{speaker}**: {msg}")
