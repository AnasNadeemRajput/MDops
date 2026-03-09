CRITICAL_SYMPTOMS = {
    "chest pain": "cardiac_emergency",
    "shortness of breath": "respiratory_emergency",
    "severe bleeding": "trauma_emergency",
    "fainting": "neurological_emergency",
    "confusion": "neurological_emergency"
}


MODERATE_SYMPTOMS = {
    "fever": "possible infection",
    "vomiting": "gastro issue",
    "headache": "neurological monitoring"
}


def evaluate_symptoms(symptoms):

    symptoms = symptoms.lower()

    for s in CRITICAL_SYMPTOMS:

        if s in symptoms:
            return {
                "severity": "critical",
                "condition": CRITICAL_SYMPTOMS[s]
            }

    for s in MODERATE_SYMPTOMS:

        if s in symptoms:
            return {
                "severity": "moderate",
                "condition": MODERATE_SYMPTOMS[s]
            }

    return {
        "severity": "low",
        "condition": "monitor"
    }