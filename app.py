"""
Vincent's Med AI — super‑simple Streamlit front‑end
WARNING: This is educational only; it can be wrong. Always verify with a qualified physician.
"""
import os
import streamlit as st
from dotenv import load_dotenv

# 👉 Correct LangChain imports (v0.2+)
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1️⃣ Load the secret key
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    st.error("❌ Please set an OPENAI_API_KEY in a .env file or Streamlit secret.")
    st.stop()

# 2️⃣ Create the chat model
llm = ChatOpenAI(
    model="gpt-4o",      # fast + smart model, adjust if you like
    temperature=0.25,    # low temp = safer, less creative
    openai_api_key=openai_key,
)

# 3️⃣ Streamlit layout
st.set_page_config(page_title=" Vincent's Med AI", page_icon="🩺")
st.title("🩺 Vincent's Medical AI Sample")

st.markdown(
    """
    **Hi, Doctor!** Paste a patient’s lab result below and I’ll explain it in plain language.  
    I’ll also list **possible** medicine *classes* and next steps.

    > ⚠️ **Remember:** I’m just an AI helper, *not* a real doctor.  
    Use my notes for brainstorming and always double‑check with proper clinical guidelines.
    """
)

# 4️⃣ Get user input
sample_text = """Hemoglobin A1C: 8.2% (High)\nLDL Cholesterol: 165 mg/dL (High)"""
lab_text = st.text_area(
    "Paste the lab‑test text here:",
    placeholder=sample_text,
    height=150,
)

# 5️⃣ Handle button click
if st.button("🔍 Explain & Recommend"):
    if not lab_text.strip():
        st.warning("Please paste a lab result before clicking 😊")
        st.stop()

    messages = [
        SystemMessage(
            content=(
                "You are a compassionate medical doctor AI assistant. "
                "Explain lab results in simple terms. "
                "You can suggest general medicine classes or tips, "
                "but don’t give exact doses or drug names. "
                "Always tell the reader to confirm with a licensed doctor."
            )
        ),
        HumanMessage(content=f"Here is the lab result:\n{lab_text}\n\nExplain and recommend."),
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
