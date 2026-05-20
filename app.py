import streamlit as st
from PIL import Image
import random
import requests
import os
import time

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Wildlife Protection System",
    layout="wide"
)

# ---------------------------
# ANIMAL DATA
# ---------------------------
animal_options = [
    {"en": "Elephant", "hi": "हाथी"},
    {"en": "Tiger", "hi": "बाघ"},
    {"en": "Leopard", "hi": "तेंदुआ"},
    {"en": "Bear", "hi": "भालू"}
]

# ---------------------------
# PABBLY
# ---------------------------
PABBLY_WEBHOOK_URL = os.getenv("PABBLY_WEBHOOK_URL")

def send_alert(msg):
    try:
        if PABBLY_WEBHOOK_URL:
            requests.post(
                PABBLY_WEBHOOK_URL,
                json={"message": msg},
                timeout=5
            )
            print("✅ Alert sent")
    except Exception as e:
        print("❌ Alert error:", e)

# ---------------------------
# FAKE AI DETECTION
# ---------------------------
def detect(image):

    # DEMO ONLY
    chosen = random.choice(animal_options)

    # confidence realistic
    conf = random.randint(72, 97)

    if conf > 75:
        send_alert(f"🚨 ALERT: {chosen['en']} detected with {conf}% confidence")

    return chosen["en"], chosen["hi"], conf

# ---------------------------
# TITLE
# ---------------------------
st.title("🐾 Wildlife Protection System")

# ---------------------------
# TABS
# ---------------------------
tab1, tab2, tab3 = st.tabs([
    "🔍 Detection",
    "🌿 Awareness",
    "🧠 Quiz"
])

# =========================================================
# DETECTION TAB
# =========================================================
with tab1:

    st.header("📸 Animal Detection")

    uploaded_file = st.file_uploader(
        "Upload Wildlife Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        img = Image.open(uploaded_file)

        st.image(img, use_container_width=True)

        # processing animation
        with st.spinner("🔍 Detecting Animal..."):
            time.sleep(2)

        animal, hi, conf = detect(img)

        # RESULTS
        st.error(f"🚨 {animal.upper()} DETECTED")

        st.markdown(f"""
        ### 📊 Confidence: `{conf}%`

        ### 🇮🇳 हिन्दी नाम:
        ## {hi}
        """)

        # ---------------------------------------
        # ALARM SECTION
        # ---------------------------------------
        if conf > 75:

            st.warning("⚠️ खतरा detected! Alarm auto-play करने की कोशिश की जा रही है...")

            # PUBLIC MP3
            alarm_url = "https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3"

            # AUTOPLAY AUDIO
            audio_html = f"""
            <audio autoplay controls>
                <source src="{alarm_url}" type="audio/mpeg">
            </audio>

            <script>
            var audio = document.getElementsByTagName('audio')[0];
            audio.play();
            </script>
            """

            st.markdown(
                audio_html,
                unsafe_allow_html=True
            )

            st.success("🔊 Alarm Triggered")

# =========================================================
# AWARENESS TAB
# =========================================================
with tab2:

    st.header("🌿 Human-Wildlife Conflict Solutions")

    st.info(
        "💧 जंगलों में जल स्रोत बढ़ाने चाहिए ताकि जानवर गांवों की ओर न आएं।"
    )

    st.success(
        "🌳 अधिक पेड़ लगाएं और प्राकृतिक आवास बचाएं।"
    )

    st.warning(
        "🚧 जंगल और गांव के बीच buffer zone बनाना चाहिए।"
    )

    st.error(
        "🚯 खुले में भोजन और कचरा न फेंकें।"
    )

# =========================================================
# QUIZ TAB
# =========================================================
with tab3:

    st.header("🧠 Wildlife Quiz")

    student_name = st.text_input("विद्यार्थी का नाम लिखें")

    q1 = st.radio(
        "वन्यजीव संघर्ष रोकने का सबसे अच्छा तरीका?",
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

    if st.button("Submit Quiz"):

        if student_name == "":
            st.warning("पहले नाम लिखें")
        else:

            score = 0

            if q1 == "उपरोक्त सभी":
                score += 1

            if q2 == "वन विभाग":
                score += 1

            if score == 2:

                st.success(
                    f"🎉 शानदार {student_name} ! आपका स्कोर {score}/2 है"
                )

                st.balloons()

            else:

                st.warning(
                    f"👍 अच्छा प्रयास {student_name} ! स्कोर {score}/2"
                )
