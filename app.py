import streamlit as st
from PIL import Image
from ultralytics import YOLO
import tempfile
import requests
import os
import base64

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Wildlife Protection System",
    page_icon="🐾",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================
st.markdown("""
<style>

.main {
    background-color: #f5fff5;
}

.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: #14532d;
    margin-bottom: 0px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #555;
    margin-top: 0px;
    margin-bottom: 30px;
}

.ready-box {
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
}

.detect-box {
    background-color: #ecfccb;
    padding: 20px;
    border-radius: 20px;
    border: 2px solid #84cc16;
}

.alert-box {
    background-color: #fee2e2;
    padding: 20px;
    border-radius: 20px;
    border: 2px solid red;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================
st.markdown(
    "<div class='title'>🐾 Wildlife Protection System</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Developed by Teacher Bhaskar Joshi</div>",
    unsafe_allow_html=True
)

# =====================================================
# SESSION STATE
# =====================================================
if "armed" not in st.session_state:
    st.session_state.armed = False

# =====================================================
# SYSTEM READY BUTTON
# =====================================================
col1, col2, col3 = st.columns([1,2,1])

with col2:

    if not st.session_state.armed:

        st.markdown(
            "<div class='alert-box'>🔴 SYSTEM NOT READY</div>",
            unsafe_allow_html=True
        )

        if st.button("🟢 ACTIVATE SYSTEM", use_container_width=True):

            st.session_state.armed = True
            st.rerun()

    else:

        st.markdown(
            "<div class='detect-box'>🟢 SYSTEM READY</div>",
            unsafe_allow_html=True
        )

# =====================================================
# LOAD MODEL
# =====================================================
@st.cache_resource
def load_model():
    return YOLO("yolov8n-cls.pt")

model = load_model()

# =====================================================
# HINDI LABELS
# =====================================================
animal_map = {
    "tiger": "बाघ",
    "bear": "भालू",
    "elephant": "हाथी",
    "dog": "कुत्ता",
    "cow": "गाय",
    "horse": "घोड़ा",
    "cat": "बिल्ली"
}

danger_animals = [
    "tiger",
    "bear",
    "elephant"
]

# =====================================================
# PABBLY WEBHOOK
# =====================================================
PABBLY_WEBHOOK_URL = "PASTE_YOUR_PABBLY_WEBHOOK_HERE"

def send_alert(message):

    try:

        response = requests.post(
            PABBLY_WEBHOOK_URL,
            json={"message": message},
            timeout=10
        )

        print(response.status_code)
        print(response.text)

    except Exception as e:
        print(e)

# =====================================================
# DETECTION
# =====================================================
def detect_animal(image):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    ) as tmp:

        image.save(tmp.name)

        results = model(tmp.name)

    probs = results[0].probs

    if probs is None:
        return None, 0

    top1 = probs.top1

    confidence = float(probs.top1conf) * 100

    animal = model.names[top1].lower()

    if confidence < 55:
        return None, confidence

    return animal, confidence

# =====================================================
# AUTO ALARM
# =====================================================
def autoplay_audio(file_path):

    if not os.path.exists(file_path):
        st.error("❌ alarm.mp3 file missing")
        return

    with open(file_path, "rb") as f:
        data = f.read()

    b64 = base64.b64encode(data).decode()

    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """

    st.markdown(md, unsafe_allow_html=True)

# =====================================================
# TABS
# =====================================================
tab1, tab2, tab3 = st.tabs([
    "🔍 Detection",
    "🌿 Awareness",
    "🧠 Quiz"
])

# =====================================================
# DETECTION TAB
# =====================================================
with tab1:

    st.markdown("## 📤 Upload Image or Use Webcam")

    uploaded_file = st.file_uploader(
        "Upload Animal Image",
        type=["jpg", "jpeg", "png"]
    )

    camera_image = st.camera_input(
        "📷 Capture from Webcam"
    )

    image = None

    if uploaded_file:
        image = Image.open(uploaded_file)

    elif camera_image:
        image = Image.open(camera_image)

    if image:

        st.image(
            image,
            width="stretch"
        )

        with st.spinner("🔍 Detecting Animal..."):

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

            # =========================================
            # DANGER ALERT
            # =========================================
            if (
                st.session_state.armed
                and animal in danger_animals
            ):

                st.error("🚨 DANGER ALERT 🚨")

                send_alert(
                    f"{animal.upper()} detected with {confidence:.1f}% confidence"
                )

                autoplay_audio("alarm.mp3")

                st.warning(
                    "🔊 Alarm Activated"
                )

            else:

                st.info("✅ Non-danger animal")

        else:

            st.warning(
                "❌ Animal not confidently detected"
            )

# =====================================================
# AWARENESS TAB
# =====================================================
with tab2:

    st.markdown(
        "## 🌿 Human-Animal Conflict Solutions"
    )

    st.info(
        "💧 जंगलों में पानी की व्यवस्था करें ताकि जानवर आबादी की ओर न आएं।"
    )

    st.success(
        "🌳 जंगलों में अधिक पेड़ लगाएं।"
    )

    st.warning(
        "🚧 Buffer Zone और Solar Fencing का उपयोग करें।"
    )

    st.error(
        "🚯 खुले में कचरा न फेंके।"
    )

# =====================================================
# QUIZ TAB
# =====================================================
with tab3:

    st.markdown(
        "## 🧠 Wildlife Awareness Quiz"
    )

    name = st.text_input(
        "👤 विद्यार्थी का नाम"
    )

    q1 = st.radio(
        "वन्यजीवों को रोकने का सबसे अच्छा तरीका?",
        [
            "जंगल में पानी",
            "पेड़ लगाना",
            "उपरोक्त सभी"
        ]
    )

    q2 = st.radio(
        "वन्यजीवों की सुरक्षा कौन करता है?",
        [
            "पुलिस",
            "वन विभाग",
            "विद्यालय"
        ]
    )

    if st.button("📩 Submit Quiz"):

        score = 0

        if q1 == "उपरोक्त सभी":
            score += 1

        if q2 == "वन विभाग":
            score += 1

        st.success(
            f"🎉 {name}, आपका स्कोर: {score}/2"
        )

        if score == 2:
            st.balloons()
