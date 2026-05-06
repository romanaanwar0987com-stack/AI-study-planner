from groq import Groq
from datetime import date
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_study_plan(subjects, weak_topics, exam_date, hours_per_day, difficulty):
    prompt = f"""You are an expert study planner. Create a comprehensive study plan:

*Student Info:*
- Subjects: {subjects}
- Weak Topics: {weak_topics}
- Exam Date: {exam_date}
- Study Hours Per Day: {hours_per_day}
- Difficulty Level: {difficulty}

Please provide:
1. DAILY STUDY SCHEDULE
   - Day-by-day plan until exam
   - Extra focus on weak topics

2. WEAK TOPICS ANALYSIS
   - Each weak topic importance
   - How to improve

3. TOPIC-WISE TIPS & TRICKS
   - Smart tricks for each subject
   - Memory techniques

4. PRACTICE QUESTIONS
   - 3 questions per weak topic"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048
    )
    return response.choices[0].message.content


def save_to_history(subjects, weak_topics, exam_date, plan):
    history = load_history()
    history.append({
        "date": str(date.today()),
        "subjects": subjects,
        "weak_topics": weak_topics,
        "exam_date": str(exam_date),
        "plan": plan
    })
    with open("history.json", "w") as f:
        json.dump(history, f, indent=2)


def load_history():
    if not os.path.exists("history.json"):
        return []
    with open("history.json", "r") as f:
        return json.load(f)