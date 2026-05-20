import streamlit as st
from PIL import Image
from ultralytics import YOLO
import tempfile
import requests
import os
import base64

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Wildlife Protection System",
    layout="wide"
)

st.title("🐾 Wildlife Protection System")

# -------------------------
# SESSION STATE
# -------------------------
if "armed" not in st.session_state:
    st.session_state.armed = False

# -------------------------
# SYSTEM ARM BUTTON
# -------------------------
if not st.session_state.armed:

    st.error("🔴 SYSTEM NOT READY")

    if st.button("🟢 ACTIVATE SYSTEM"):

        st.session_state.armed = True
        st.rerun()

else:

    st.success("🟢 SYSTEM READY")

# -------------------------
# LOAD MODEL
# -------------------------
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

# -------------------------
# HINDI LABELS
# -------------------------
animal_map = {
    "elephant": "हाथी",
    "bear": "भालू",
    "zebra": "ज़ेब्रा",
    "giraffe": "जिराफ",
    "cow": "गाय",
    "dog": "कुत्ता",
    "cat": "बिल्ली"
}

danger_animals = [
    "elephant",
    "bear",
    "zebra",
    "giraffe"
]

# -------------------------
# ALERT SYSTEM
# -------------------------
PABBLY_WEBHOOK_URL = os.getenv("PABBLY_WEBHOOK_URL")

def send_alert(message):

    try:

        if PABBLY_WEBHOOK_URL:

            requests.post(
                PABBLY_WEBHOOK_URL,
                json={"message": message},
                timeout=5
            )

            print("✅ Alert Sent")

    except Exception as e:
        print(e)

# -------------------------
# DETECTION
# -------------------------
def detect_animal(image):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    ) as tmp:

        image.save(tmp.name)

        results = model(tmp.name)

    detected_name = None
    confidence = 0

    for r in results:

        boxes = r.boxes

        if boxes is not None and len(boxes) > 0:

            confs = boxes.conf.cpu().numpy()
            classes = boxes.cls.cpu().numpy()

            max_index = confs.argmax()

            confidence = float(confs[max_index]) * 100

            cls_id = int(classes[max_index])

            detected_name = model.names[cls_id].lower()

            break

    return detected_name, confidence

# -------------------------
# AUTO ALARM
# -------------------------
def autoplay_audio(file_path):

    with open(file_path, "rb") as f:
        data = f.read()

    b64 = base64.b64encode(data).decode()

    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """

    st.markdown(md, unsafe_allow_html=True)

# -------------------------
# IMAGE UPLOAD
# -------------------------
uploaded_file = st.file_uploader(
    "📤 Upload Animal Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(image, width="stretch")

    with st.spinner("🔍 Detecting..."):

        animal, confidence = detect_animal(image)

    if animal:

        hindi_name = animal_map.get(
            animal,
            "अज्ञात"
        )

        st.success(
            f"✅ {animal.upper()} detected ({confidence:.1f}%)"
        )

        st.markdown(
            f"### हिन्दी नाम: {hindi_name}"
        )

        # -------------------------
        # DANGER ALERT
        # -------------------------
        if (
            st.session_state.armed
            and animal in danger_animals
            and confidence > 40
        ):

            st.error("🚨 DANGER ALERT 🚨")

            send_alert(
                f"{animal.upper()} detected"
            )

            # AUTO PLAY SOUND
            autoplay_audio("alarm.mp3")

            st.warning(
                "🔊 Alarm Activated"
            )

        else:

            st.info("✅ No danger animal")

    else:

        st.warning("❌ No animal detected")
