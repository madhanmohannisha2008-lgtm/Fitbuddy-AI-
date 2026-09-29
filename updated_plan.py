import os
import google.generativeai as genai
from dotenv import load_dotenv


def update_workout_plan(original_plan: str, user_feedback: str) -> str:
    """
    Update the workout plan based on user feedback.
    """
    load_dotenv(override=True)
    api_key = os.getenv("GOOGLE_API_KEY")
    model_name = os.getenv("GEMINI_MODEL")

    if not api_key or not model_name:
        return "Error: GOOGLE_API_KEY or GEMINI_MODEL is missing in the .env file."

    genai.configure(api_key=api_key)

    prompt = f"""
You are a professional fitness trainer assistant.

Here's the original 7-day workout plan:
{original_plan}

User Feedback:
"{user_feedback}"

Based on the feedback, revise the relevant parts of the workout plan concisely. Keep the format and rest of the plan unchanged if not needed.
"""
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        if response.candidates and response.candidates[0].content.parts:
            return response.text.strip()
        return original_plan
    except Exception as e:
        return f"Error updating plan: {str(e)}"