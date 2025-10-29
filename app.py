import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# -------------------------------
# CONFIGURACIÓN MQTT
# -------------------------------
broker = "broker.mqttdashboard.com"
port = 1883
client_id = "nebula7_terminal"
topic_switch = "santiagoV/cmqtt_s"
topic_analog = "santiagoV/cmqtt_a"

# -------------------------------
# FUNCIONES CALLBACK
# -------------------------------
def on_publish(client, userdata, result):
    print("✅ Transmisión enviada al núcleo principal.")

def on_message(client, userdata, message):
    message_received = str(message.payload.decode("utf-8"))
    st.markdown(f"<span style='color:#00FFFF;'>📡 Transmisión recibida:</span> `{message_received}`", unsafe_allow_html=True)

# -------------------------------
# ESTILO FUTURISTA
# -------------------------------
st.set_page_config(page_title="Nebula-7 Control Panel", page_icon="🪐", layout="centered")

st.markdown("""
    <style>
    body {
        background: radial-gradient(circle at 20% 20%, #0f2027, #203a43, #2c5364);
        color: #00ffff;
        font-family: 'Share Tech Mono', monospace;
    }
    .stButton>button {
        background-color: #0b132b;
        color: #00ffff;
        border: 2px solid #00ffff;
        border-radius: 12px;
        padding: 0.6em 1.2em;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1b2a4e;
        color: #76e3ff;
        box-shadow: 0 0 15px #00ffff;
    }
    .stSlider > div[data-baseweb="slider"] {
        color: #00ffff;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# INTERFAZ DE USUARIO
# -------------------------------
st.title("🪐 Estación Nebula-7")
st.markdown("### Panel de control del **núcleo cuántico**")
st.markdown("---")

st.write(f"🧠 Sistema operativo: `{platform.system()} {platform.release()}`")
st.write(f"📡 Broker activo: `{broker}:{port}`")

st.markdown("---")

# -------------------------------
# BOTONES DE CONTROL
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("⚡ ACTIVAR REACTOR"):
        client = paho.Client(client_id)
        client.on_publish = on_publish
        client.connect(broker, port)
        msg = json.dumps({"Act1": "ON"})
        client.publish(topic_switch, msg)
        st.success("🟢 Reactor cuántico activado")

with col2:
    if st.button("🛑 DESACTIVAR REACTOR"):
        client = paho.Client(client_id)
        client.on_publish = on_publish
        client.connect(broker, port)
        msg = json.dumps({"Act1": "OFF"})
        client.publish(topic_switch, msg)
        st.error("🔴 Reactor cuántico detenido")

# -------------------------------
# CONTROL ANALÓGICO
# -------------------------------
st.markdown("---")
st.markdown("### ⚙️ Regulador de energía")

value = st.slider("Nivel de potencia del núcleo (%)", 0.0, 100.0, 50.0)
st.markdown(f"🔋 Energía establecida en: **{value}%**")

if st.button("🚀 Transmitir valor al núcleo"):
    client = paho.Client(client_id)
    client.on_publish = on_publish
    client.connect(broker, port)
    msg = json.dumps({"Analog": float(value)})
    client.publish(topic_analog, msg)
    st.info(f"📤 Transmisión enviada con potencia {value}%")

# -------------------------------
# PIE DE PÁGINA
# -------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#00ffff; font-size:13px;'>"
    "Terminal Nebula-7 v1.0 — Control remoto de sistemas cuánticos MQTT.<br>"
    "Diseño temático por Santiago Velásquez 🪐"
    "</p>",
    unsafe_allow_html=True
)
