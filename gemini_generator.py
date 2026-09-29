import os
import google.generativeai as genai
from dotenv import load_dotenv


def generate_workout_gemini(user_input: dict) -> str:
    load_dotenv(override=True)
    api_key = os.getenv("GOOGLE_API_KEY")
    model_name = os.getenv("GEMINI_MODEL")

    if not api_key or not model_name:
        return "Error: GOOGLE_API_KEY or GEMINI_MODEL is missing in the .env file."

    genai.configure(api_key=api_key)

    prompt = f"""
You are a professional fitness trainer.

Create a concise, structured 7-day workout plan for someone with the goal of **{user_input['goal']}**, and prefers **{user_input['intensity']} intensity** workouts. Keep each day brief (1 short line per item).

Each day must include:
- Warm-up (5-10 mins)
- Main Workout (3-4 exercises with sets & reps)
- Cooldown

Format:
Day 1:
Warm-up: ...
Main Workout: ...
Cooldown: ...
(Repeat for Day 2-7)
"""
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        if response.candidates and response.candidates[0].content.parts:
            return response.text.strip()
        return "Unable to generate workout plan. Please try again."
    except Exception as e:
        return f"Error generating workout plan: {str(e)}"