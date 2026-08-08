# Simple Quiz Game

questions = [
    {
        "question": "1. What is the capital of India?",
        "answer": "Delhi"
    },
    {
        "question": "2. Which language is used for Python programming?",
        "answer": "Python"
    },
    {
        "question": "3. Who developed Python?",
        "answer": "Guido van Rossum"
    },
    {
        "question": "4. What does CPU stand for?",
        "answer": "Central Processing Unit"
    },
    {
        "question": "5. Which keyword is used to create a function in Python?",
        "answer": "def"
    }
]

score = 0

print("===== Welcome to the Quiz Game =====")

for q in questions:
    print("\n" + q["question"])
    user_answer = input("Your Answer: ")
    if user_answer.strip().lower() == q["answer"].lower():
        print("✅ Correct!")
        score += 1
    else:
        print("❌ Wrong!")
        print("Correct Answer:", q["answer"])

print("\n===== Quiz Finished =====")
print("Your Score:", score, "/", len(questions))

percentage = (score / len(questions)) * 100
print("Percentage:", percentage, "%")

if percentage >= 80:
    print("🎉 Excellent!")
elif percentage >= 50:
    print("👍 Good Job!")
else:
    print("📚 Keep Practicing!")
    