import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# ---------------- LOAD ENV ----------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found in .env file")
    st.stop()

client = Groq(api_key=api_key)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Code Review & Rewrite Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Code Review & Rewrite Agent")
st.markdown("### 🚀 Powered by Groq + Llama 3.3 70B")

st.divider()

# ---------------- USER INPUT ----------------

language = st.selectbox(
    "Select Programming Language",
    ["Python", "Java", "C++", "JavaScript", "C", "Other"]
)

code_input = st.text_area(
    "Paste your code below:",
    height=300,
    placeholder="Paste your source code here..."
)

st.divider()

col1, col2 = st.columns(2)

# ---------------- PROMPT FUNCTIONS ----------------

def code_review_prompt(code, language):
    return f"""
You are a senior software engineer performing a professional code review.

Carefully analyze the following {language} code.

Categorize findings into:
1. Critical Issues
2. High Priority Issues
3. Medium Priority Issues
4. Low Priority Issues

For each issue:
- Describe the problem
- Explain why it matters
- Provide a fix suggestion

Here is the code to review:

{code}

Now provide the structured review.
"""



def code_rewrite_prompt(code, language):
    return f"""
You are a senior software engineer.

Rewrite the following {language} code to be optimized, secure, clean,
production-ready, and properly formatted.

Maintain original functionality.
Add meaningful comments if necessary.

Here is the code:

{code}

Return ONLY the improved code.
"""


# ---------------- REVIEW BUTTON ----------------

with col1:
    if st.button("🔍 Review Code"):
        if not code_input.strip():
            st.warning("Please paste code before reviewing.")
        else:
            with st.spinner("Analyzing code..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a professional AI code reviewer."},
                        {"role": "user", "content": code_review_prompt(code_input, language)}
                    ],
                    temperature=0.2,
                    max_tokens=1200
                )

                review_output = response.choices[0].message.content

                st.subheader("📋 Code Review Report")
                st.markdown(review_output)

# ---------------- REWRITE BUTTON ----------------

with col2:
    if st.button("♻️ Rewrite Code"):
        if not code_input.strip():
            st.warning("Please paste code before rewriting.")
        else:
            with st.spinner("Rewriting code..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a senior AI engineer rewriting code."},
                        {"role": "user", "content": code_rewrite_prompt(code_input, language)}
                    ],
                    temperature=0.1,
                    max_tokens=1200
                )

                rewritten_code = response.choices[0].message.content

                st.subheader("✅ Optimized Code")
                st.code(rewritten_code, language=language.lower())

