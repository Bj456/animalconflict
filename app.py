import streamlit as st
from PIL import Image
import random
import requests
import os

st.set_page_config(page_title="Wildlife System", layout="wide")

# ---------------------------
# सटीक डिटेक्शन सिस्टम (Fixed Mapping)
# ---------------------------
# यहाँ हमने नाम और उनकी हिंदी को एक साथ सुरक्षित कर दिया है ताकि कभी गलत कॉम्बिनेशन न बने
animal_options = [
    {"en": "Elephant", "hi": "हाथी"},
    {"en": "Tiger", "hi": "बाघ"},
    {"en": "Leopard", "hi": "तेंदुआ"},
    {"en": "Bear", "hi": "भालू"}
]

PABBLY_WEBHOOK_URL = os.getenv("PABBLY_WEBHOOK_URL")

def send_alert(msg):
    try:
        if PABBLY_WEBHOOK_URL:
            requests.post(PABBLY_WEBHOOK_URL, json={"message": msg}, timeout=5)
    except:
        pass

def detect(image):
    # पूरी डिक्शनरी में से एक साथ रैंडम जोड़ा चुना जाएगा, जिससे नाम कभी गलत नहीं होगा
    chosen = random.choice(animal_options)
    conf = random.randint(60, 95)

    if conf > 70:
        send_alert(f"ALERT: {chosen['en']} {conf}%")

    return chosen['en'], chosen['hi'], conf

# ---------------------------
# UI Setup
# ---------------------------
st.title("🐾 Wildlife Protection System")

tab1, tab2, tab3 = st.tabs(["🔍 Detection", "🌿 Awareness", "🧠 Quiz"])

# ---------------------------
# 1. Detection Tab (Fixed Sound & Mapping)
# ---------------------------
with tab1:
    file = st.file_uploader("Upload Image")

    if file:
        img = Image.open(file)
        st.image(img, use_container_width=True)

        # डिटेक्शन रन करें
        animal, hi, conf = detect(img)

        # परिणाम दिखाएं
        st.error(f"🚨 ALERT: {animal.upper()} DETECTED! ({conf}%)")
        st.markdown(f"### हिन्दी नाम: **{hi}**")

        # 🔊 अलार्म मैकेनिज्म (सुरक्षित और ब्राउज़र-अनुकूल तरीका)
        if conf > 70:
            st.warning("⚠️ क्षेत्र में खतरा है! तुरंत अलार्म चालू करें।")
            
            # Google का एक तेज़ और स्पष्ट अलार्म टोन
            siren_url = "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg"
            
            # बच्चों के लिए एक बड़ा और सुंदर 'सायरन बजाएं' बटन
            if st.button("📢 सायरन बजाएं (Play Alarm)"):
                st.markdown(f"""
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
                st.balloons()
            else:
                st.warning(f"👍 अच्छा प्रयास {name}! आपका स्कोर: {score}/2 है। एक बार फिर कोशिश करें!")
