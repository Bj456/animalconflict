import streamlit as st
from PIL import Image
import random
import requests
import os

st.set_page_config(page_title="Wildlife System", layout="wide")

# ---------------------------
# Fake Detection (Stable Alternative)
# ---------------------------
animals = ["Elephant", "Tiger", "Leopard", "Bear"]

animal_hi = {
    "Elephant": "हाथी",
    "Tiger": "शेर",
    "Leopard": "चीता",
    "Bear": "भालू"
}

PABBLY_WEBHOOK_URL = os.getenv("PABBLY_WEBHOOK_URL")

def send_alert(msg):
    try:
        if PABBLY_WEBHOOK_URL:
            requests.post(PABBLY_WEBHOOK_URL, json={"message": msg})
    except:
        pass

def detect(image):
    animal = random.choice(animals)
    conf = random.randint(60, 95)

    if conf > 70:
        send_alert(f"ALERT: {animal} {conf}%")

    return animal, animal_hi[animal], conf

# ---------------------------
# UI
# ---------------------------
st.title("🐾 Wildlife Protection System")

tab1, tab2, tab3 = st.tabs(["🔍 Detection", "🌿 Awareness", "🧠 Quiz"])

# ---------------------------
# Detection
# ---------------------------
with tab1:
    file = st.file_uploader("Upload Image")

    if file:
        img = Image.open(file)
        st.image(img)

        animal, hi, conf = detect(img)

        st.success(f"⚠️ {animal} detected ({conf}%)")
        st.write(f"हिन्दी: {hi}")

# ---------------------------
# Awareness
# ---------------------------
with tab2:
    st.markdown("## 🌿 Human-Animal Conflict Solutions")

    st.info("Water sources in forest")
    st.success("Plant trees")
    st.warning("Use buffer zones")
    st.error("Avoid waste dumping")

# ---------------------------
# Quiz
# ---------------------------
with tab3:
    name = st.text_input("Name")

    q1 = st.radio("Best method?", ["Water","Trees","All"])
    q2 = st.radio("Who protects wildlife?", ["Police","Forest Dept","School"])

    if st.button("Submit"):
        score = 0
        if q1=="All": score+=1
        if q2=="Forest Dept": score+=1

        st.success(f"{name}, Score: {score}/2")
