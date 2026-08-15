"""
Generate synthetic patient databases for multi-country Population Health Analytics.

Country-agnostic engine: for every country in countries.REGISTRY it produces
RECORDS_PER_COUNTRY synthetic patients using that country's regions, curated
names, ethnicity mix, insurance/payer system, age structure and a curated,
prevalence-tuned condition list. Medications and severity bands come from the
shared CONDITION_LIBRARY in countries/base.py.

Output: data/patients.json  (a flat list across all countries; each record
carries a `country` code field).
"""

import json
import random
from datetime import datetime, timedelta

from countries import REGISTRY
from countries.base import CONDITION_LIBRARY, age_multiplier, age_group

RECORDS_PER_COUNTRY = 1000
random.seed(42)


def pick_weighted(pairs):
    """pairs: list of (value, weight). Returns a value."""
    values = [v for v, _ in pairs]
    weights = [w for _, w in pairs]
    return random.choices(values, weights=weights)[0]


def pick_from_dict(prob_dict):
    """prob_dict: {value: probability}. Returns a value."""
    return random.choices(list(prob_dict.keys()), weights=list(prob_dict.values()))[0]


def sample_age(age_brackets):
    (lo, hi) = pick_weighted(age_brackets)
    return random.randint(lo, hi)


def adjust_probability(base_prob, age, ethnicity, condition_name, cond_cfg):
    """Combine generic age effect with country-supplied ethnicity adjustment."""
    category = CONDITION_LIBRARY[condition_name]["category"]
    prob = base_prob * age_multiplier(category, age)

    eth_adjust = cond_cfg.get("ethnicity_adjust", {})
    if ethnicity in eth_adjust:
        prob *= eth_adjust[ethnicity]

    return min(prob, 0.85)


def generate_patient(cfg, seq):
    code = cfg["code"]
    gender = random.choice(["Male", "Female"])
    ethnicity = pick_from_dict(cfg["ethnicities"])
    age = sample_age(cfg["age_brackets"])
    dob = datetime.now() - timedelta(days=age * 365 + random.randint(0, 364))

    if gender == "Male":
        first_name = random.choice(cfg["first_names_male"])
    else:
        first_name = random.choice(cfg["first_names_female"])
    last_name = random.choice(cfg["last_names"])
    region = random.choice(cfg["regions"])

    # Determine conditions from the country's curated condition list
    patient_conditions = []
    patient_medications = []

    for cond_name, cond_cfg in cfg["conditions"].items():
        lib = CONDITION_LIBRARY[cond_name]
        prob = adjust_probability(cond_cfg["base_prob"], age, ethnicity, cond_name, cond_cfg)
        if random.random() < prob:
            severity = random.choices(lib["severity"], weights=lib["severity_weights"])[0]

            med_names = [m[0] for m in lib["medications"]]
            med_weights = [m[1] for m in lib["medications"]]
            num_meds = random.choices([1, 2], weights=[0.65, 0.35])[0]
            chosen_meds = list(set(random.choices(med_names, weights=med_weights, k=num_meds)))

            entry = {
                "condition": cond_name,
                "severity": severity,
                "diagnosed_date": (datetime.now() - timedelta(days=random.randint(30, age * 200))).strftime("%Y-%m-%d"),
            }
            if cond_name == "Cancer":
                entry["subtype"] = random.choice(lib["subtypes"])

            patient_conditions.append(entry)
            for med in chosen_meds:
                patient_medications.append({
                    "medication": med,
                    "for_condition": cond_name,
                    "frequency": random.choice(["Once daily", "Twice daily", "As needed", "Weekly"]),
                    "adherence": random.choices(
                        ["Good", "Moderate", "Poor"], weights=[0.50, 0.30, 0.20]
                    )[0],
                })

    # Vitals
    bmi = round(max(18.0, min(random.gauss(27.5, 5.5), 48.0)), 1)

    if any(c["condition"] == "Hypertension" for c in patient_conditions):
        systolic, diastolic = random.randint(135, 180), random.randint(85, 110)
    else:
        systolic, diastolic = random.randint(110, 135), random.randint(65, 85)

    if any(c["condition"] == "Type 2 Diabetes" for c in patient_conditions):
        hba1c = round(random.uniform(6.5, 12.0), 1)
        fasting_glucose = round(random.uniform(126, 300), 0)
    else:
        hba1c = round(random.uniform(4.5, 6.4), 1)
        fasting_glucose = round(random.uniform(70, 125), 0)

    last_visit = datetime.now() - timedelta(days=random.randint(1, 180))
    insurance = pick_weighted(cfg["insurance"])

    return {
        "patient_id": f"{code}-{seq:04d}",
        "country": code,
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
            ["Sedentary", "1-2x/week", "3-4x/week", "5+/week"], weights=[0.35, 0.30, 0.20, 0.15]
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
        if any(k in sev for k in ("Severe", "Uncontrolled", "Crisis", "Stage 4", "Stage III", "Stage IV", "Advanced", "Cerebral", "Resistant")):
            score += 12
        elif any(k in sev for k in ("Moderate", "Stage 2", "Stage II", "Stage 3", "Active", "Chronic")):
            score += 6

    for m in patient["medications"]:
        if m["adherence"] == "Poor":
            score += 5

    return min(round(score), 100)


def main():
    all_patients = []
    per_country_summary = {}

    for code, cfg in REGISTRY.items():
        patients = []
        for i in range(1, RECORDS_PER_COUNTRY + 1):
            p = generate_patient(cfg, i)
            p["risk_score"] = calculate_risk_score(p)
            patients.append(p)
        all_patients.extend(patients)

        # summary
        cond_counts = {}
        for p in patients:
            for c in p["conditions"]:
                cond_counts[c["condition"]] = cond_counts.get(c["condition"], 0) + 1
        avg_risk = sum(p["risk_score"] for p in patients) / len(patients)
        per_country_summary[code] = (cfg["name"], cond_counts, avg_risk)

    with open("data/patients.json", "w") as f:
        json.dump(all_patients, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(all_patients)} patients across {len(REGISTRY)} countries "
          f"({RECORDS_PER_COUNTRY} each)\n")
    for code, (name, cond_counts, avg_risk) in per_country_summary.items():
        top = sorted(cond_counts.items(), key=lambda x: -x[1])[:5]
        top_str = ", ".join(f"{c} {n}" for c, n in top)
        print(f"  [{code}] {name}: avg risk {avg_risk:.1f} | top: {top_str}")


if __name__ == "__main__":
    main()
