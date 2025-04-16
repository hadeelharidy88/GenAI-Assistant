import streamlit as st
import google.generativeai as genai
import os

# Setup Google Generative AI
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", "AIzaSyATIUK_dvY0rg_FONGW1668--IwlMrFVyo")
GOOGLE_PROJECT = st.secrets.get("GOOGLE_PROJECT", "analog-grin-455718-i4")
GOOGLE_LOCATION = st.secrets.get("GOOGLE_LOCATION", "us-east1")

genai.configure(api_key=GOOGLE_API_KEY)

model = "gemini-1.5-pro-002"

# Define your prompts
question_list = [
    "How can I extend this class to include multiplication and division methods?",
    "Please provide test cases for the addition class.",
    "Please provide test cases for different functions in this code.",
    "Please provide the scope for this document.",
    "Please provide a brief about this project for the HR manager highlighting the skills needed for a developer who will extend this project.",
    "Please suggest edits in code formatting to support OOP disciplines."
]

# Helper to format the prompt
def create_prompt(code, question):
    return f"""You are a knowledgeable software assistant. Analyze the following document and answer the subsequent question.

[CODE START]
{code}
[CODE END]

Question: {question}
Please provide a clear and concise answer. If you generate code, make sure it is runnable given the code above (Don't include placeholders).
"""

# Streamlit App UI
st.title("📄 Code Review with Gemini AI")
st.write("Upload your code file and select a question to analyze it using Google's Gemini model.")

uploaded_file = st.file_uploader("Upload a .txt or .py file", type=["txt", "py"])
question = st.selectbox("Choose a question to ask Gemini:", question_list)

if uploaded_file and question:
    code = uploaded_file.read().decode("utf-8")

    # Run Gemini model
    try:
        client = genai.GenerativeModel(model)
        response = client.generate_content(create_prompt(code, question))
        st.subheader("💬 Gemini's Response")
        st.write(response.text.strip())
    except Exception as e:
        st.error(f"Error: {e}")