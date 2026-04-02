import streamlit as st
from ultralytics import YOLO
import requests
import base64
import os

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="Wildlife System", layout="wide")

PABBLY_WEBHOOK_URL = os.getenv("PABBLY_WEBHOOK_URL")

model = YOLO("yolov8n.pt")

animal_name_hi = {
    "elephant": "हाथी",
    "bear": "भालू",
    "dog": "कुत्ता",
    "cat": "बिल्ली"
}

# ---------------------------
# ALERT FUNCTION
# ---------------------------
def send_alert(msg):
    try:
        if PABBLY_WEBHOOK_URL:
            requests.post(PABBLY_WEBHOOK_URL, json={"message": msg})
    except:
        pass

# ---------------------------
# AUDIO
# ---------------------------
def get_audio():
    if os.path.exists("alert.mp3"):
        with open("alert.mp3", "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# ---------------------------
# DETECTION
# ---------------------------
def detect(image_path):
    results = model.predict(source=image_path)
    r = results[0]

    if len(r.boxes) == 0:
        return None, None, None

    cls = int(r.boxes.cls[0])
    conf = float(r.boxes.conf[0]) * 100

    animal_en = model.names[cls]
    animal_hi = animal_name_hi.get(animal_en, animal_en)

    if conf > 70:
        send_alert(f"ALERT: {animal_en} {conf:.1f}%")

    return animal_en, animal_hi, conf

# ---------------------------
# UI HEADER
# ---------------------------
st.markdown("<h1 style='text-align:center;color:#1e3a8a;'>🐾 Wildlife Protection System</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔍 Detection", "🌿 Awareness", "🧠 Quiz"])

# ---------------------------
# TAB 1: DETECTION
# ---------------------------
with tab1:
    uploaded = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])

    if uploaded:
        with open("temp.jpg","wb") as f:
            f.write(uploaded.read())

        st.image("temp.jpg")

        with st.spinner("Detecting..."):
            animal_en, animal_hi, conf = detect("temp.jpg")

        if animal_en:
            color = "green" if conf>80 else "orange" if conf>50 else "red"

            st.markdown(f"""
            <div style='padding:20px;border:3px solid {color};border-radius:10px;'>
            <h2 style='color:{color};'>⚠️ {animal_en.upper()}</h2>
            <p>Confidence: {conf:.1f}%</p>
            <p>हिन्दी: {animal_hi}</p>
            </div>
            """, unsafe_allow_html=True)

            st.audio("alert.mp3")

        else:
            st.error("No detection")

# ---------------------------
# TAB 2: AWARENESS
# ---------------------------
with tab2:
    st.markdown("## 🌿 Human-Animal Conflict Awareness")

    cols = st.columns(3)

    tips = [
        "Water holes in forest",
        "Plant trees",
        "Buffer zone",
        "Waste management",
        "Solar lights",
        "Protect animals"
    ]

    for i, tip in enumerate(tips):
        cols[i%3].info(tip)

# ---------------------------
# TAB 3: QUIZ
# ---------------------------
with tab3:
    st.markdown("## 🧠 Quiz")

    name = st.text_input("Enter Name")

    q1 = st.radio("Best method?", ["Water","Trees","All"])
    q2 = st.radio("Who protects wildlife?", ["Police","Forest Dept","School"])

    if st.button("Submit"):
        score = 0
        if q1=="All": score+=1
        if q2=="Forest Dept": score+=1

        st.success(f"{name} Score: {score}/2")
