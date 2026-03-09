import psycopg2

DB_CONFIG = {
    "database": "medicalops",
    "user": "postgres",
    "password": "Musabnadeem_12",
    "host": "localhost",
    "port": "5432"
}

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
tables = cur.fetchall()

print("Tables in the database:")
for t in tables:
    print(t[0])

cur.close()
conn.close()