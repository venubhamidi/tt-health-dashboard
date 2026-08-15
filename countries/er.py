"""Eritrea country configuration. Display language: Tigrinya."""

CONFIG = {
    "code": "ER",
    "name": "Eritrea",
    "name_local": "ኤርትራ",
    "language": "ti",
    "regions": [
        "Maekel (Asmara)", "Debub", "Gash-Barka", "Anseba",
        "Northern Red Sea", "Southern Red Sea",
    ],
    "ethnicities": {
        "Tigrinya": 0.55,
        "Tigre": 0.30,
        "Saho": 0.04,
        "Afar": 0.04,
        "Bilen": 0.02,
        "Kunama": 0.02,
        "Nara": 0.02,
        "Rashaida": 0.01,
    },
    "insurance": [
        ("Public Health Facilities", 0.75), ("Out-of-Pocket", 0.20), ("Employer/Other", 0.05),
    ],
    # Young population
    "age_brackets": [((18, 29), 0.40), ((30, 44), 0.32), ((45, 59), 0.18), ((60, 85), 0.10)],
    "first_names_male": [
        "Tesfay", "Yohannes", "Ghebre", "Mehari", "Abraham", "Fitsum", "Dawit",
        "Samuel", "Robel", "Filmon", "Henok", "Amanuel", "Biniam", "Yonas",
        "Kibrom", "Nahom", "Efrem", "Micael", "Aron", "Semere", "Isaias",
        "Tekle", "Goitom", "Yemane", "Haile",
    ],
    "first_names_female": [
        "Selam", "Rahwa", "Senait", "Hiwet", "Freweini", "Luwam", "Winta",
        "Askalu", "Almaz", "Tsega", "Danait", "Semhar", "Yordanos", "Mulu",
        "Abeba", "Saba", "Rigat", "Milen", "Feven", "Helen", "Ruta",
        "Zaid", "Tirhas", "Nardos", "Elsa",
    ],
    "last_names": [
        "Tesfay", "Ghebremariam", "Habte", "Weldu", "Berhane", "Tekle", "Haile",
        "Ghebreselassie", "Andom", "Mengesha", "Fessehaye", "Tewelde", "Okbay",
        "Kidane", "Yohannes", "Araya", "Gaim", "Hagos", "Estifanos", "Zerai",
        "Woldemariam", "Gebrehiwet", "Tsegay", "Beraki", "Solomon",
    ],
    "conditions": {
        "Type 2 Diabetes": {"base_prob": 0.05},
        "Hypertension": {"base_prob": 0.16},
        "Cardiovascular Disease": {"base_prob": 0.04},
        "Asthma / COPD": {"base_prob": 0.05},
        "Tuberculosis": {"base_prob": 0.02},
        "HIV/AIDS": {"base_prob": 0.01},
        "Malaria": {"base_prob": 0.03},
        "Schistosomiasis": {"base_prob": 0.02},
        "Cancer": {"base_prob": 0.02},
        "Depression / Anxiety": {"base_prob": 0.06},
    },
}
