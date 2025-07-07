# MedBuddy AI (draft)

A kid‑friendly demo that turns lab‑test text into an easy explanation and **possible** medicine classes.  It is **NOT** real medical advice—always talk to a licensed doctor!

### Quick start

```bash
# 1) clone or download the folder
cd medbuddy-ai

# 2) create and activate a virtual env (Windows example)
python -m venv venv
venv\Scripts\activate

# 3) install packages
pip install -r requirements.txt

# 4) add your OpenAI key (same folder)
copy con .env
OPENAI_API_KEY="sk‑REPLACE_ME"
^Z  # (Ctrl+Z then Enter to save)

# 5) run locally
streamlit run app.py