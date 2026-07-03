import json
import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
st.set_page_config(page_title="AI Task Automation", page_icon="⚡", layout="wide")
st.title("AI Task Automation System")
st.caption("Summarize emails, identify actions, set priority, and draft replies.")

api_key = os.getenv("GROQ_API_KEY", "")
model = st.sidebar.selectbox("Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"])
if not api_key:
    st.sidebar.error("GROQ_API_KEY is not configured.")

def ask(prompt):
    client = Groq(api_key=api_key)
    result = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}], temperature=0.2)
    return result.choices[0].message.content

tab1, tab2 = st.tabs(["Email workflow", "Batch processing"])
with tab1:
    email = st.text_area("Email content", height=240, placeholder="Paste an email here...")
    tone = st.selectbox("Reply tone", ["Professional", "Friendly", "Concise", "Formal"])
    if st.button("Process email", type="primary"):
        if not api_key or not email.strip():
            st.error("Add a Groq API key and email content.")
        else:
            prompt = f'''Analyze this email and return valid JSON only with keys summary, priority, category, action_items, deadline, reply. The reply tone is {tone}. Email:\n{email}'''
            with st.spinner("Running workflow..."):
                try:
                    raw = ask(prompt).strip().removeprefix("```json").removesuffix("```").strip()
                    data = json.loads(raw)
                    a, b, c = st.columns(3)
                    a.metric("Priority", data.get("priority", "Unknown"))
                    b.metric("Category", data.get("category", "General"))
                    c.metric("Deadline", data.get("deadline", "Not found"))
                    st.subheader("Summary")
                    st.write(data.get("summary", ""))
                    st.subheader("Action items")
                    for item in data.get("action_items", []):
                        st.checkbox(item)
                    st.subheader("Suggested reply")
                    st.text_area("Edit before sending", data.get("reply", ""), height=180)
                except Exception as error:
                    st.error(str(error))
with tab2:
    upload = st.file_uploader("Upload CSV with a column named email", type="csv")
    if upload and st.button("Process CSV"):
        if not api_key:
            st.error("Add a Groq API key.")
        else:
            frame = pd.read_csv(upload)
            if "email" not in frame.columns:
                st.error("The CSV must contain an email column.")
            else:
                results = []
                progress = st.progress(0)
                for index, value in enumerate(frame["email"].fillna("")):
                    results.append(ask(f"Summarize this email in one sentence and state its priority: {value}"))
                    progress.progress((index + 1) / len(frame))
                frame["ai_result"] = results
                st.dataframe(frame, use_container_width=True)
                st.download_button("Download results", frame.to_csv(index=False), "processed_emails.csv", "text/csv")
