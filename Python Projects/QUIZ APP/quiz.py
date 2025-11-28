import time
import random
import threading
import google.generativeai as genai
import json


TIME_LIMIT = 20
user_answer = None

genai.configure(api_key="AIzaSyB_V9KsP7iRsQWpTZowOi0Bou0vJ8yDlJM")
model = genai.GenerativeModel("models/gemini-2.5-flash")


def timer():
    global user_answer
    for _ in range(TIME_LIMIT):
        time.sleep(1)
        if user_answer is not None:
            return
    print("\n⏳ Time's up! Try again")
    user_answer = ""

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
    text = response.text

    text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)


def ask_question(q):
    global user_answer
    user_answer = None

    print("📘 Question:", q["question"])

    for i, opt in enumerate(q["options"], 1):
        print(f"{i}. {opt}")

    t = threading.Thread(target=timer)
    t.start()

    try:
        user_answer = input(f"\nYour Answer (1–4) | Timer {TIME_LIMIT}s: ")
    except:
        user_answer = ""

    t.join()
    return user_answer

def start_quiz():
    print("Good Luck")
    questions = generate_questions()
    random.shuffle(questions)

    score = 0

    for q in questions:
        ans = ask_question(q)

        if not ans.isdigit():
            print("❌ Invalid answer / Timeout!")
            print("✔ Correct Answer:", q["answer"])
            print("📘 Explanation:", q["explanation"])
            continue

        idx = int(ans) - 1

        if q["options"][idx] == q["answer"]:
            print("✅ Correct!")
            score += 1
        else:
            print("❌ Wrong!")

        print("✔ Correct Answer:", q["answer"])
        print("📘 Explanation:", q["explanation"])

    
    print(f"Your Score: {score}/{len(questions)}")


if __name__ == "__main__":
    start_quiz()

