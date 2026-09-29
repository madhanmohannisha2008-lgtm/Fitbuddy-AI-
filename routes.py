import os
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from app.schemas import WorkoutRequest, UserInput, FeedbackRequest
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan
from app.database import (
    SessionLocal,
    User,
    WorkoutPlan,
    save_user,
    save_plan,
    update_plan,
    get_original_plan,
    get_user,
)

load_dotenv(override=True)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ==========================================
# HTML FRONTEND ROUTES
# ==========================================

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.get("/generate-workout")
@router.get("/submit-feedback")
def redirect_to_home():
    return RedirectResponse(url="/", status_code=303)


@router.post("/generate-workout", response_class=HTMLResponse)
def handle_form_submission(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    save_user(
        user_id=user_id,
        name=username,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )

    plan = generate_workout_gemini({"goal": goal, "intensity": intensity})
    save_plan(user_id=user_id, plan=plan)
    nutrition_tip = generate_nutrition_tip_with_flash(goal)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "username": username,
            "user_id": user_id,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": plan,
            "nutrition_tip": nutrition_tip,
            "updated": False
        }
    )


@router.post("/submit-feedback", response_class=HTMLResponse)
def handle_feedback_submission(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...)
):
    user = get_user(user_id)
    original = get_original_plan(user_id)

    if not user or not original:
        raise HTTPException(status_code=404, detail="User or original workout plan not found.")

    updated = update_workout_plan(original, feedback)
    update_plan(user_id, updated)
    nutrition_tip = generate_nutrition_tip_with_flash(user.goal)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "username": user.name,
            "user_id": user.id,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "workout_plan": updated,
            "nutrition_tip": nutrition_tip,
            "updated": True
        }
    )


# 5. Web: View all users & their plans (Admin Panel)
@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    db = SessionLocal()
    try:
        users = db.query(User).all()
        user_data = []
        for user in users:
            plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user.id).first()
            user_data.append({
                "id": user.id,
                "name": user.name,
                "age": user.age,
                "weight": user.weight,
                "goal": user.goal,
                "intensity": user.intensity,
                "original_plan": plan.original_plan if plan else "N/A",
                "updated_plan": plan.updated_plan if plan and plan.updated_plan else "Not updated"
            })
    finally:
        db.close()

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={"users": user_data}
    )


# ==========================================
# REST API ROUTES (For Swagger UI / API Testing)
# ==========================================

# 1. API: Generate workout using Gemini
@router.post("/generate-workout-gemini")
async def generate_gemini_workout(request: WorkoutRequest):
    try:
        result = generate_workout_gemini({
            "goal": request.goal,
            "intensity": request.intensity
        })
        return {"model": os.getenv("GEMINI_MODEL"), "workout_plan": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 2. API: Generate nutrition tip using Gemini
@router.get("/nutrition-tip")
def get_flash_tip(goal: str):
    tip = generate_nutrition_tip_with_flash(goal)
    return {"goal": goal, "nutrition_tip": tip}


# 3. API: Save user info & generate plan
@router.post("/generate-plan")
def generate_plan(user_data: UserInput):
    try:
        save_user(
            user_id=user_data.user_id,
            name=user_data.username,
            age=user_data.age,
            weight=user_data.weight,
            goal=user_data.goal,
            intensity=user_data.intensity
        )
        plan = generate_workout_gemini({
            "goal": user_data.goal,
            "intensity": user_data.intensity
        })
        save_plan(user_data.user_id, plan)
        return {
            "message": "Workout plan generated and saved successfully",
            "workout_plan": plan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")


# 4. API: Update workout plan based on user feedback
@router.post("/update-plan/{user_id}", response_model=dict)
def update_user_plan(user_id: int, data: FeedbackRequest):
    original = get_original_plan(user_id)
    if not original:
        return {"error": "Original plan not found for this user."}

    updated = update_workout_plan(original, data.feedback)
    update_plan(user_id, updated)
    return {"updated_plan": updated}