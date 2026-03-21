"""
Generate synthetic patient database for Trinidad & Tobago Population Health Analytics.

Reflects real epidemiological patterns:
- High diabetes prevalence (~13%)
- Hypertension (~30% of adults)
- Cardiovascular disease as leading cause of death
- Significant obesity rates
- Sickle cell trait in Afro-Caribbean population
- HIV prevalence
- Asthma/COPD from environmental factors
"""

import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)

# Trinidad & Tobago demographics
REGIONS = [
    "Port of Spain", "San Fernando", "Chaguanas", "Arima", "Point Fortin",
    "Scarborough (Tobago)", "Siparia", "Princes Town", "Couva", "Sangre Grande",
    "Tunapuna", "Diego Martin", "Penal", "Rio Claro", "Fyzabad"
]

ETHNICITIES = {
    "Indo-Trinidadian": 0.35,
    "Afro-Trinidadian": 0.34,
    "Mixed": 0.23,
    "Other": 0.08,
}

# Conditions with base probabilities (adjusted per age/ethnicity)
CONDITIONS = {
    "Type 2 Diabetes": {
        "base_prob": 0.13,
        "medications": [
            ("Metformin 500mg", 0.45), ("Metformin 1000mg", 0.20),
            ("Glimepiride 2mg", 0.15), ("Insulin Glargine", 0.12),
            ("Sitagliptin 100mg", 0.05), ("Empagliflozin 25mg", 0.03),
        ],
        "severity": ["Controlled", "Moderately Controlled", "Uncontrolled"],
        "severity_weights": [0.4, 0.35, 0.25],
    },
    "Hypertension": {
        "base_prob": 0.30,
        "medications": [
            ("Amlodipine 5mg", 0.25), ("Amlodipine 10mg", 0.15),
            ("Lisinopril 10mg", 0.20), ("Losartan 50mg", 0.15),
            ("Hydrochlorothiazide 25mg", 0.12), ("Atenolol 50mg", 0.08),
            ("Nifedipine 30mg", 0.05),
        ],
        "severity": ["Stage 1", "Stage 2", "Hypertensive Crisis"],
        "severity_weights": [0.50, 0.38, 0.12],
    },
    "Cardiovascular Disease": {
        "base_prob": 0.08,
        "medications": [
            ("Aspirin 81mg", 0.30), ("Atorvastatin 20mg", 0.25),
            ("Clopidogrel 75mg", 0.15), ("Rosuvastatin 10mg", 0.12),
            ("Warfarin 5mg", 0.10), ("Metoprolol 50mg", 0.08),
        ],
        "severity": ["Stable", "Moderate", "Severe"],
        "severity_weights": [0.45, 0.35, 0.20],
    },
    "Obesity": {
        "base_prob": 0.18,
        "medications": [
            ("Orlistat 120mg", 0.30), ("Lifestyle Modification Only", 0.50),
            ("Phentermine 37.5mg", 0.10), ("Liraglutide 3mg", 0.10),
        ],
        "severity": ["Class I (BMI 30-34.9)", "Class II (BMI 35-39.9)", "Class III (BMI 40+)"],
        "severity_weights": [0.50, 0.30, 0.20],
    },
    "Asthma / COPD": {
        "base_prob": 0.10,
        "medications": [
            ("Salbutamol Inhaler", 0.35), ("Fluticasone Inhaler", 0.25),
            ("Montelukast 10mg", 0.15), ("Ipratropium Inhaler", 0.10),
            ("Budesonide/Formoterol", 0.10), ("Prednisolone 5mg", 0.05),
        ],
        "severity": ["Mild Intermittent", "Mild Persistent", "Moderate Persistent", "Severe"],
        "severity_weights": [0.30, 0.30, 0.25, 0.15],
    },
    "Chronic Kidney Disease": {
        "base_prob": 0.05,
        "medications": [
            ("Erythropoietin", 0.20), ("Calcium Carbonate 500mg", 0.25),
            ("Furosemide 40mg", 0.20), ("Sodium Bicarbonate", 0.15),
            ("Iron Supplement", 0.20),
        ],
        "severity": ["Stage 1-2", "Stage 3", "Stage 4-5"],
        "severity_weights": [0.35, 0.40, 0.25],
    },
    "HIV/AIDS": {
        "base_prob": 0.015,
        "medications": [
            ("Tenofovir/Emtricitabine", 0.35), ("Dolutegravir 50mg", 0.30),
            ("Efavirenz 600mg", 0.15), ("Atazanavir/Ritonavir", 0.10),
            ("Lamivudine/Zidovudine", 0.10),
        ],
        "severity": ["Well Controlled (Undetectable)", "Controlled", "Advanced"],
        "severity_weights": [0.50, 0.35, 0.15],
    },
    "Cancer": {
        "base_prob": 0.04,
        "medications": [
            ("Chemotherapy Regimen", 0.30), ("Tamoxifen 20mg", 0.15),
            ("Letrozole 2.5mg", 0.10), ("Bicalutamide 50mg", 0.10),
            ("Palliative Care", 0.15), ("Surgical Management", 0.20),
        ],
        "severity": ["Stage I", "Stage II", "Stage III", "Stage IV"],
        "severity_weights": [0.25, 0.30, 0.25, 0.20],
        "subtypes": ["Prostate", "Breast", "Colorectal", "Cervical", "Lung", "Lymphoma"],
    },
    "Depression / Anxiety": {
        "base_prob": 0.12,
        "medications": [
            ("Sertraline 50mg", 0.25), ("Fluoxetine 20mg", 0.20),
            ("Amitriptyline 25mg", 0.15), ("Escitalopram 10mg", 0.15),
            ("Diazepam 5mg", 0.10), ("Counseling/Therapy Only", 0.15),
        ],
        "severity": ["Mild", "Moderate", "Severe"],
        "severity_weights": [0.35, 0.40, 0.25],
    },
    "Sickle Cell Disease": {
        "base_prob": 0.02,
        "medications": [
            ("Hydroxyurea 500mg", 0.35), ("Folic Acid 5mg", 0.30),
            ("Penicillin V 250mg", 0.15), ("Pain Management", 0.20),
        ],
        "severity": ["Mild (Trait)", "Moderate", "Severe"],
        "severity_weights": [0.40, 0.35, 0.25],
    },
}

