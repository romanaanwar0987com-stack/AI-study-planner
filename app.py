import streamlit as st
from agent import generate_study_plan, save_to_history, load_history
from mypdf import create_pdf
from datetime import date
import os

st.set_page_config(page_title="AI Study Planner", page_icon="📚", layout="centered")
st.title("📚 AI Study Planner Agent")
st.markdown("*Generate your personalized study plan powered by AI*")

with st.form("study_form"):
    subjects = st.text_input("📖 Subjects", placeholder="e.g. Math, Physics, Chemistry")
    weak_topics = st.text_input("😟 Weak Topics", placeholder="e.g. Calculus, Thermodynamics")
    exam_date = st.date_input("📅 Exam Date", min_value=date.today())
    hours_per_day = st.slider("⏰ Study Hours Per Day", 1, 12, 4)
    difficulty = st.selectbox("🎯 Difficulty Level", ["Easy", "Medium", "Hard"])
    submitted = st.form_submit_button("🚀 Generate Study Plan")

if submitted:
    if not subjects or not weak_topics:
        st.warning("Please fill in all fields!")
    else:
        with st.spinner("🤖 AI is creating your plan..."):
            plan = generate_study_plan(subjects, weak_topics, exam_date, hours_per_day, difficulty)
            save_to_history(subjects, weak_topics, exam_date, plan)

        st.success("✅ Your Study Plan is Ready!")
        st.markdown(plan)

        pdf_path = create_pdf(subjects, weak_topics, str(exam_date), hours_per_day, difficulty, plan)
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📥 Download PDF",
                data=f,
                file_name="study_plan.pdf",
                mime="application/pdf"
            )

st.markdown("---")
st.subheader("📜 Previous Study Plans")

history = load_history()
if not history:
    st.info("No history yet. Generate your first plan above!")
else:
    for i, item in enumerate(reversed(history)):
        with st.expander(f"📅 {item['date']} — {item['subjects']}"):
            st.markdown(f"**Exam Date:** {item['exam_date']}")
            st.markdown(f"**Weak Topics:** {item['weak_topics']}")
            st.markdown(item['plan'])