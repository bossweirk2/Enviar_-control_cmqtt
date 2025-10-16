import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# -------------------------------
# CONFIGURACIÓN MQTT PERSONAL
# -------------------------------
broker = "157.230.214.127"     # Servidor MQTT del profesor
port = 1883                    # Puerto estándar MQTT
client_id = "santiagoV_app"    # Identificador único de cliente
topic_switch = "santiagoV/cmqtt_s"  # Tópico para ON/OFF
topic_analog = "santiagoV/cmqtt_a"  # Tópico para valores analógicos

# -------------------------------
# FUNCIONES CALLBACK
# -------------------------------
def on_publish(client, userdata, result):
    print("✅ Dato publicado con éxito\n")

def on_message(client, userdata, message):
    message_received = str(message.payload.decode("utf-8"))
    st.write("📩 Mensaje recibido:", message_received)

# -------------------------------
# INTERFAZ STREAMLIT
# -------------------------------
st.title("Control MQTT - Santiago Velásquez")
st.write("Versión de Python:", platform.python_version())
st.write("Broker:", broker)
st.write("Puerto:", port)

# -------------------------------
# BOTONES ON / OFF
# -------------------------------
if st.button("Encender (ON)"):
    client = paho.Client(client_id)
    client.on_publish = on_publish
    client.connect(broker, port)
    msg = json.dumps({"Act1": "ON"})
    client.publish(topic_switch, msg)
    st.success("Se envió la señal ON")

if st.button("Apagar (OFF)"):
    client = paho.Client(client_id)
    client.on_publish = on_publish
    client.connect(broker, port)
    msg = json.dumps({"Act1": "OFF"})
    client.publish(topic_switch, msg)
    st.warning("Se envió la señal OFF")

# -------------------------------
# SLIDER ANALÓGICO
# -------------------------------
value = st.slider("Selecciona un valor analógico", 0.0, 100.0)
st.write(f"Valor seleccionado: {value}")

if st.button("Enviar valor analógico"):
    client = paho.Client(client_id)
    client.on_publish = on_publish
    client.connect(broker, port)
    msg = json.dumps({"Analog": float(value)})
    client.publish(topic_analog, msg)
    st.info(f"Valor analógico {value} enviado correctamente")
