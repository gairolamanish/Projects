import time
import random
import threading
import google.generativeai as genai
import json, re
import streamlit as st


TIME_LIMIT = 20
user_answer = None

genai.configure(api_key="AIzaSyB_V9KsP7iRsQWpTZowOi0Bou0vJ8yDlJM")
model = genai.GenerativeModel("models/gemini-2.5-flash")

if "questions" not in st.session_state:
    st.session_state.questions = []
if "current" not in st.session_state:
    st.session_state.current = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "user_answer" not in st.session_state:
    st.session_state.user_answer = None
if "timer_start" not in st.session_state:
    st.session_state.timer_start = None
if "show_explanation" not in st.session_state:
    st.session_state.show_explanation = False
if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None    


def timer():
    """Simulate the countdown timer for UI"""
    if st.session_state.timer_start is None:
        st.session_state.timer_start = time.time()
    elapsed = int(time.time() - st.session_state.timer_start)
    return TIME_LIMIT - elapsed

def generate_questions():
    prompt = """
    Generate 20 multiple-choice questions for Class 10 Mathematics.
    Return ONLY JSON in this format:

    [
      {
        "question": "....",
        "options": ["A","B","C","D"],
        "answer": "B",
        "explanation": "...."
      }
    ]

    Ensure:
    - Exactly 20 MCQs
    - Class 10 level
    - Correct answer must match one option
    - Provide explanation
    """

    response = model.generate_content(prompt)
    parts = []
    for p in response.candidates[0].content.parts:
        if hasattr(p, "text"):
            parts.append(p.text)
    text = "\n".join(parts)

    text = text.replace("```json", "").replace("```", "").strip()
    text = re.sub(r"[\x00-\x1F\x7F]", " ", text)

    match = re.search(r"\[.*\]", text, re.DOTALL)
    if not match:
        st.error("❌ Could not extract JSON array from model output")
        st.code(text)
        return []

    json_str = match.group(0)

    try:
        data = json.loads(json_str)
    except Exception as e:
        st.error("❌ JSON Parsing Error: " + str(e))
        st.code(json_str)
        return []

    # Ensure explanation always exists
    for q in data:
        if not q.get("explanation"):
            q["explanation"] = "Explanation not provided by model."

    return data


def ask_question(q):
    st.subheader(f"Question {st.session_state.current + 1} of 20")
    st.write(q["question"])

    st.session_state.stored_answer = st.radio(
        "Choose an option:",
        q["options"],
        key=f"q_{st.session_state.current}"
    )

    elapsed = int(time.time() - st.session_state.timer_start)
    st.progress(min(elapsed / TIME_LIMIT, 1.0))

    return st.session_state.stored_answer

def process_answer(q, ans):
    if ans == q["answer"]:
        st.success("✅ Correct!")
        st.session_state.score += 1
    else:
        st.error(f"❌ Wrong! Correct answer: {q['answer']}")
    st.info(f"📘 Explanation: {q['explanation']}")


if not st.session_state.questions:
    st.write("Generating questions... ⏳")
    st.session_state.questions = generate_questions()
    random.shuffle(st.session_state.questions)
    st.session_state.timer_start = time.time()

# ------------------ CURRENT QUESTION ------------------
if st.session_state.current < len(st.session_state.questions):
    q = st.session_state.questions[st.session_state.current]
    ans = ask_question(q)
    
    if st.button("Submit Answer"):
        st.session_state.show_explanation = True
        st.session_state.selected_answer = ans
        st.rerun()

    if st.session_state.show_explanation:
        process_answer(q, st.session_state.selected_answer)

        if st.button("Next Question"):
            st.session_state.current += 1
            st.session_state.timer_start = time.time()
            st.session_state.show_explanation = False
            st.rerun()    
else:
    st.write(f"🎉 Quiz Finished! Your Score: {st.session_state.score}/{len(st.session_state.questions)}")
    if st.button("Restart Quiz"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()