TT_FIRST_NAMES_MALE = [
    "Avinash", "Brian", "Curtis", "Dwayne", "Emile", "Farouk", "Gregory",
    "Hamid", "Isaiah", "Jason", "Kevon", "Lester", "Marcus", "Navin",
    "Omar", "Prakash", "Quincy", "Ravi", "Shawn", "Tyrone", "Vijay",
    "Wayne", "Xavier", "Yusuf", "Zahir", "Andre", "Darren", "Keron",
    "Rishi", "Stefan",
]

TT_FIRST_NAMES_FEMALE = [
    "Alicia", "Brinda", "Camille", "Devika", "Esther", "Farzana", "Giselle",
    "Hema", "Indira", "Janelle", "Kamla", "Latoya", "Meera", "Nalini",
    "Odette", "Priya", "Queenie", "Reshma", "Simone", "Tricia", "Uma",
    "Vanessa", "Wendy", "Xena", "Yashoda", "Zara", "Asha", "Donna",
    "Kavita", "Sharon",
]

TT_LAST_NAMES = [
    "Mohammed", "Singh", "Williams", "Ramnath", "Joseph", "Ali", "Charles",
    "Doodnath", "Edwards", "Fraser", "Garcia", "Hosein", "Isaac", "James",
    "Khan", "Lewis", "Maharaj", "Narine", "Ottley", "Persad", "Ramkissoon",
    "Sookdeo", "Thomas", "Udecott", "Valentine", "Warner", "Young",
    "Boodoo", "De Silva", "Gonzales",
]


def pick_ethnicity():
    r = random.random()
    cumulative = 0
    for eth, prob in ETHNICITIES.items():
        cumulative += prob
        if r <= cumulative:
            return eth
    return "Other"


def adjust_probability(base_prob, age, ethnicity, condition_name):
    """Adjust condition probability based on age and ethnicity."""
    prob = base_prob

    # Age adjustments
    if condition_name in ("Type 2 Diabetes", "Hypertension", "Cardiovascular Disease", "Chronic Kidney Disease"):
        if age > 60:
            prob *= 2.0
        elif age > 45:
            prob *= 1.5
        elif age < 30:
            prob *= 0.2

    if condition_name == "Obesity":
        if 30 <= age <= 55:
            prob *= 1.4

    if condition_name == "Cancer":
        if age > 55:
            prob *= 2.5
        elif age < 35:
            prob *= 0.15

    # Ethnicity adjustments (based on known epidemiological data for T&T)
    if condition_name == "Type 2 Diabetes" and ethnicity == "Indo-Trinidadian":
        prob *= 1.4
    if condition_name == "Hypertension" and ethnicity == "Afro-Trinidadian":
        prob *= 1.3
    if condition_name == "Sickle Cell Disease" and ethnicity == "Afro-Trinidadian":
        prob *= 3.0
    if condition_name == "Sickle Cell Disease" and ethnicity == "Indo-Trinidadian":
        prob *= 0.1

    return min(prob, 0.85)


def generate_patient(patient_id):
    gender = random.choice(["Male", "Female"])
    ethnicity = pick_ethnicity()
    age = random.randint(18, 85)
    dob = datetime.now() - timedelta(days=age * 365 + random.randint(0, 364))

    if gender == "Male":
        first_name = random.choice(TT_FIRST_NAMES_MALE)
    else:
        first_name = random.choice(TT_FIRST_NAMES_FEMALE)
    last_name = random.choice(TT_LAST_NAMES)

    region = random.choice(REGIONS)

    # Determine conditions
    patient_conditions = []
    patient_medications = []

    for cond_name, cond_data in CONDITIONS.items():
        prob = adjust_probability(cond_data["base_prob"], age, ethnicity, cond_name)
        if random.random() < prob:
            severity = random.choices(cond_data["severity"], weights=cond_data["severity_weights"])[0]

            # Pick 1-2 medications for this condition
            med_names = [m[0] for m in cond_data["medications"]]
            med_weights = [m[1] for m in cond_data["medications"]]
            num_meds = random.choices([1, 2], weights=[0.65, 0.35])[0]
            chosen_meds = random.choices(med_names, weights=med_weights, k=num_meds)
            chosen_meds = list(set(chosen_meds))

            entry = {
                "condition": cond_name,
                "severity": severity,
                "diagnosed_date": (datetime.now() - timedelta(days=random.randint(30, age * 200))).strftime("%Y-%m-%d"),
            }
            if cond_name == "Cancer":
                entry["subtype"] = random.choice(cond_data["subtypes"])

            patient_conditions.append(entry)
            for med in chosen_meds:
                patient_medications.append({
                    "medication": med,
                    "for_condition": cond_name,
                    "frequency": random.choice(["Once daily", "Twice daily", "As needed", "Weekly"]),
                    "adherence": random.choices(
                        ["Good", "Moderate", "Poor"],
                        weights=[0.50, 0.30, 0.20]
                    )[0],
                })

    # Generate vitals
    bmi = round(random.gauss(27.5, 5.5), 1)
    bmi = max(18.0, min(bmi, 48.0))

    if any(c["condition"] == "Hypertension" for c in patient_conditions):
        systolic = random.randint(135, 180)
        diastolic = random.randint(85, 110)
    else:
        systolic = random.randint(110, 135)
        diastolic = random.randint(65, 85)

    if any(c["condition"] == "Type 2 Diabetes" for c in patient_conditions):
        hba1c = round(random.uniform(6.5, 12.0), 1)
        fasting_glucose = round(random.uniform(126, 300), 0)
    else:
        hba1c = round(random.uniform(4.5, 6.4), 1)
        fasting_glucose = round(random.uniform(70, 125), 0)

    last_visit = datetime.now() - timedelta(days=random.randint(1, 180))
    insurance = random.choices(
        ["Public (CDAP)", "Private Insurance", "Out-of-Pocket", "NHIS"],
        weights=[0.40, 0.25, 0.15, 0.20]
    )[0]

    return {
        "patient_id": f"TT-{patient_id:04d}",
        "first_name": first_name,
        "last_name": last_name,
        "gender": gender,
        "age": age,
        "date_of_birth": dob.strftime("%Y-%m-%d"),
        "ethnicity": ethnicity,
        "region": region,
        "insurance": insurance,
        "bmi": bmi,
        "blood_pressure": f"{systolic}/{diastolic}",
        "systolic": systolic,
        "diastolic": diastolic,
        "hba1c": hba1c,
        "fasting_glucose": fasting_glucose,
        "smoker": random.choices([True, False], weights=[0.15, 0.85])[0],
        "alcohol_use": random.choices(["None", "Social", "Moderate", "Heavy"], weights=[0.40, 0.30, 0.20, 0.10])[0],
        "exercise_frequency": random.choices(
            ["Sedentary", "1-2x/week", "3-4x/week", "5+/week"],
            weights=[0.35, 0.30, 0.20, 0.15]
        )[0],
        "conditions": patient_conditions,
        "medications": patient_medications,
        "last_visit": last_visit.strftime("%Y-%m-%d"),
        "risk_score": 0,  # calculated below
    }


def calculate_risk_score(patient):
    """Composite health risk score 0-100."""
    score = 0
    score += len(patient["conditions"]) * 10
    score += max(0, (patient["age"] - 40)) * 0.5
    if patient["bmi"] > 30:
        score += 10
    if patient["bmi"] > 35:
        score += 5
    if patient["systolic"] > 140:
        score += 10
    if patient["hba1c"] > 7.0:
        score += 10
    if patient["smoker"]:
        score += 8
    if patient["alcohol_use"] == "Heavy":
        score += 5
    if patient["exercise_frequency"] == "Sedentary":
        score += 5

    for c in patient["conditions"]:
        sev = c["severity"]
        if "Severe" in sev or "Uncontrolled" in sev or "Crisis" in sev or "Stage 4" in sev or "Stage III" in sev or "Stage IV" in sev:
            score += 12
        elif "Moderate" in sev or "Stage 2" in sev or "Stage II" in sev or "Stage 3" in sev:
            score += 6

    for m in patient["medications"]:
        if m["adherence"] == "Poor":
            score += 5

    return min(round(score), 100)


def main():
    patients = []
    for i in range(1, 151):
        p = generate_patient(i)
        p["risk_score"] = calculate_risk_score(p)
        patients.append(p)

    with open("data/patients.json", "w") as f:
        json.dump(patients, f, indent=2)

    # Print summary
    total_conditions = {}
    total_medications = {}
    for p in patients:
        for c in p["conditions"]:
            total_conditions[c["condition"]] = total_conditions.get(c["condition"], 0) + 1
        for m in p["medications"]:
            total_medications[m["medication"]] = total_medications.get(m["medication"], 0) + 1

    print(f"Generated {len(patients)} patients")
    print(f"\nCondition prevalence:")
    for cond, count in sorted(total_conditions.items(), key=lambda x: -x[1]):
        print(f"  {cond}: {count} ({count/len(patients)*100:.1f}%)")

    print(f"\nTop 15 medications:")
    for med, count in sorted(total_medications.items(), key=lambda x: -x[1])[:15]:
        print(f"  {med}: {count}")

    avg_risk = sum(p["risk_score"] for p in patients) / len(patients)
    print(f"\nAverage risk score: {avg_risk:.1f}/100")
    print(f"High risk (>60): {sum(1 for p in patients if p['risk_score'] > 60)}")
    print(f"Medium risk (30-60): {sum(1 for p in patients if 30 <= p['risk_score'] <= 60)}")
    print(f"Low risk (<30): {sum(1 for p in patients if p['risk_score'] < 30)}")


if __name__ == "__main__":
    main()
