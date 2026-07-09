import time
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from dotenv import load_dotenv
from state import AgentState
from schemas import SectionContent
from prompts import EXECUTOR_PROMPT

load_dotenv()
client = genai.Client()

# MANDATORY IMPROVEMENT: Exponential Backoff & Retry Logic for 429 errors
@retry(
    stop=stop_after_attempt(5),
    # If hit by a 429, wait 5s, then 10s, then 20s... up to 60s max
    wait=wait_exponential(multiplier=2, min=5, max=60),
    retry=retry_if_exception_type(ClientError),
    reraise=True
)
def call_gemini_executor(prompt):
    """Executes the LLM generation with a rate-limiting safety net."""
    # Preemptive pacing delay: sleep 4 seconds before every single call 
    # to naturally smooth out Gemini's strict 5 RPM ceiling.
    time.sleep(4)
    
    return client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=SectionContent,
            temperature=0.7,
        ),
    )

def executor_node(state: AgentState) -> dict:
    idx = state["current_task_index"]
    current_task = state["tasks_to_execute"][idx]
    
    prev_context = ""
    for sec in state.get("compiled_sections", []):
        prev_context += f"### {sec['heading']}\n" + "\n".join(sec['paragraphs']) + "\n\n"
        
    prompt = EXECUTOR_PROMPT.format(
        user_request=state["user_request"],
        task_title=current_task.title,
        task_description=current_task.description,
        previous_context=prev_context if prev_context else "None (First section)"
    )
    
    # Use our new retry wrapper instead of raw 'client.models.generate_content'
    response = call_gemini_executor(prompt)
    
    content = SectionContent.model_validate_json(response.text)
    
    current_sections = list(state.get("compiled_sections", []))
    current_sections.append({"heading": content.heading, "paragraphs": content.paragraphs})
    
    return {
        "compiled_sections": current_sections,
        "logs": state.get("logs", []) + [f"Drafted section: {content.heading}"]
    }