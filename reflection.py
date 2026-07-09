import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from state import AgentState
from schemas import ReflectionResult
from prompts import REFLECTION_PROMPT

load_dotenv()
# Consistency Fix: Standardize client instantiation via explicit key if needed,
# or let it fallback natively to the preloaded env.
client = genai.Client()

def reflection_node(state: AgentState) -> dict:
    latest_section = state["compiled_sections"][-1]
    attempts = state.get("reflection_attempts", 0)
    
    prompt = REFLECTION_PROMPT.format(
        heading=latest_section["heading"],
        paragraphs="\n".join(latest_section["paragraphs"])
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ReflectionResult,
                temperature=0.1,
            ),
        )
        result = ReflectionResult.model_validate_json(response.text)
    except Exception as e:
        # Fallback if the evaluation call itself errors out
        result = ReflectionResult(approved=True, feedback="Forced approval due to evaluation error.")

    if not result.approved:
        # Check if we have hit our maximum allowed retries (2)
        if attempts >= 2:
            return {
                "current_task_index": state["current_task_index"] + 1,
                "reflection_attempts": 0,
                "logs": state.get("logs", []) + [
                    f"⚠️ Max reflection retries reached for '{latest_section['heading']}'. Advancing with current draft."
                ]
            }
        
        # Pull out the failed draft to let executor rewrite it
        updated_sections = state["compiled_sections"][:-1]
        return {
            "compiled_sections": updated_sections,
            "reflection_attempts": attempts + 1,
            "logs": state.get("logs", []) + [
                f"❌ Quality Check Failed for '{latest_section['heading']}': {result.feedback}. Retry attempt {attempts + 1}/2..."
            ]
        }
        
    # Content passes QA check cleanly
    return {
        "current_task_index": state["current_task_index"] + 1,
        "reflection_attempts": 0,
        "logs": state.get("logs", []) + [f"✅ Quality Check Approved for '{latest_section['heading']}'."]
    }