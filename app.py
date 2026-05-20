# =========================
# AUTO ALARM FIX
# =========================
# PURANE st.components.v1.html WALE CODE KO HATA DO
# AUR ISKO LAGA DO
# =========================

import base64

# Local siren file
SIREN_FILE = "alarm.mp3"

def autoplay_audio(file_path):

    with open(file_path, "rb") as f:
        data = f.read()

    b64 = base64.b64encode(data).decode()

    md = f"""
    <audio id="alarmAudio" autoplay controls loop>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>

    <script>
    var audio = document.getElementById("alarmAudio");

    async function startAudio() {{
        try {{
            audio.volume = 1.0;
            await audio.play();
            console.log("Playing");
        }}
        catch(err) {{
            console.log(err);
        }}
    }}

    startAudio();

    document.addEventListener('click', function() {{
        audio.play();
    }});

    document.addEventListener('keydown', function() {{
        audio.play();
    }});
    </script>
    """

    st.markdown(md, unsafe_allow_html=True)

# =========================
# ISKO DANGER ALERT KE ANDAR LAGAO
# =========================

if animal in danger_animals and confidence > 40:

    st.error("🚨 खतरा! जंगली जानवर पाया गया!")

    send_alert(
        f"🚨 ALERT: {animal.upper()} detected with {confidence:.1f}% confidence"
    )

    # SOUND PLAY
    autoplay_audio("alarm.mp3")

    st.warning(
        "🔊 यदि आवाज़ न आए तो स्क्रीन पर एक बार क्लिक करें"
    )
