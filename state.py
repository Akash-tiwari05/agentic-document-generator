from typing import List, Dict, Any
from typing_extensions import TypedDict
from schemas import Task, ExecutionPlan

class AgentState(TypedDict):
    user_request: str
    plan: ExecutionPlan
    current_task_index: int
    tasks_to_execute: List[Task]
    compiled_sections: List[Dict[str, Any]]
    logs: List[str]
    final_docx_path: str
    # FIX: Bounded reflection tracker
    reflection_attempts: int