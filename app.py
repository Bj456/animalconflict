import streamlit as st
from ultralytics import YOLO
import requests
import os

# ---------------------------
# Pabbly Webhook Configuration
# ---------------------------
PABBLY_WEBHOOK_URL = "https://connect.pabbly.com/workflow/sendwebhookdata/IjU3NjcwNTZkMDYzZjA0M2M1MjZjNTUzNDUxMzAi_pc"

def send_alert_via_pabbly(message: str):
    try:
        response = requests.post(PABBLY_WEBHOOK_URL, json={"message": message}, timeout=10)
        response.raise_for_status()
        st.success("✅ Alert sent via Pabbly!")
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Failed to send alert via Pabbly: {e}")

# ---------------------------
# Load YOLO Model
# ---------------------------
@st.cache_resource
def load_model():
    return YOLO("yolov8n-cls.pt")

model = load_model()

# ---------------------------
# Hindi Names
# ---------------------------
animal_name_hi = {
    "brown_bear": "भालू",
    "tiger": "शेर",
    "elephant": "हाथी",
    "leopard": "चीता",
    "wolf": "भेड़िया"
}

# ---------------------------
# Prediction Function
# ---------------------------
def predict(image_path):
    results = model.predict(source=image_path, verbose=False, save=True, project="runs", name="detect")
    result = results[0]

    if result.probs is None:
        return None, None, None

    pred_class = result.probs.top1
    conf = result.probs.top1conf.item() * 100

    animal_en = result.names[pred_class]
    animal_hi = animal_name_hi.get(animal_en, animal_en)

    # Send alert
    alert_message = f"🐾 ALERT: {animal_en.upper()} detected with confidence {conf:.1f}%"
    send_alert_via_pabbly(alert_message)

    return animal_en, animal_hi, conf

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Wildlife Detection System", layout="wide")

st.markdown("<h1 style='text-align:center;'>🐾 Wildlife Detection System 2026</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📷 Upload Photo", "🎥 Live Camera"])

# ---- Tab 1: Upload Photo ----
with tab1:
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        with open("temp.jpg", "wb") as f:
            f.write(uploaded_file.read())

        st.image("temp.jpg", caption="Uploaded Image", use_column_width=True)

        animal_en, animal_hi, conf = predict("temp.jpg")

        if animal_en:
            st.markdown(f"## ⚠️ ALERT: {animal_en.upper()}")
            st.write(f"Confidence: **{conf:.1f}%**")
            st.write(f"**हिन्दी:** यह {animal_hi} हो सकता है।")

            st.audio("alert.mp3", autoplay=True)

            # Show annotated detection result
            det_path = "runs/detect/predict/temp.jpg"
            if os.path.exists(det_path):
                st.image(det_path, caption="Detection Result", use_column_width=True)
        else:
            st.error("❌ Detection failed.")

# ---- Tab 2: Live Camera ----
with tab2:
    camera_input = st.camera_input("Take a snapshot")
    if camera_input is not None:
        with open("live.jpg", "wb") as f:
            f.write(camera_input.getbuffer())

        st.image("live.jpg", caption="Live Snapshot", use_column_width=True)

        animal_en, animal_hi, conf = predict("live.jpg")

        if animal_en:
            st.markdown(f"## ⚠️ ALERT: {animal_en.upper()}")
            st.write(f"Confidence: **{conf:.1f}%**")
            st.write(f"**हिन्दी:** यह {animal_hi} हो सकता है।")

            st.audio("alert.mp3", autoplay=True)

            det_path = "runs/detect/predict/live.jpg"
            if os.path.exists(det_path):
                st.image(det_path, caption="Detection Result", use_column_width=True)
        else:
            st.error("❌ Detection failed.")
