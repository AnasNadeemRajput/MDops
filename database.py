import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "database": "medicalops",
    "user": "postgres",
    "password": "Musabnadeem_12",
    "host": "localhost",
    "port": "5432"
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def get_patient_by_mrn(mrn):

    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    query = """
    SELECT p.id,
           p.name,
           p.mrn,
           p.age,
           p.emergency_contact,
           m.discharge_summary,
           m.medications,
           m.instructions
    FROM patients p
    JOIN medical_records m
    ON p.id = m.patient_id
    WHERE p.mrn = %s
    """

    cursor.execute(query, (mrn,))
    patient = cursor.fetchone()

    cursor.close()
    conn.close()

    return patient