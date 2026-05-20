import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2
import requests
import os
import time

# -----------------------------------
# PAGE
# -----------------------------------
st.set_page_config(
    page_title="Wildlife Protection System",
    layout="wide"
)

st.title("🐾 Wildlife Protection System")

# -----------------------------------
# MODEL LOAD
# -----------------------------------
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

# -----------------------------------
# ANIMAL LIST
# -----------------------------------
danger_animals = [
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "cow",
    "dog",
    "cat",
    "horse"
]

hindi_names = {
    "elephant": "हाथी",
    "bear": "भालू",
    "zebra": "ज़ेबरा",
    "giraffe": "जिराफ",
    "cow": "गाय",
    "dog": "कुत्ता",
    "cat": "बिल्ली",
    "horse": "घोड़ा"
}

# -----------------------------------
# PABBLY
# -----------------------------------
PABBLY_WEBHOOK_URL = os.getenv("PABBLY_WEBHOOK_URL")

def send_alert(msg):
    try:
        if PABBLY_WEBHOOK_URL:
            requests.post(
                PABBLY_WEBHOOK_URL,
                json={"message": msg},
                timeout=5
            )
            print("✅ ALERT SENT")
    except:
        pass

# -----------------------------------
# FILE UPLOAD
# -----------------------------------
uploaded_file = st.file_uploader(
    "📸 Upload Image",
    type=["jpg", "jpeg", "png"]
)

# -----------------------------------
# DETECTION
# -----------------------------------
if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(
        image,
        width='stretch'
    )

    st.info("🔍 Detecting animals...")

    img_array = np.array(image)

    # YOLO DETECTION
    results = model(img_array)

    detected = False

    for result in results:

        boxes = result.boxes

        for box in boxes:

            cls_id = int(box.cls[0])

            conf = float(box.conf[0])

            label = model.names[cls_id]

            if label in danger_animals and conf > 0.40:

                detected = True

                hindi = hindi_names.get(label, label)

                st.error(
                    f"🚨 {label.upper()} DETECTED ({round(conf*100,2)}%)"
                )

                st.markdown(f"## हिन्दी नाम: {hindi}")

                # ALERT
                send_alert(
                    f"🚨 ALERT: {label} detected"
                )

                # -----------------------------------
                # AUTO SOUND
                # -----------------------------------

                alarm_url = "https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3"

                st.markdown(
                    f"""
                    <audio autoplay>
                    <source src="{alarm_url}" type="audio/mpeg">
                    </audio>

                    <script>
                    var audio = document.getElementsByTagName("audio")[0];
                    audio.play();
                    </script>
                    """,
                    unsafe_allow_html=True
                )

                st.success("🔊 Alarm Triggered")

    if detected == False:
        st.success("✅ No dangerous animal detected")

# -----------------------------------
# AWARENESS
# -----------------------------------
st.divider()

st.header("🌿 Awareness")

st.info("💧 जंगलों में पानी की व्यवस्था करें")

st.success("🌳 पेड़ लगाएं")

st.warning("🚧 Buffer zone बनाएं")

st.error("🚯 जंगलों में कचरा न फैलाएं")
