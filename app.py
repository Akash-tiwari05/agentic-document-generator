import os
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# 1. Load environment variables before importing modules that instantiate clients
load_dotenv()

from graph import agent_graph

app = FastAPI(title="Autonomous Multi-Step AI Agent")

class AgentRequest(BaseModel):
    request: str

class AgentResponse(BaseModel):
    rationale: str
    assumptions_made: list[str]
    execution_log: list[str]
    download_url: str

@app.post("/agent", response_model=AgentResponse)
async def process_request(payload: AgentRequest):
    # Initialize state dictionary cleanly
    # Inside app.py -> process_request endpoint initialization:
    initial_state = {
        "user_request": payload.request,
        "compiled_sections": [],
        "logs": [],
        "current_task_index": 0,
        "tasks_to_execute": [],
        "reflection_attempts": 0 # Initialize loop safety valve
    }
    
    try:
        # Run LangGraph State Machine
        final_state = agent_graph.invoke(initial_state)
        
        filename = os.path.basename(final_state["final_docx_path"])
        
        return AgentResponse(
            rationale=final_state["plan"].rationale,
            assumptions_made=final_state["plan"].assumptions,
            execution_log=final_state["logs"],
            download_url=f"/download/{filename}"
        )
    except Exception as e:
        # --- VERBOSE DEBUGGING INSIGHT PRINT ---
        print("\n❌ ===========================================")
        print("          AGENT EXECUTION CRASH TRACEBACK      ")
        print("=============================================\n")
        traceback.print_exc()
        print("\n❌ ===========================================\n")
        
        raise HTTPException(status_code=500, detail=f"Internal Graph Error: {str(e)}")

@app.get("/download/{filename}")
async def download_file(filename: str):
    filepath = os.path.join("./generated_docs", filename)
    if os.path.exists(filepath):
        return FileResponse(
            path=filepath, 
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
            filename=filename
        )
    raise HTTPException(status_code=404, detail="File not found.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)