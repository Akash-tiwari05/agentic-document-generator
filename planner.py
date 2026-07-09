import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from state import AgentState
from schemas import ExecutionPlan
from prompts import PLANNER_PROMPT

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)

def planning_node(state: AgentState) -> dict:
    prompt = PLANNER_PROMPT.format(user_request=state["user_request"])
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ExecutionPlan,
            temperature=0.2,
        ),
    )
    
    plan = ExecutionPlan.model_validate_json(response.text)
    
    return {
        "plan": plan,
        "tasks_to_execute": plan.tasks,
        "current_task_index": 0,
        "logs": state.get("logs", []) + ["Autonomous execution plan constructed successfully."]
    }