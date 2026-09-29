import os
import google.generativeai as genai
from dotenv import load_dotenv


def generate_nutrition_tip_with_flash(goal: str) -> str:
    """
    Generate a concise nutrition or recovery tip based on the user's fitness goal.
    """
    load_dotenv(override=True)
    api_key = os.getenv("GOOGLE_API_KEY")
    model_name = os.getenv("GEMINI_MODEL")

    if not api_key or not model_name:
        return "Error: GOOGLE_API_KEY or GEMINI_MODEL is missing in the .env file."

    genai.configure(api_key=api_key)

    prompt = (
        f"Give one clear, helpful nutrition or recovery tip (maximum 2 sentences) "
        f"for someone focused on '{goal}'. "
        "The tip should be practical, friendly, and easy to understand."
    )
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        if response.candidates and response.candidates[0].content.parts:
            return response.text.strip()
        return "Stay hydrated and prioritize protein after your workouts to support recovery."
    except Exception as e:
        return f"Error generating tip: {str(e)}"