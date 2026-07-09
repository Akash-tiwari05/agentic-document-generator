from langgraph.graph import StateGraph, START, END
from state import AgentState
from planner import planning_node
from executor import executor_node
from reflection import reflection_node
from doc_generator import document_generator_node

def route_next_task(state: AgentState) -> str:
    # Check if the execution list has been exhausted
    if state["current_task_index"] < len(state["tasks_to_execute"]):
        return "executor"
    return "generator"

# Initialize graph instance
workflow = StateGraph(AgentState)

# Append operational nodes
workflow.add_node("planner", planning_node)
workflow.add_node("executor", executor_node)
workflow.add_node("reflection", reflection_node)
workflow.add_node("generator", document_generator_node)

# Define static entry and path flows
workflow.add_edge(START, "planner")
workflow.add_edge("planner", "executor")
workflow.add_edge("executor", "reflection")

# Define conditional execution looping path
workflow.add_conditional_edges(
    "reflection",
    route_next_task,
    {
        "executor": "executor",
        "generator": "generator"
    }
)

workflow.add_edge("generator", END)

# Compile ready for invoke calls
agent_graph = workflow.compile()