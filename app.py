
---
## app.py
```python
"""
MedBuddy AI — super‑simple Streamlit front‑end
WARNING: This is **educational only**; it can be wrong.  Always verify with a qualified physician.
"""
import os
import streamlit as st
from dotenv import load_dotenv

# LangChain lets us chat with the model more easily
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# 1️⃣ load the secret key
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    st.error("❌ Please set an OPENAI_API_KEY in a .env file or Streamlit secret.")
    st.stop()

# 2️⃣ create the chat model (uses GPT‑4o by default)
llm = ChatOpenAI(
    model="gpt-4o",       # fast + smart model, adjust if you like
    temperature=0.25,      # low temp = safer, less creative
    openai_api_key=openai_key,
)

# 3️⃣ Streamlit page layout
st.set_page_config(page_title="MedBuddy AI", page_icon="🩺")
st.title("🩺 MedBuddy AI (draft)")

st.markdown(
    """
    **Hi, Doctor!** Paste a patient’s lab result below and I’ll explain it in plain language.  I’ll also list **possible** medicine *classes* (not specific brands) and next steps.

    > ⚠️ **Remember:** I’m just an AI helper, *not* a real doctor.  Use my notes for brainstorming and always double‑check with proper clinical guidelines.
    """
)

# 4️⃣ User input
sample_text = """Hemoglobin A1C: 8.2% (High)\nLDL Cholesterol: 165 mg/dL (High)"""
lab_text = st.text_area(
    "Paste the lab‑test text here:",
    placeholder=sample_text,
    height=150,
)

# 5️⃣ When the doctor clicks the button, call the model
if st.button("🔍 Explain & Recommend"):
    if not lab_text.strip():
        st.warning("Please paste a lab result before clicking 😊")
        st.stop()

    # build the conversation
    messages = [
        SystemMessage(
            content=(
                "You are a compassionate medical doctor AI assistant. "
                "You read lab results supplied by a human doctor and explain them in simple terms. "
                "You may suggest *general* medicine classes (e.g., 'statins', 'ACE inhibitors') or lifestyle tips, "
                "but you never prescribe exact doses or brand names. "
                "Always remind the reader to confirm with a licensed physician."
            )
        ),
        HumanMessage(content=f"Here is the lab result:\n{lab_text}\n\nExplain what it means and suggest possible medicine classes or next steps."),
    ]

    with st.spinner("Thinking …"):
        try:
            response = llm(messages)
            st.success("Here’s my draft explanation:")
            st.write(response.content)
        except Exception as e:
            st.error(f"😓 Oops, something went wrong: {e}")

# 6️⃣ Footer
st.sidebar.info("Built with Streamlit, LangChain & GPT‑4o · July 2025")