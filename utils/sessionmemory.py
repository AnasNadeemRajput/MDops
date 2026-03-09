from services.rag import PatientVectorStore

sessions = {}


def create_session(mrn, patient):

    sessions[mrn] = {
        "patient": patient,
        "chat_history": [],
        "vector_store": PatientVectorStore()
    }


def get_session(mrn):

    return sessions.get(mrn)


def add_chat(mrn, q, a):

    session = sessions[mrn]

    session["chat_history"].append({
        "question": q,
        "answer": a
    })


def get_vector_store(mrn):

    return sessions[mrn]["vector_store"]