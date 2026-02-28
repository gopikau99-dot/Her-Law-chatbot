import streamlit as st
from groq import Groq

# ---------------------------------------------------
# 🔑 GROQ API
# ---------------------------------------------------
client = Groq(
    api_key="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"  # Replace with your key
)

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="HerLaw",
    page_icon="🌸",
    layout="wide"
)

# ---------------------------------------------------
# UI STYLE (SAGE + CREAM + BLACK TEXT)
# ---------------------------------------------------
st.markdown("""
<style>

header {visibility: hidden;}
footer {visibility: hidden;}

.stApp {
    background: linear-gradient(135deg, #f4f1e8, #f8f6ef);
    font-family: 'Georgia', serif;
    color: black;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #cfded3, #b8cbbf);
    padding-top: 2rem;
}

section[data-testid="stSidebar"] * {
    color: black !important;
}

h1 {
    color: black;
    font-size: 44px;
    font-weight: 500;
}

p {
    color: black;
    font-size: 18px;
}

.stChatMessage {
    background: #f7f4ed;
    border-radius: 18px;
    padding: 14px;
    margin-bottom: 12px;
    border: 1px solid #e0dbd1;
}

[data-testid="stChatMessageContent"] {
    color: black !important;
}

textarea {
    background-color: #f7f4ed !important;
    color: black !important;
    border-radius: 16px !important;
    border: 1px solid #d6d0c4 !important;
}

div[data-testid="stChatInput"] {
    background: #f7f4ed;
    border-radius: 20px;
    padding: 6px;
    border: 1px solid #d6d0c4;
}

.stButton button {
    background: #b78fa1;
    color: white;
    border-radius: 14px;
    border: none;
    padding: 8px 16px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.markdown("""
<h1>🌸 HerLaw — Structured Legal Guidance for Women</h1>
<p>Understand your rights clearly. Take informed legal steps confidently.</p>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# CATEGORY SELECTION
# ---------------------------------------------------
category = st.selectbox(
    "Select Legal Category",
    [
        "Domestic Violence",
        "Divorce / Marriage Issues",
        "Workplace Harassment",
        "Dowry Harassment",
        "Child Custody",
        "Property Rights",
        "Other"
    ]
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
with st.sidebar:
    st.markdown("## 🚨 Emergency Contacts (India)")
    st.markdown("Police: 112")
    st.markdown("Women Helpline: 181")
    st.markdown("Domestic Violence: 1091")
    st.markdown("Legal Aid: 1516")
    st.markdown("Child Helpline: 1098")
    st.markdown("---")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.caption("This assistant provides general legal information only.")

# ---------------------------------------------------
# SYSTEM PROMPT (STRUCTURED OUTPUT)
# ---------------------------------------------------
SYSTEM_PROMPT = f"""
You are HerLaw, a compassionate and professional legal assistant for women in India.

Selected Category: {category}

Always respond in this structured format:

📌 Situation Summary:
Briefly summarize the user's issue.

⚖ Relevant Indian Laws:
Mention specific Acts and provisions applicable.

📝 Practical Steps You Can Take:
Provide step-by-step actions.

🚨 If Immediate Risk Exists:
Mention emergency helpline numbers if necessary.

👩‍⚖ When to Consult a Lawyer:
Explain when professional legal help is important.

Use simple language.
Be empathetic.
Avoid legal jargon.
"""

# ---------------------------------------------------
# CHAT MEMORY
# ---------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------------------
# USER INPUT
# ---------------------------------------------------
user_input = st.chat_input("Describe your situation in detail... 💜")

if user_input:

    emergency_keywords = ["danger", "hit", "abuse", "threat", "urgent", "kill"]
    if any(word in user_input.lower() for word in emergency_keywords):
        st.error("🚨 If you are in immediate danger, please call 112 or 181 immediately.")

    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.spinner("Analyzing your situation..."):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT}
            ] + st.session_state.messages,
            temperature=0.6,
            max_tokens=900,
        )

    reply = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

# ---------------------------------------------------
# COMPLAINT DRAFT GENERATOR
# ---------------------------------------------------
st.markdown("---")
st.markdown("## 📝 Generate Complaint Draft")

draft_details = st.text_area(
    "Enter details for complaint drafting (Names, Dates, Location, Incident Description):"
)

if st.button("Generate Complaint Draft"):

    if draft_details.strip() == "":
        st.warning("Please enter incident details first.")
    else:

        draft_prompt = f"""
        Draft a formal legal complaint letter in India based on the following details:

        Category: {category}
        Details:
        {draft_details}

        Structure:
        - To
        - Subject
        - Respected Sir/Madam
        - Detailed complaint narrative
        - Legal provisions involved
        - Request for action
        - Closing
        - Name & Signature placeholder

        Keep it formal and legally appropriate.
        """

        with st.spinner("Drafting complaint..."):
            draft_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "system", "content": draft_prompt}],
                temperature=0.5,
                max_tokens=900,
            )

        draft_text = draft_response.choices[0].message.content

        st.markdown("### 📄 Complaint Draft")
        st.markdown(draft_text)