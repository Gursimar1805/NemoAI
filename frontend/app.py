import streamlit as st
import requests
import json

BACKEND_URL = "https://nemoai-1.onrender.com"

st.set_page_config(page_title="NemoAI", page_icon="✨", layout="centered")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Inter:wght@400;500&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .stApp {
        background: radial-gradient(circle at 20% 0%, #1a1230 0%, #0b0b14 55%, #08080f 100%);
    }

    /* Hide default streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }

    /* Animated gradient title */
    .nemo-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.6rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399, #a78bfa);
        background-size: 300% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 6s linear infinite;
        margin-bottom: 0;
    }
    .nemo-subtitle {
        text-align: center;
        color: #8b8b9e;
        font-size: 0.95rem;
        margin-top: 4px;
        margin-bottom: 28px;
    }
    @keyframes shine {
        to { background-position: 300% center; }
    }

    /* Chat bubbles */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 4px 8px;
        margin-bottom: 14px;
        animation: fadeIn 0.35s ease-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* User vs assistant bubble tint */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: linear-gradient(135deg, rgba(96,165,250,0.12), rgba(167,139,250,0.08));
        border-color: rgba(96,165,250,0.25);
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        background: linear-gradient(135deg, rgba(52,211,153,0.10), rgba(255,255,255,0.03));
        border-color: rgba(52,211,153,0.18);
    }

    /* Chat input box */
    [data-testid="stChatInput"] textarea {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(167,139,250,0.35) !important;
        border-radius: 14px !important;
        color: #f0f0f5 !important;
        box-shadow: 0 0 18px rgba(124,58,237,0.08);
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: #a78bfa !important;
        box-shadow: 0 0 22px rgba(167,139,250,0.35) !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-thumb { background: rgba(167,139,250,0.3); border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="nemo-title">✨ NemoAI</div>', unsafe_allow_html=True)
st.markdown('<div class="nemo-subtitle">Your all-purpose AI assistant, powered by Nemotron</div>', unsafe_allow_html=True)

# ---------- STATE ----------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- RENDER HISTORY ----------
for msg in st.session_state.history:
    avatar = "🧑" if msg["role"] == "user" else "✨"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ---------- INPUT ----------
user_input = st.chat_input("Ask me anything...")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})

    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="✨"):
        placeholder = st.empty()
        placeholder.markdown("_thinking…_")
        full_response = ""

                resp = requests.post(
            f"{BACKEND_URL}/chat",
            json={"message": user_input, "history": st.session_state.history[:-1]},
            stream=True,
        )

        if resp.status_code != 200:
            placeholder.error(f"Connection failed: HTTP {resp.status_code} — {resp.text[:200]}")
            full_response = None
        else:
            for line in resp.iter_lines():
                if not line:
                    continue
                line = line.decode("utf-8")
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    if "error" in data:
                        placeholder.error(f"Backend error: {data['error']}")
                        full_response = None
                        break
                    if "content" in data:
                        full_response += data["content"]
                        placeholder.markdown(full_response + " ▌")

            if full_response is not None:
                placeholder.markdown(full_response)

    if full_response is not None:
        st.session_state.history.append({"role": "assistant", "content": full_response})