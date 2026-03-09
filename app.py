from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import LoginRequest, ChatOrSymptomRequest
from agent import agent_login, agent_chat, agent_health_monitor
from graph import graph
import uvicorn

app = FastAPI(
    title="Medicalops",
    version="1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
)


# ------------------------------------
# Login endpoint
# ------------------------------------
@app.post("/login")
def login(request: LoginRequest):
    patient = agent_login(request.mrn)
    if not patient:
        return {"status": "error", "message": "Invalid MRN"}
    return {"status": "success", "patient_name": patient["name"]}


@app.post("/chat")
def chat(request: ChatOrSymptomRequest):

    result = graph.invoke({
        "mrn": request.mrn,
        "query": request.query,
        "symptoms": request.symptoms
    })

    return {
        "alert": result.get("alert", False),
        "response": result.get("response")
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)