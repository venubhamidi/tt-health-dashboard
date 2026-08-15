"""
Shared building blocks for the multi-country synthetic patient generator.

The CONDITION_LIBRARY is a superset of every condition modelled across all
countries. Medications, severity bands and (for cancer) subtypes are largely
universal, so they live here once. Each country config in this package then
*selects* a subset of these conditions and supplies its own prevalence
(base_prob) and ethnicity/age risk adjustments.

Nothing in this file is country-specific.
"""

# ---------------------------------------------------------------------------
# Condition library — medications + severity bands, keyed by condition name.
# `category` groups conditions so the engine can apply generic age effects.
# ---------------------------------------------------------------------------
CONDITION_LIBRARY = {
    # ---- Chronic / non-communicable ----
    "Type 2 Diabetes": {
        "category": "chronic_metabolic",
        "medications": [
            ("Metformin 500mg", 0.45), ("Metformin 1000mg", 0.20),
            ("Glimepiride 2mg", 0.15), ("Insulin Glargine", 0.12),
            ("Sitagliptin 100mg", 0.05), ("Empagliflozin 25mg", 0.03),
        ],
        "severity": ["Controlled", "Moderately Controlled", "Uncontrolled"],
        "severity_weights": [0.4, 0.35, 0.25],
    },
    "Hypertension": {
        "category": "chronic_cardio",
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
        "category": "chronic_cardio",
        "medications": [
            ("Aspirin 81mg", 0.30), ("Atorvastatin 20mg", 0.25),
            ("Clopidogrel 75mg", 0.15), ("Rosuvastatin 10mg", 0.12),
            ("Warfarin 5mg", 0.10), ("Metoprolol 50mg", 0.08),
        ],
        "severity": ["Stable", "Moderate", "Severe"],
        "severity_weights": [0.45, 0.35, 0.20],
    },
    "Obesity": {
        "category": "chronic_metabolic",
        "medications": [
            ("Orlistat 120mg", 0.30), ("Lifestyle Modification Only", 0.50),
            ("Phentermine 37.5mg", 0.10), ("Liraglutide 3mg", 0.10),
        ],
        "severity": ["Class I (BMI 30-34.9)", "Class II (BMI 35-39.9)", "Class III (BMI 40+)"],
        "severity_weights": [0.50, 0.30, 0.20],
    },
    "Asthma / COPD": {
        "category": "chronic_respiratory",
        "medications": [
            ("Salbutamol Inhaler", 0.35), ("Fluticasone Inhaler", 0.25),
            ("Montelukast 10mg", 0.15), ("Ipratropium Inhaler", 0.10),
            ("Budesonide/Formoterol", 0.10), ("Prednisolone 5mg", 0.05),
        ],
        "severity": ["Mild Intermittent", "Mild Persistent", "Moderate Persistent", "Severe"],
        "severity_weights": [0.30, 0.30, 0.25, 0.15],
    },
    "Chronic Kidney Disease": {
        "category": "chronic_cardio",
        "medications": [
            ("Erythropoietin", 0.20), ("Calcium Carbonate 500mg", 0.25),
            ("Furosemide 40mg", 0.20), ("Sodium Bicarbonate", 0.15),
            ("Iron Supplement", 0.20),
        ],
        "severity": ["Stage 1-2", "Stage 3", "Stage 4-5"],
        "severity_weights": [0.35, 0.40, 0.25],
    },
    "Cancer": {
        "category": "cancer",
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
        "category": "mental_health",
        "medications": [
            ("Sertraline 50mg", 0.25), ("Fluoxetine 20mg", 0.20),
            ("Amitriptyline 25mg", 0.15), ("Escitalopram 10mg", 0.15),
            ("Diazepam 5mg", 0.10), ("Counseling/Therapy Only", 0.15),
        ],
        "severity": ["Mild", "Moderate", "Severe"],
        "severity_weights": [0.35, 0.40, 0.25],
    },
    "Sickle Cell Disease": {
        "category": "genetic",
        "medications": [
            ("Hydroxyurea 500mg", 0.35), ("Folic Acid 5mg", 0.30),
            ("Penicillin V 250mg", 0.15), ("Pain Management", 0.20),
        ],
        "severity": ["Mild (Trait)", "Moderate", "Severe"],
        "severity_weights": [0.40, 0.35, 0.25],
    },

    # ---- Communicable / endemic ----
    "HIV/AIDS": {
        "category": "infectious_chronic",
        "medications": [
            ("Tenofovir/Emtricitabine", 0.35), ("Dolutegravir 50mg", 0.30),
            ("Efavirenz 600mg", 0.15), ("Atazanavir/Ritonavir", 0.10),
            ("Lamivudine/Zidovudine", 0.10),
        ],
        "severity": ["Well Controlled (Undetectable)", "Controlled", "Advanced"],
        "severity_weights": [0.50, 0.35, 0.15],
    },
    "Tuberculosis": {
        "category": "infectious_acute",
        "medications": [
            ("Isoniazid + Rifampicin (RHZE)", 0.45), ("Rifampicin 150mg", 0.15),
            ("Isoniazid 300mg", 0.15), ("Pyrazinamide 500mg", 0.10),
            ("Ethambutol 400mg", 0.10), ("MDR-TB Regimen", 0.05),
        ],
        "severity": ["Latent", "Active - Drug Sensitive", "Active - Drug Resistant"],
        "severity_weights": [0.40, 0.48, 0.12],
    },
    "Malaria": {
        "category": "infectious_acute",
        "medications": [
            ("Artemether/Lumefantrine (ACT)", 0.45), ("Artesunate Injection", 0.20),
            ("Chloroquine", 0.10), ("Sulfadoxine/Pyrimethamine", 0.10),
            ("Primaquine", 0.08), ("Quinine", 0.07),
        ],
        "severity": ["Uncomplicated", "Severe", "Cerebral"],
        "severity_weights": [0.70, 0.24, 0.06],
    },
    "Dengue / Arbovirus": {
        "category": "infectious_acute",
        "medications": [
            ("Supportive Care / Paracetamol", 0.55), ("IV Fluid Rehydration", 0.25),
            ("Hospital Observation", 0.15), ("Platelet Transfusion", 0.05),
        ],
        "severity": ["Dengue (No Warning Signs)", "Dengue with Warning Signs", "Severe Dengue"],
        "severity_weights": [0.60, 0.30, 0.10],
    },
    "Schistosomiasis": {
        "category": "infectious_chronic",
        "medications": [
            ("Praziquantel 600mg", 0.75), ("Repeat Praziquantel Course", 0.15),
            ("Supportive Care", 0.10),
        ],
        "severity": ["Mild", "Moderate", "Chronic / Organ Involvement"],
        "severity_weights": [0.45, 0.35, 0.20],
    },
    "Chagas Disease": {
        "category": "infectious_chronic",
        "medications": [
            ("Benznidazole", 0.55), ("Nifurtimox", 0.25),
            ("Cardiac Management", 0.15), ("Supportive Care", 0.05),
        ],
        "severity": ["Acute", "Indeterminate (Chronic)", "Chronic - Cardiac/GI"],
        "severity_weights": [0.20, 0.50, 0.30],
    },
}

