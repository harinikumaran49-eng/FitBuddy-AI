import os

from flask import Blueprint, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

routes = Blueprint("routes", __name__)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_PLAN_MODEL", "gemini-2.5-flash")

client = genai.Client(api_key=API_KEY) if API_KEY else None


@routes.route("/")
def home():
    return render_template("index.html")


@routes.route("/generate", methods=["POST"])
def generate_plan():

    if client is None:
        return jsonify({
            "error": "Gemini API key is missing. Check your .env file."
        }), 500

    data = request.get_json()

    age = data.get("age", "")
    goal = data.get("goal", "")
    activity = data.get("activity", "")
    days = data.get("days", "5")
    preferences = data.get("preferences", "")

    prompt = f"""
You are FitBuddy AI, a friendly general wellness assistant.

Create a safe and beginner-friendly fitness and wellness plan.

User information:
Age: {age}
Goal: {goal}
Current activity level: {activity}
Days per week: {days}
Preferences: {preferences}

Give:
1. Weekly workout plan
2. Simple warm-up
3. Cool-down
4. General healthy eating suggestions
5. Rest and recovery suggestions
6. Safety reminders

Do not promote extreme dieting, rapid weight loss, body shaming,
or unsafe exercise. Keep the advice general and age-appropriate.

Format the answer clearly with headings and bullet points.
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return jsonify({
            "plan": response.text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500