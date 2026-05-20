import streamlit as st
from PIL import Image
import requests
import os
from ultralytics import YOLO
import tempfile

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Wildlife Protection System", layout="wide")

st.title("🐾 Wildlife Protection System")

# ---------------------------
# LOAD YOLO MODEL
# ---------------------------
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

# ---------------------------
# ANIMAL LABELS
# ---------------------------
animal_map = {
    "elephant": "हाथी",
    "bear": "भालू",
    "zebra": "ज़ेब्रा",
    "giraffe": "जिराफ",
    "cow": "गाय",
    "dog": "कुत्ता",
    "cat": "बिल्ली",
    "horse": "घोड़ा",
    "sheep": "भेड़"
}

danger_animals = [
    "elephant",
    "bear",
    "zebra",
    "giraffe"
]

# ---------------------------
# PABBLY ALERT
# ---------------------------
PABBLY_WEBHOOK_URL = os.getenv("PABBLY_WEBHOOK_URL")

def send_alert(message):
    try:
        if PABBLY_WEBHOOK_URL:
            requests.post(
                PABBLY_WEBHOOK_URL,
                json={"message": message},
                timeout=5
            )
            print("✅ Alert sent")
    except Exception as e:
        print(e)

# ---------------------------
# DETECTION FUNCTION
# ---------------------------
def detect_animal(image):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
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

# ---------------------------
# TABS
# ---------------------------
tab1, tab2, tab3 = st.tabs(
    ["🔍 Detection", "🌿 Awareness", "🧠 Quiz"]
)

# =========================================================
# DETECTION TAB
# =========================================================
with tab1:

    uploaded_file = st.file_uploader(
        "📤 Upload Animal Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:

        image = Image.open(uploaded_file)

        st.image(image, width='stretch')

        with st.spinner("🔍 Detecting Animal..."):

            animal, confidence = detect_animal(image)

        # ---------------------------
        # RESULT
        # ---------------------------
        if animal:

            hindi_name = animal_map.get(animal, "अज्ञात")

            st.success(
                f"✅ Detected: {animal.upper()} ({confidence:.1f}%)"
            )

            st.markdown(
                f"### हिन्दी नाम: **{hindi_name}**"
            )

            # ---------------------------
            # DANGER ALERT
            # ---------------------------
            if animal in danger_animals and confidence > 40:

                st.error(
                    "🚨 खतरा! जंगली जानवर पाया गया!"
                )

                # Send webhook
                send_alert(
                    f"🚨 ALERT: {animal.upper()} detected with {confidence:.1f}% confidence"
                )

                # ---------------------------
                # AUTO PLAY SIREN
                # ---------------------------
                # IMPORTANT:
                # Streamlit browsers block autoplay sometimes.
                # THIS JS forces play automatically.
                # ---------------------------

                st.components.v1.html(
                    """
                    <html>
                    <body>

                    <audio id="alarm" autoplay loop>
                        <source src="https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3" type="audio/mp3">
                    </audio>

                    <script>
                    var audio = document.getElementById("alarm");

                    function playAudio() {
                        audio.play();
                    }

                    playAudio();

                    document.addEventListener('click', function() {
                        audio.play();
                    });

                    </script>

                    <h1 style="color:red;text-align:center;">
                    🚨 DANGER ALERT 🚨
                    </h1>

                    </body>
                    </html>
                    """,
                    height=200,
                )

                st.warning(
                    "🔊 यदि आवाज़ न आए तो स्क्रीन पर एक बार क्लिक करें।"
                )

            else:

                st.info("✅ कोई खतरनाक जानवर नहीं मिला")

        else:

            st.warning("❌ कोई जानवर detect नहीं हुआ")

# =========================================================
# AWARENESS TAB
# =========================================================
with tab2:

    st.markdown("## 🌿 Human-Animal Conflict Solutions")

    st.info(
        "💧 जंगलों में पानी की व्यवस्था करें ताकि जानवर गांवों में न आएं।"
    )

    st.success(
        "🌳 जंगलों में फलदार पेड़ लगाएं।"
    )

    st.warning(
        "🚧 सोलर फेंसिंग और बफर ज़ोन का उपयोग करें।"
    )

    st.error(
        "🚯 खुले में भोजन और कचरा न फेंकें।"
    )

# =========================================================
# QUIZ TAB
# =========================================================
with tab3:

    st.markdown("## 🧠 Wildlife Quiz")

    name = st.text_input("👦 विद्यार्थी का नाम")

    q1 = st.radio(
        "वन्यजीवों को गांव में आने से कैसे रोक सकते हैं?",
        [
            "जंगल में पानी रखना",
            "पेड़ लगाना",
            "दोनों"
        ]
    )

    q2 = st.radio(
        "वन्यजीव सुरक्षा कौन करता है?",
        [
            "पुलिस",
            "वन विभाग",
            "विद्यालय"
        ]
    )

    if st.button("📤 Submit Quiz"):

        if not name:

            st.warning("⚠️ नाम लिखें")

        else:

            score = 0

            if q1 == "दोनों":
                score += 1

            if q2 == "वन विभाग":
                score += 1

            st.success(
                f"🎉 {name} आपका स्कोर: {score}/2"
            )

            if score == 2:
                st.balloons()
