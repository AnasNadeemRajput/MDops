import psycopg2

DB_CONFIG = {
    "database": "medicalops",
    "user": "postgres",
    "password": "Musabnadeem_12",
    "host": "localhost",
    "port": "5432"
}

CREATE_PATIENTS_TABLE = """
CREATE TABLE IF NOT EXISTS patients (
    id                SERIAL PRIMARY KEY,
    name              VARCHAR(150)  NOT NULL,
    mrn               VARCHAR(50)   UNIQUE NOT NULL,
    age               INTEGER       CHECK (age >= 0 AND age <= 150),
    emergency_contact VARCHAR(200)
);
"""

CREATE_MEDICAL_RECORDS_TABLE = """
CREATE TABLE IF NOT EXISTS medical_records (
    id                SERIAL PRIMARY KEY,
    patient_id        INTEGER   NOT NULL,
    discharge_summary TEXT,
    medications       TEXT,
    instructions      TEXT,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients (id)
        ON DELETE CASCADE
);
"""

CREATE_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_patients_mrn ON patients (mrn);",
    "CREATE INDEX IF NOT EXISTS idx_medical_records_patient_id ON medical_records (patient_id);"
]


def create_database():
    try:
        print("Connecting to PostgreSQL...")
        conn = psycopg2.connect(
            database="postgres",
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'medicalops'")
        if not cursor.fetchone():
            cursor.execute("CREATE DATABASE medicalops")
            print("✅ Database 'medicalops' created!")
        else:
            print("ℹ️  Database 'medicalops' already exists.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Failed to create database: {e}")
        exit(1)


def create_tables():
    try:
        print("Connecting to 'medicalops' database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        print("Creating 'patients' table...")
        cursor.execute(CREATE_PATIENTS_TABLE)

        print("Creating 'medical_records' table...")
        cursor.execute(CREATE_MEDICAL_RECORDS_TABLE)

        print("Creating indexes...")
        for index_sql in CREATE_INDEXES:
            cursor.execute(index_sql)

        conn.commit()
        print("\n✅ All tables and indexes created successfully!")

    except Exception as e:
        print(f"\n❌ Error creating tables: {e}")
        if conn:
            conn.rollback()

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    create_database()
    create_tables()
