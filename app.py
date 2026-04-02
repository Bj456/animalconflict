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
    results = model.predict(source=image_path, verbose=False)
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

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save temp file
    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.read())

    # Show full image on screen
    st.image("temp.jpg", caption="Uploaded Image", use_column_width=True)

    # Run prediction
    animal_en, animal_hi, conf = predict("temp.jpg")

    if animal_en:
        st.markdown(f"## ⚠️ ALERT: {animal_en.upper()}")
        st.write(f"Confidence: **{conf:.1f}%**")
        st.write(f"**हिन्दी:** यह {animal_hi} हो सकता है।")

        # Play alarm audio
        st.audio("alert.mp3", autoplay=True)

        # Optional: Show detection video (if you want to display YOLO inference video)
        # Save video output
        model.predict(source="temp.jpg", save=True, project="runs", name="detect")
        video_path = "runs/detect/predict/temp.jpg"  # YOLO saves annotated image/video

        if os.path.exists(video_path):
            st.image(video_path, caption="Detection Result", use_column_width=True)

    else:
        st.error("❌ Detection failed.")
