"""
Load patient data into Railway PostgreSQL database.
Creates tables: patients, conditions, medications
"""

import json
import psycopg2
from psycopg2.extras import execute_values

DATABASE_URL = "postgresql://postgres:CKUsFFxHuncuINbfZVHyQojwKGefollG@centerbeam.proxy.rlwy.net:18737/railway"

def main():
    with open("data/patients.json") as f:
        patients = json.load(f)

    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()

    # Create schema
    cur.execute("""
        DROP TABLE IF EXISTS medications CASCADE;
        DROP TABLE IF EXISTS conditions CASCADE;
        DROP TABLE IF EXISTS patients CASCADE;

        CREATE TABLE patients (
            patient_id VARCHAR(10) PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            gender VARCHAR(10),
            age INTEGER,
            date_of_birth DATE,
            ethnicity VARCHAR(30),
            region VARCHAR(50),
            insurance VARCHAR(30),
            bmi DECIMAL(4,1),
            systolic INTEGER,
            diastolic INTEGER,
            blood_pressure VARCHAR(10),
            hba1c DECIMAL(4,1),
            fasting_glucose DECIMAL(5,0),
            smoker BOOLEAN,
            alcohol_use VARCHAR(20),
            exercise_frequency VARCHAR(20),
            last_visit DATE,
            risk_score INTEGER,
            num_conditions INTEGER,
            num_medications INTEGER
        );

        CREATE TABLE conditions (
            id SERIAL PRIMARY KEY,
            patient_id VARCHAR(10) REFERENCES patients(patient_id),
            condition VARCHAR(50),
            severity VARCHAR(50),
            diagnosed_date DATE,
            subtype VARCHAR(30)
        );

        CREATE TABLE medications (
            id SERIAL PRIMARY KEY,
            patient_id VARCHAR(10) REFERENCES patients(patient_id),
            medication VARCHAR(50),
            for_condition VARCHAR(50),
            frequency VARCHAR(20),
            adherence VARCHAR(10)
        );
    """)

    # Insert patients
    patient_rows = []
    for p in patients:
        patient_rows.append((
            p["patient_id"], p["first_name"], p["last_name"], p["gender"],
            p["age"], p["date_of_birth"], p["ethnicity"], p["region"],
            p["insurance"], p["bmi"], p["systolic"], p["diastolic"],
            p["blood_pressure"], p["hba1c"], p["fasting_glucose"],
            p["smoker"], p["alcohol_use"], p["exercise_frequency"],
            p["last_visit"], p["risk_score"],
            len(p["conditions"]), len(p["medications"]),
        ))

    execute_values(cur, """
        INSERT INTO patients (
            patient_id, first_name, last_name, gender, age, date_of_birth,
            ethnicity, region, insurance, bmi, systolic, diastolic,
            blood_pressure, hba1c, fasting_glucose, smoker, alcohol_use,
            exercise_frequency, last_visit, risk_score, num_conditions, num_medications
        ) VALUES %s
    """, patient_rows)
    print(f"Inserted {len(patient_rows)} patients")

    # Insert conditions
    cond_rows = []
    for p in patients:
        for c in p["conditions"]:
            cond_rows.append((
                p["patient_id"], c["condition"], c["severity"],
                c["diagnosed_date"], c.get("subtype"),
            ))

    if cond_rows:
        execute_values(cur, """
            INSERT INTO conditions (patient_id, condition, severity, diagnosed_date, subtype)
            VALUES %s
        """, cond_rows)
    print(f"Inserted {len(cond_rows)} condition records")

    # Insert medications
    med_rows = []
    for p in patients:
        for m in p["medications"]:
            med_rows.append((
                p["patient_id"], m["medication"], m["for_condition"],
                m["frequency"], m["adherence"],
            ))

    if med_rows:
        execute_values(cur, """
            INSERT INTO medications (patient_id, medication, for_condition, frequency, adherence)
            VALUES %s
        """, med_rows)
    print(f"Inserted {len(med_rows)} medication records")

    # Verify
    cur.execute("SELECT COUNT(*) FROM patients")
    print(f"\nVerification - Patients: {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM conditions")
    print(f"Verification - Conditions: {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM medications")
    print(f"Verification - Medications: {cur.fetchone()[0]}")

    cur.close()
    conn.close()
    print("\nDatabase loaded successfully!")


if __name__ == "__main__":
    main()
