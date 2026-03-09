from database import get_patient_by_mrn
from utils.sessionmemory import create_session, get_session, add_chat, get_vector_store
from utils.triage import evaluate_symptoms
from services.llm import generate_response


# --------------------------------
# Agent 1
# Patient Login + Data Loader
# --------------------------------

def agent_login(mrn):

    patient = get_patient_by_mrn(mrn)

    if not patient:
        return None

    create_session(mrn, patient)

    vector_store = get_vector_store(mrn)

    discharge = patient["discharge_summary"]
    meds = patient["medications"]
    instructions = patient["instructions"]

    context = f"""
Discharge Summary:
{discharge}

Medications:
{meds}

Instructions:
{instructions}
"""

    vector_store.add_document(context)

    return patient


# --------------------------------
# Agent 2
# RAG Chat Agent
# --------------------------------

def agent_chat(mrn, query):

    session = get_session(mrn)

    if not session:
        return "User not logged in."

    vector_store = get_vector_store(mrn)

    docs = vector_store.search(query)

    context = "\n".join(docs)

    prompt = f"""
You are a clinical assistant chatbot.

Use ONLY the patient's medical information.

Patient Data:
{context}

Patient Question:
{query}

If the question is unrelated to patient health data,
say you cannot answer.
"""

    response = generate_response(prompt)

    add_chat(mrn, query, response)

    return response


# --------------------------------
# Agent 3
# Symptom Monitoring Agent
# --------------------------------

def agent_health_monitor(mrn, symptoms):

    session = get_session(mrn)

    if not session:
        return {"error": "Not logged in"}

    patient = session["patient"]

    triage = evaluate_symptoms(symptoms)

    if triage["severity"] == "critical":

        return {
            "alert": True,
            "severity": "critical",
            "message": f"""
⚠️ CRITICAL SYMPTOMS DETECTED

Possible Condition:
{triage["condition"]}

Please contact emergency services immediately.

Emergency Contact:
{patient["emergency_contact"]}
"""
        }

    if triage["severity"] == "moderate":

        return {
            "alert": False,
            "severity": "moderate",
            "message": f"""
Symptoms indicate:
{triage["condition"]}

Monitor symptoms and consult your doctor if worsening.
"""
        }

    return {
        "alert": False,
        "severity": "low",
        "message": "Symptoms recorded. Continue monitoring."
    }