import os
from flask import Flask, render_template, request
import google.generativeai as genai

# Load API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment.")

genai.configure(api_key=api_key)

app = Flask(__name__)

# Use Gemini flash model
model = genai.GenerativeModel("gemini-flash-latest")


def get_gift_ideas(name: str, relationship: str, interests: str, budget: str) -> str:
    prompt = f"""
You are a friendly gift recommendation assistant.

Person details:
- Name/label: {name}
- Relationship: {relationship}
- Interests/hobbies/style: {interests}
- Budget: {budget}

Your task:
- Suggest 5–10 specific, creative gift ideas.
- Each idea MUST include:
  1. A short, clear gift name
  2. A brief explanation (1–2 sentences)
  3. A realistic price range that fits the budget
  4. A direct link (Amazon, Etsy, Target, or other reasonable site)
     → If you can’t find an exact product, use a relevant keyword-search link.

Formatting:
- Use a numbered list.
- Bold the gift names.
- Place each link on a new line under the idea.
- Keep the tone warm and simple.
- Make sure all links begin with https://
"""
    response = model.generate_content(prompt)
    return response.text.strip()


@app.route("/", methods=["GET", "POST"])
def index():
    ideas = None
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        relationship = request.form.get("relationship", "").strip()
        interests = request.form.get("interests", "").strip()
        budget = request.form.get("budget", "").strip()

        if not (name and relationship and interests and budget):
            error = "Please fill out all fields."
        else:
            try:
                ideas = get_gift_ideas(name, relationship, interests, budget)
            except Exception as e:
                error = f"Something went wrong while generating ideas: {e}"

    return render_template("index.html", ideas=ideas, error=error)


if __name__ == "__main__":
    # For local testing
    app.run(debug=True)
