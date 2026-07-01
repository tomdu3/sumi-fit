# SumiFit app

## 1. Feasibility Assessment

This project is **highly feasible** for a single developer, provided you break it down into modular phases.

* **Backend (Flask):** Excellent choice. Flask’s lightweight nature makes it easy to quickly build RESTful endpoints for your dashboard data and write clean, decoupled Python modules to interact with external AI APIs.
* **Data Aggregation:** Handled via OAuth2 authentication. You will fetch data points (Steps, Sleep Sessions, Calories) from Google’s endpoints, serialize them, and store them locally in a database (like PostgreSQL or SQLite) for quick retrieval.
* **AI Integration:** Instead of trying to build or fine-tune models from scratch, you can use API wrappers (like the `google-genai` SDK or `openai`) to act as a multi-agent consultant. You pass the user's structured data as context to get personalized advice.

---

## 2. Overall Architectural Plan

### A. The Tech Stack

* **Core Backend:** Flask, Blueprint (for modular routing), SQLAlchemy (ORM).
* **Environment & Package Management:** `uv` for lightning-fast dependency management and virtual environments.
* **Task Queue:** `Celery` or `Redis Queue (RQ)` to handle asynchronous background tasks (like fetching heavy weekly api logs or waiting for AI responses without freezing the UI).
* **Data Visualization:** `Chart.js` or `Plotly.js` on the frontend, parsing JSON arrays served by your Flask backend.
* **AI Layer:** Structured prompting via an LLM API wrapper (e.g., Gemini Flash or GPT-4o-mini for cost-effective speed).

### B. Core Database Schema (Relational)

You will need a clean relational mapping to track metrics over time:

* **User Profile:** Preferences, daily calorie targets, sleep goals, workout style.
* **Activity Logs:** Timestamps, data type (`steps`, `active_minutes`, `sleep_minutes`), and values.
* **Nutrition Logs:** Food items, weights, and macronutrient breakdowns.
* **AI Insights Cache:** Saved analysis records so you don't re-run expensive LLM requests every time you refresh the page.

---

## 3. Step-by-Step Implementation Guide

### Phase 1: Authentication & Health Ingestion (The Foundation)

1. **Set up Google Cloud Platform (GCP):** Register an application in the Google API Console, configure your OAuth consent screen, and enable the relevant health/fitness read scopes.
2. **OAuth2 Flow:** Use `requests-oauthlib` in Flask to handle user authorization, token exchange, and automatic token refreshing.
3. **The Ingestion Pipeline:** Create a sync route that calls Google's endpoints to fetch the last 7 days of metrics and merges them into your database.

### Phase 2: Analytics & Dashboarding

1. **Aggregate Metrics:** Write helper utilities in Python to compute rolling averages for your sleep efficiency and calorie balances.
2. **Build RESTful Endpoints:** Create routes like `/api/stats/weekly` that yield structured JSON:
```json
{
  "dates": ["2026-06-25", "2026-06-26", "2026-06-27"],
  "steps": [8400, 10200, 6100],
  "sleep_hours": [7.2, 6.8, 8.1]
}

```


3. **Frontend Render:** Connect these endpoints to modern frontend components using Tailwind CSS for a clean look, utilizing simple JavaScript charting libraries to render the visual graphs.

### Phase 3: The AI Advisory Engine (Structured Context)

To make your AI feature genuinely useful and prevent it from hallucinating or giving generic advice, use **Structured Inputs/Outputs** (Function Calling or JSON schema modes).

Instead of sending a messy prompt, construct a structured context object:

```python
# Pseudo-logic for your AI engine module
def generate_health_advice(user_metrics, user_preferences):
    prompt = f"""
    You are an expert athletic coach and clinical nutritionist. 
    Analyze the following 7-day user snapshot:
    - Average Sleep: {user_metrics.avg_sleep} hours
    - Daily Step Average: {user_metrics.avg_steps}
    - Logged Calories Input: {user_metrics.avg_calories_in} kcal
    - User Preferences: {user_preferences.workout_style} (Prefers: {user_preferences.equipment})
    
    Provide actionable advice structured exactly in JSON format with three keys: 
    'nutrition_adjustments', 'sleep_optimization', and 'suggested_workout_plan'.
    """
    # Call your preferred LLM Client here using JSON mode
    response = client.generate_content(prompt, response_mime_type="application/json")
    return response.text

```

### Phase 4: Calorie & Workout Planner

1. **Calorie Tracker:** Create a straightforward interface to input food. You can include a simple text box ("I ate two boiled eggs and avocado toast") and let the AI extract the ingredients and approximate macronutrients, saving them straight into your `Nutrition Log` table.
2. **Workout Scheduler:** Use the AI engine to output a 3-day split matching the user's specific preferences, saving the generated plan to the database so the user can check off exercises as they complete them.

---

## 4. Immediate Next Steps

To begin developing with clean patterns, start with a minimal skeleton:

1. Initialise a clean directory structure using `uv init`.
2. Install your core dependencies: `uv add flask flask-sqlalchemy requests-oauthlib`.
3. Set up a simple test route confirming your SQLite/Postgres database initializes correctly.
4. Download your client secrets JSON from the Google Cloud Console to start writing your OAuth2 handshake.
