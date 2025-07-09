"""
Vincent's Med AI — super‑simple Streamlit front‑end
WARNING: This is educational only; it can be wrong. Always verify with a qualified physician.
"""
import os
import io
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
st.set_page_config(page_title="Vincent's Med AI", page_icon="🩺")
st.title("🩺 Vincent's Medical AI Sample")

st.markdown(
    """
    **Hi, Doctor!** Paste a patient’s lab result **or upload a file** below and I’ll explain it in plain language.  
    I’ll also list **possible** medicine *classes* and next steps.

    > ⚠️ **Remember:** I’m just an AI helper, *not* a real doctor.  
    Use my notes for brainstorming and always double‑check with proper clinical guidelines.
    """
)

# 4️⃣ File upload (new!)
uploaded_file = st.file_uploader(
    "📂 Upload a lab‑result file (TXT or CSV)",
    type=["txt", "csv"],
    help="Supported formats: plain‑text .txt or comma‑separated .csv files.",
)
file_text = ""
if uploaded_file is not None:
    # Read the uploaded file
    try:
        bytes_content = uploaded_file.read()
        file_text = bytes_content.decode("utf-8")
    except Exception:
        st.warning("😕 I couldn't read that file. Please make sure it's plain text or CSV.")
        file_text = ""

# 5️⃣ Manual text area (kept for flexibility)
sample_text = """Hemoglobin A1C: 8.2% (High)\nLDL Cholesterol: 165 mg/dL (High)"""
lab_text_input = st.text_area(
    "…or paste the lab‑test text here:",
    placeholder=sample_text,
    height=150,
    value=file_text,  # pre‑fill with uploaded content if any
)

# Decide which text actually gets sent
final_text = file_text if file_text.strip() else lab_text_input

# 6️⃣ Handle button click
if st.button("🔍 Explain & Recommend"):
    if not final_text.strip():
        st.warning("Please upload a file or paste a lab result before clicking 😊")
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
        HumanMessage(content=f"Here is the lab result:\n{final_text}\n\nExplain and recommend."),
    ]

    with st.spinner("Thinking …"):
        try:
            response = llm(messages)
            st.success("Here’s my draft explanation:")
            st.write(response.content)
        except Exception as e:
            st.error(f"😓 Oops, something went wrong: {e}")

# 7️⃣ Footer
st.sidebar.info("Built with Streamlit, LangChain & GPT‑4o · July 2025")
