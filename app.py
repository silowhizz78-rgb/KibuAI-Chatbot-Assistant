from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    system_prompt = """
    You are KibuAI, an intelligent virtual assistant designed for Kibu University students. 
    You have deep knowledge about:
    - Student venues, departments, hostels, and campus locations.
    - School fees payment via Jiunge App.
    - Vaccination cards and hospital/health issues.
    - Curriculum and courses offered at the university.
    - General student support, help desks, and administrative guidance.

    Your tone is friendly, respectful, and helpful.
    Always give clear, short answers unless more detail is needed.
    When unsure, guide the student to visit the right office (e.g., Finance, Registrar, or Health Center).
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        bot_reply = response.choices[0].message.content
        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
