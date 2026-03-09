from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from agent import agent_chat, agent_health_monitor

# ---------------------------
# Graph State
# ---------------------------

class GraphState(TypedDict):

    mrn: str
    query: Optional[str]
    symptoms: Optional[str]
    response: Optional[str]
    alert: Optional[bool]


# ---------------------------
# Chat Node
# ---------------------------

def chat_node(state: GraphState):

    response = agent_chat(state["mrn"], state["query"])

    return {
        "response": response,
        "alert": False
    }


# ---------------------------
# Symptom Node
# ---------------------------

def symptom_node(state: GraphState):

    result = agent_health_monitor(state["mrn"], state["symptoms"])

    return {
        "response": result.get("message"),
        "alert": result.get("alert")
    }


# ---------------------------
# Router
# ---------------------------

def router(state: GraphState):

    if state.get("symptoms"):
        return "symptom"

    return "chat"


# ---------------------------
# Build Graph
# ---------------------------

builder = StateGraph(GraphState)

builder.add_node("chat", chat_node)
builder.add_node("symptom", symptom_node)

builder.set_conditional_entry_point(
    router,
    {
        "chat": "chat",
        "symptom": "symptom"
    }
)

builder.add_edge("chat", END)
builder.add_edge("symptom", END)

graph = builder.compile()