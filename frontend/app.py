import streamlit as st
import requests
import json

BACKEND_URL = "http://localhost:8000"  # update after deploying backend

st.set_page_config(page_title="NemoAI", page_icon="🤖")
st.title("NemoAI Chat Assistant")

if "history" not in st.session_state:
    st.session_state.history = []

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        resp = requests.post(
            f"{BACKEND_URL}/chat",
            json={"message": user_input, "history": st.session_state.history[:-1]},
            stream=True,
        )

        for line in resp.iter_lines():
            if not line:
                continue
            line = line.decode("utf-8")
            if line.startswith("data: "):
                data = json.loads(line[6:])
                if "content" in data:
                    full_response += data["content"]
                    placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)

    st.session_state.history.append({"role": "assistant", "content": full_response})