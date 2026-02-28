# ---------------------------------------
# HERLAW CHATBOT (GROQ + STREAMLIT)
# Beautiful Women-Friendly UI Version
# ---------------------------------------

import streamlit as st
from groq import Groq

# ---------------------------------------
# 🔑 GROQ API KEY
# ---------------------------------------
client = Groq(
    api_key="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"   # ← paste your key
)

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(
    page_title="HerLaw",
    page_icon="⚖️",
    layout="centered"
)

# ---------------------------------------
# 🌸 BEAUTIFUL WOMEN-FRIENDLY UI STYLE
# ---------------------------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #fff6fb, #f3e8ff);
    font-family: 'Segoe UI', sans-serif;
}

/* Container spacing */
.block-container {
    padding-top: 2rem;
}

/* Chat bubbles */
.stChatMessage {
    background-color: white;
    border-radius: 18px;
    padding: 14px;
    margin-bottom: 10px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.08);
}

/* Message text visibility */
[data-testid="stChatMessageContent"] {
    color: #222222 !important;
    font-size: 16px;
    line-height: 1.6;
}

/* User message highlight */
[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageContent"]) {
    border-left: 5px solid #d946ef;
}

/* Input box */
textarea {
    background-color: white !important;
    color: black !important;
    border-radius: 12px !important;
    border: 2px solid #f0abfc !important;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fdf2f8, #f3e8ff);
}

section[data-testid="stSidebar"] * {
    color: #3b0764 !important;
}

/* Buttons */
.stButton button {
    background: linear-gradient(90deg, #ec4899, #a855f7);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 8px 16px;
    font-weight: 600;
}

.stButton button:hover {
    opacity: 0.9;
}

/* Title */
h1 {
    color: #7e22ce;
}

/* Caption */
p {
    color: #374151;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# TITLE
# ---------------------------------------
st.title("🌸 HerLaw — A Safe Space to Know Your Rights")
st.caption("AI assistant helping women understand legal rights in India 💜")

# ---------------------------------------
# SIDEBAR
# ---------------------------------------
with st.sidebar:
    st.header("🚨 Emergency Helplines (India)")
    st.write("📞 Police: 112")
    st.write("📞 Women Helpline: 181")
    st.write("📞 Domestic Violence: 1091")
    st.write("📞 Legal Aid: 1516")
    st.write("📞 Child Helpline: 1098")

    st.divider()

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.caption(
        "⚠️ This chatbot provides general legal information only."
    )

# ---------------------------------------
# SYSTEM PROMPT
# ---------------------------------------
SYSTEM_PROMPT = """
You are HerLaw, a compassionate legal assistant for women in India.

Rules:
- Respond with empathy and emotional support.
- Explain legal rights in simple language.
- Provide practical next steps.
- Mention Indian laws when relevant.
- Encourage consulting a lawyer.
- Avoid legal jargon.
"""

# ---------------------------------------
# CHAT MEMORY
# ---------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------
# USER INPUT
# ---------------------------------------
user_input = st.chat_input(
    "Describe your situation... I am here to help 💜"
)

if user_input:

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # AI Response
    with st.spinner("HerLaw is thinking..."):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT}
            ] + st.session_state.messages,
            temperature=0.7,
            max_tokens=800,
        )

    reply = response.choices[0].message.content

    # Show assistant reply
    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )