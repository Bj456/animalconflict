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
    "Tiger": "बाघ",  # 'शेर' को 'बाघ' किया ताकि बच्चों के लिए वैज्ञानिक रूप से सही रहे
    "Leopard": "तेंदुआ", # 'चीता' को 'तेंदुआ' (Leopard) किया
    "Bear": "भालू"
}

PABBLY_WEBHOOK_URL = os.getenv("PABBLY_WEBHOOK_URL")

def send_alert(msg):
    try:
        if PABBLY_WEBHOOK_URL:
            requests.post(PABBLY_WEBHOOK_URL, json={"message": msg}, timeout=5)
    except:
        pass

def detect(image):
    animal = random.choice(animals)
    conf = random.randint(60, 95)

    if conf > 70:
        send_alert(f"ALERT: {animal} {conf}%")

    return animal, animal_hi[animal], conf

# ---------------------------
# UI Setup
# ---------------------------
st.title("🐾 Wildlife Protection System")

tab1, tab2, tab3 = st.tabs(["🔍 Detection", "🌿 Awareness", "🧠 Quiz"])

# ---------------------------
# 1. Detection Tab (with Audio Siren)
# ---------------------------
with tab1:
    file = st.file_uploader("Upload Image")

    if file:
        img = Image.open(file)
        st.image(img, use_container_width=True)

        animal, hi, conf = detect(img)

        st.error(f"🚨 ALERT: {animal.upper()} DETECTED! ({conf}%)")
        st.markdown(f"### हिन्दी नाम: **{hi}**")

        # 🔊 अगर कॉन्फिडेंस 70% से ज़्यादा है, तो ज़ोरदार अलार्म बजेगा
        if conf > 70:
            # Google का एक सुरक्षित और तेज़ डिजिटल वॉच अलार्म टोन
            siren_url = "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg"
            
            # HTML5 ऑडियो कोड जो बिना किसी बटन के अपने आप बजता है
            st.markdown(f"""
                <iframe src="{siren_url}" allow="autoplay" style="display:none" id="iframeAudio"></iframe>
                <audio autoplay loop>
                    <source src="{siren_url}" type="audio/ogg">
                </audio>
            """, unsafe_allowed_html=True)
            st.toast("🚨 अलार्म बज रहा है! सावधान रहें!", icon="📢")

# ---------------------------
# 2. Awareness Tab
# ---------------------------
with tab2:
    st.markdown("## 🌿 Human-Animal Conflict Solutions")
    st.markdown("ग्रामीण और पर्वतीय क्षेत्रों में मानव-वन्यजीव संघर्ष को रोकने के उपाय:")

    st.info("💧 **Water sources in forest:** जंगलों के भीतर प्राकृतिक जलस्रोतों (नौले/धारे) का पुनरुद्धार ताकि जानवर पानी के लिए आबादी में न आएं।")
    st.success("🌳 **Plant trees:** वनों में फलदार और स्थानीय चौड़ी पत्ती वाले पौधों का रोपण करना।")
    st.warning("🚧 **Use buffer zones:** कृषि भूमि और घने जंगलों के बीच एक सुरक्षित बफर ज़ोन या सोलर फेंसिंग का उपयोग।")
    st.error("🚯 **Avoid waste dumping:** बस्तियों के आस-पास खुले में कचरा और जूठा भोजन न फेंकना, जिससे भालू और तेंदुए आकर्षित होते हैं।")

# ---------------------------
# 3. Quiz Tab
# ---------------------------
with tab3:
    st.markdown("## 🧠 बाल वैज्ञानिक क्विज़ (Life Skills & Nature)")
    name = st.text_input("विद्यार्थी का नाम दर्ज करें:")

    q1 = st.radio("वन्यजीवों को आबादी में आने से रोकने का सबसे अच्छा तरीका क्या है?", ["जंगल में पानी की व्यवस्था", "फलदार पेड़ लगाना", "उपरोक्त सभी"])
    q2 = st.radio("हमारे जंगलों और वन्यजीवों की सुरक्षा मुख्य रूप से कौन करता है?", ["पुलिस", "वन विभाग (Forest Dept)", "विद्यालय"])

    if st.button("जमा करें (Submit Score)"):
        if not name:
            st.warning("कृपया पहले अपना नाम लिखें!")
        else:
            score = 0
            if q1 == "उपरोक्त सभी": score += 1
            if q2 == "वन विभाग (Forest Dept)": score += 1

            if score == 2:
                st.success(f"🎉 शानदार, {name}! आपका स्कोर: {score}/2 है। आप एक सच्चे प्रकृति रक्षक हैं! 🌟")
                st.balloons() # बच्चों के उत्साहवर्धन के लिए स्क्रीन पर गुब्बारे छूटेंगे
            else:
                st.warning(f"👍 अच्छा प्रयास {name}! आपका स्कोर: {score}/2 है। एक बार फिर कोशिश करें!")
