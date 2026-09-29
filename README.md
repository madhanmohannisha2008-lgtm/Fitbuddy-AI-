# 💪 FitBuddy – AI Fitness Plan Generator using Gemini Models

**FitBuddy** is a web-based AI application built with **FastAPI**, **Google Gemini Models**, **SQLite (SQLAlchemy ORM)**, and **Jinja2 HTML Templates**. It generates personalized 7-day workout routines and actionable nutrition/recovery tips tailored to a user's fitness goals and preferred workout intensity, while allowing dynamic plan revisions through user feedback.

---

## 🌟 Key Features & Scenarios

1. **Personalized 7-Day Workout Plan Generation:**
   Users enter their name, user ID, age, weight, fitness goal (e.g., *weight loss*, *muscle gain*, *general wellness*), and workout intensity (*Low*, *Medium*, *High*) to receive a structured day-by-day workout schedule containing warm-ups, main exercises (sets & reps), and cooldowns.
2. **Dynamic Feedback-Based Plan Updating:**
   Users can submit natural-language feedback on their generated plan (e.g., *"Add more cardio"* or *"Include 15 minutes of yoga in the cooldown"*), and Gemini refines the existing schedule while keeping the structure intact.
3. **AI Nutrition & Recovery Tips:**
   Delivers concise, practical nutrition or recovery advice tailored to the user's primary fitness goal alongside every generated workout plan.
4. **Coach / Admin Dashboard (`/view-all-users`):**
   Provides an overview table of all registered users, comparing their original and updated workout plans side by side.

---

## 🛠️ Tech Stack

* **Backend Framework:** FastAPI (Python)
* **ASGI Server:** Uvicorn
* **AI / LLM Layer:** Google Generative AI SDK (`google-generativeai` – Gemini Models)
* **Database & ORM:** SQLite (`fitbuddy.db`) + SQLAlchemy
* **Data Validation:** Pydantic
* **Frontend:** HTML5, CSS3, Jinja2 Templates

---

## 📂 Project Structure

```text
fitbuddy/
├── .env                          # Stores GOOGLE_API_KEY
├── requirements.txt              # Project Python dependencies
├── run.bat                       # One-click Windows setup & launch script
├── README.md                     # Project documentation
├── fitbuddy.db                   # Auto-generated SQLite database
├── app/
│   ├── __init__.py               # Package initializer
│   ├── main.py                   # FastAPI entry point & static file mounting
│   ├── routes.py                 # Web UI & REST API route handlers
│   ├── database.py               # SQLAlchemy models (User, WorkoutPlan) & CRUD logic
│   ├── schemas.py                # Pydantic request validation models
│   ├── gemini_generator.py       # 7-day workout plan generator
│   ├── gemini_flash_generator.py # Nutrition & recovery tip generator
│   ├── updated_plan.py           # Feedback-based workout plan updater
│   └── nutrition.py              # Nutrition helper module
├── templates/
│   ├── index.html                # User input form page
│   ├── result.html               # Workout plan, nutrition tip & feedback page
│   └── all_users.html            # Admin dashboard viewing all users & plans
└── static/
    └── images/
        └── gym-bg.jpg            # Background asset
```

---

## 🚀 Getting Started

### Prerequisites
* **Python 3.10+** installed and added to your system `PATH`
* A **Google Gemini API Key** (from [Google AI Studio](https://aistudio.google.com/))

### Option A: Quick Start on Windows (`run.bat`)
1. Create a `.env` file in the project root and add your API key:
   ```ini
   GOOGLE_API_KEY=your_actual_gemini_api_key_here
   ```
2. Double-click **`run.bat`** (or run `.\run.bat` in your terminal).
3. The script will automatically create `venv`, install all requirements, start the Uvicorn server, and open `http://127.0.0.1:8000` in your browser.

### Option B: Manual Setup (Windows / macOS / Linux)
1. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment variables:**
   Create a `.env` file in the root folder:
   ```ini
   GOOGLE_API_KEY=your_actual_gemini_api_key_here
   ```
4. **Run the FastAPI server:**
   ```bash
   uvicorn app.main:app --reload
   ```

---

## 🌐 Application URLs & API Endpoints

### Web Interface Routes
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Renders `index.html` user input form |
| `POST` | `/generate-workout` | Saves user, generates 7-day plan + tip, renders `result.html` |
| `POST` | `/submit-feedback` | Updates user's workout plan via feedback, renders `result.html` |
| `GET` | `/view-all-users` | Renders `all_users.html` Admin Dashboard |

### REST API Endpoints (Testable via `/docs`)
| Method | Endpoint | Request Body / Query | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/generate-workout-gemini` | `{"goal": "muscle gain", "intensity": "high"}` | Generates a 7-day workout plan via JSON |
| `GET` | `/nutrition-tip?goal=weight loss` | Query param: `goal` | Returns a quick nutrition/recovery tip |
| `POST` | `/generate-plan` | `UserInput` JSON payload | Saves user & plan to SQLite and returns JSON |
| `POST` | `/update-plan/{user_id}` | `{"feedback": "Add more rest days"}` | Updates an existing user's workout plan |

---

## 🧪 Testing Checklist

1. **Web Form Generation:** Open `http://127.0.0.1:8000`, submit user details, and verify that the 7-day plan and nutrition tip display on the results page.
2. **Feedback Loop:** On the results page, enter feedback in the **Share Your Feedback** box and submit to verify the updated plan and green confirmation banner.
3. **Admin View:** Navigate to `http://127.0.0.1:8000/view-all-users` and confirm both `Original Plan` and `Updated Plan` columns are populated.
4. **Swagger UI:** Open `http://127.0.0.1:8000/docs` to test the standalone JSON API endpoints interactively.