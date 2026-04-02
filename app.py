import gradio as gr
from ultralytics import YOLO
import base64
import os
import requests

# ---------------------------
# Secure Webhook
# ---------------------------
PABBLY_WEBHOOK_URL = os.getenv("PABBLY_WEBHOOK_URL")

# ---------------------------
# Load Model (Detection)
# ---------------------------
model = YOLO("yolov8n.pt")

animal_name_hi = {
    "elephant": "हाथी",
    "bear": "भालू",
    "zebra": "ज़ेब्रा",
    "giraffe": "जिराफ",
    "dog": "कुत्ता",
    "cat": "बिल्ली"
}

# ---------------------------
# Alert Function
# ---------------------------
def send_alert(message):
    try:
        if PABBLY_WEBHOOK_URL:
            requests.post(PABBLY_WEBHOOK_URL, json={"message": message}, timeout=5)
    except:
        pass

# ---------------------------
# Audio
# ---------------------------
def get_audio():
    if os.path.exists("alert.mp3"):
        with open("alert.mp3", "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# ---------------------------
# Detection Function
# ---------------------------
def detect(image):
    if image is None:
        return "Upload image first"

    results = model.predict(source=image, conf=0.4)
    r = results[0]

    if len(r.boxes) == 0:
        return "❌ No animal detected"

    cls_id = int(r.boxes.cls[0])
    conf = float(r.boxes.conf[0]) * 100

    animal_en = model.names[cls_id]
    animal_hi = animal_name_hi.get(animal_en, animal_en)

    if conf > 70:
        send_alert(f"ALERT: {animal_en} {conf:.1f}%")

    audio = get_audio()

    color = "green" if conf > 80 else "orange" if conf > 50 else "red"

    return f"""
    <div style='padding:20px;border-radius:15px;border:3px solid {color};background:#f9fafb;text-align:center;'>
        <h2 style='color:{color};'>⚠️ {animal_en.upper()}</h2>
        <p>Confidence: <b>{conf:.1f}%</b></p>
        <p style='font-size:18px;background:#e0f2fe;padding:10px;border-radius:10px;'>
        हिन्दी: यह <b>{animal_hi}</b> हो सकता है
        </p>
        <audio controls autoplay src='data:audio/mpeg;base64,{audio}'></audio>
    </div>
    """

# ---------------------------
# Awareness Section
# ---------------------------
awareness_html = """
<h2 style='text-align:center;color:#6b21a8;'>🌿 Human-Animal Conflict Awareness</h2>
<div style='display:flex;flex-wrap:wrap;gap:15px;justify-content:center;'>
<div style='background:#fde68a;padding:15px;border-radius:10px;'>Water holes in forest</div>
<div style='background:#a7f3d0;padding:15px;border-radius:10px;'>Plant native trees</div>
<div style='background:#fca5a5;padding:15px;border-radius:10px;'>Buffer zones</div>
<div style='background:#c7d2fe;padding:15px;border-radius:10px;'>Waste management</div>
<div style='background:#fde68a;padding:15px;border-radius:10px;'>Solar lights</div>
<div style='background:#a7f3d0;padding:15px;border-radius:10px;'>Protect livestock</div>
</div>
"""

# ---------------------------
# Quiz Data
# ---------------------------
quiz_q = [
    ("Best way to reduce conflict?", ["Water", "Trees", "All"], 2),
    ("Who handles wildlife in India?", ["Police", "Forest Dept", "School"], 1),
]

# ---------------------------
# Quiz Function
# ---------------------------
def quiz(name, q1, q2):
    score = 0
    if q1 == "All": score += 1
    if q2 == "Forest Dept": score += 1

    return f"""
    <div style='padding:20px;background:#ecfeff;border-radius:10px;text-align:center;'>
        <h2>🎉 {name} Score: {score}/2</h2>
    </div>
    """

# ---------------------------
# UI Layout
# ---------------------------
with gr.Blocks(css="""
body {background: linear-gradient(to right,#dbeafe,#f0fdf4);}
""") as app:

    gr.Markdown("""
    <h1 style='text-align:center;color:#1e3a8a;'>🐾 Wildlife Protection System</h1>
    """)

    with gr.Tabs():

        # -------- Detection --------
        with gr.Tab("🔍 Detection + Alert"):
            with gr.Row():
                img = gr.Image(type="filepath")
                out = gr.HTML()
            btn = gr.Button("Detect")
            btn.click(detect, img, out)

        # -------- Awareness --------
        with gr.Tab("🌿 Awareness"):
            gr.HTML(awareness_html)

        # -------- Quiz --------
        with gr.Tab("🧠 Quiz"):
            name = gr.Textbox(label="Your Name")
            q1 = gr.Radio(["Water","Trees","All"], label="Q1")
            q2 = gr.Radio(["Police","Forest Dept","School"], label="Q2")
            btn2 = gr.Button("Submit")
            result = gr.HTML()
            btn2.click(quiz, [name,q1,q2], result)

app.launch()
