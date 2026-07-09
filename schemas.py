# schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional

class Task(BaseModel):
    id: int = Field(..., description="Unique sequential identifier for the task.")
    title: str = Field(..., description="Clear title of the document section.")
    description: str = Field(..., description="Detailed instructions on what content must be generated.")

class ExecutionPlan(BaseModel):
    rationale: str = Field(..., description="Reasoning behind why this specific outline solves the user's requirements.")
    # Notice: Remove 'default=[]' from inside Field() to avoid Gemini schema generation conflicts
    assumptions: List[str] = Field(..., description="Assumptions made to resolve ambiguities or missing info. Leave empty if none.")
    tasks: List[Task] = Field(..., description="Ordered list of tasks/sections to build.")

class SectionContent(BaseModel):
    heading: str = Field(..., description="The definitive heading name for the Word doc.")
    paragraphs: List[str] = Field(..., description="Detailed paragraphs for this section.")

class ReflectionResult(BaseModel):
    approved: bool = Field(..., description="True if the section meets high quality standards, False otherwise.")
    feedback: Optional[str] = Field(None, description="Constructive feedback if the section requires rewrite.")