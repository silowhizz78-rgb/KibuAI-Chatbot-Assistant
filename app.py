from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# Make sure you have your OpenAI API key in Render environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """
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
                },
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = response["choices"][0]["message"]["content"]
        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
