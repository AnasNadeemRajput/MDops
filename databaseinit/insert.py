import psycopg2

DB_CONFIG = {
    "database": "medicalops",
    "user": "postgres",
    "password": "Musabnadeem_12",
    "host": "localhost",
    "port": "5432"
}

# Sample patients data with 8-digit MRNs
patients_data = [
    ("John Smith", "10000001", 45, "Jane Smith - 555-1234"),
    ("Alice Johnson", "10000002", 30, "Mark Johnson - 555-5678"),
    ("David Brown", "10000003", 60, "Emily Brown - 555-8765"),
    ("Mary Davis", "10000004", 25, "Paul Davis - 555-4321")
]

# Sample medical records (patient_id must match inserted IDs)
medical_records_data = [
    (1, "Admitted for chest pain, discharged stable.", "Aspirin, Atorvastatin", "Follow up in 2 weeks"),
    (2, "Mild pneumonia treated with antibiotics.", "Azithromycin", "Complete medication course"),
    (3, "Hypertension monitoring.", "Lisinopril", "Daily BP monitoring"),
    (4, "Minor surgery, no complications.", "Paracetamol", "Rest for 1 week")
]

def insert_data():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Insert patients
        print("Inserting patients...")
        patient_insert_query = """
        INSERT INTO patients (name, mrn, age, emergency_contact)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (mrn) DO NOTHING
        RETURNING id;
        """
        patient_ids = []
        for patient in patients_data:
            cursor.execute(patient_insert_query, patient)
            result = cursor.fetchone()
            if result:
                patient_ids.append(result[0])

        print("Patients inserted.")

        # Insert medical records
        print("Inserting medical records...")
        medical_insert_query = """
        INSERT INTO medical_records (patient_id, discharge_summary, medications, instructions)
        VALUES (%s, %s, %s, %s);
        """

        for record in medical_records_data:
            cursor.execute(medical_insert_query, record)

        conn.commit()
        print("Medical records inserted successfully!")

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    insert_data()