# Generic age multipliers applied by the engine, keyed by condition category.
# Country configs layer their own ethnicity/sex adjustments on top of these.
AGE_MULTIPLIERS = {
    "chronic_metabolic": [(60, 2.0), (45, 1.5), (30, 1.0), (0, 0.25)],
    "chronic_cardio":    [(60, 2.2), (45, 1.5), (30, 1.0), (0, 0.2)],
    "chronic_respiratory": [(0, 1.0)],
    "cancer":            [(55, 2.5), (35, 1.0), (0, 0.15)],
    "mental_health":     [(0, 1.0)],
    "genetic":           [(0, 1.0)],
    "infectious_chronic": [(0, 1.0)],
    # Acute infections skew toward children/young adults in endemic settings.
    "infectious_acute":  [(60, 0.8), (40, 0.9), (15, 1.0), (0, 1.6)],
}


def age_multiplier(category, age):
    """Return the age-based prevalence multiplier for a condition category."""
    for threshold, mult in AGE_MULTIPLIERS.get(category, [(0, 1.0)]):
        if age >= threshold:
            return mult
    return 1.0


def age_group(age):
    if age < 30:
        return "18-29"
    elif age < 40:
        return "30-39"
    elif age < 50:
        return "40-49"
    elif age < 60:
        return "50-59"
    elif age < 70:
        return "60-69"
    return "70+"


AGE_ORDER = ["18-29", "30-39", "40-49", "50-59", "60-69", "70+"]
