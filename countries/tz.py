"""Tanzania country configuration. Display language: Swahili."""

CONFIG = {
    "code": "TZ",
    "name": "Tanzania",
    "name_local": "Tanzania",
    "language": "sw",
    "regions": [
        "Dar es Salaam", "Mwanza", "Arusha", "Dodoma", "Mbeya", "Morogoro",
        "Tanga", "Kilimanjaro", "Tabora", "Kagera", "Mtwara", "Zanzibar Mjini",
        "Singida", "Iringa", "Shinyanga",
    ],
    "ethnicities": {
        "Sukuma": 0.16,
        "Chagga": 0.05,
        "Haya": 0.05,
        "Nyamwezi": 0.04,
        "Makonde": 0.04,
        "Zaramo": 0.03,
        "Other Bantu": 0.56,
        "Other": 0.07,
    },
    "insurance": [
        ("Out-of-Pocket", 0.65), ("NHIF (Bima ya Afya)", 0.15),
        ("CHF/iCHF (Community)", 0.10), ("Private", 0.10),
    ],
    # Young population
    "age_brackets": [((18, 29), 0.42), ((30, 44), 0.33), ((45, 59), 0.17), ((60, 85), 0.08)],
    "first_names_male": [
        "Juma", "Bakari", "Rashidi", "Hamisi", "Salum", "Athumani", "Musa",
        "Ally", "Emmanuel", "Baraka", "Godfrey", "Elias", "Daudi", "Isaya",
        "Shabani", "Ramadhani", "Selemani", "Kelvin", "Deo", "Erick",
        "Frank", "Joseph", "Mussa", "Hassan", "Abdallah",
    ],
    "first_names_female": [
        "Neema", "Amina", "Zainabu", "Fatuma", "Rehema", "Halima", "Asha",
        "Mwanaisha", "Grace", "Happy", "Upendo", "Tumaini", "Furaha", "Salma",
        "Rukia", "Devota", "Anna", "Esther", "Zawadi", "Subira",
        "Mariamu", "Hawa", "Jane", "Sophia", "Aisha",
    ],
    "last_names": [
        "Mwakalinga", "Mushi", "Kimaro", "Massawe", "Shirima", "Mrema", "Nyerere",
        "Mwaikambo", "Mgeni", "Juma", "Said", "Hassan", "Ndosi", "Lyimo", "Swai",
        "Kessy", "Mollel", "Mbwana", "Kilonzo", "Makame", "Mwakyusa", "Mkumbo",
        "Ngassa", "Mmbaga", "Kikwete",
    ],
    "conditions": {
        "Type 2 Diabetes": {"base_prob": 0.05},
        "Hypertension": {"base_prob": 0.22},
        "Cardiovascular Disease": {"base_prob": 0.04},
        "Asthma / COPD": {"base_prob": 0.05},
        "Malaria": {"base_prob": 0.08},
        "HIV/AIDS": {"base_prob": 0.045},
        "Tuberculosis": {"base_prob": 0.02},
        "Schistosomiasis": {"base_prob": 0.03},
        "Sickle Cell Disease": {"base_prob": 0.02},
        "Cancer": {"base_prob": 0.02},
        "Depression / Anxiety": {"base_prob": 0.05},
    },
}
