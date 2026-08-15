"""Djibouti country configuration. Display language: French."""

CONFIG = {
    "code": "DJ",
    "name": "Djibouti",
    "name_local": "Djibouti",
    "language": "fr",
    "regions": [
        "Djibouti (Ville)", "Ali Sabieh", "Dikhil", "Tadjourah", "Obock", "Arta",
    ],
    "ethnicities": {
        "Somali (Issa)": 0.60,
        "Afar": 0.35,
        "Arabe": 0.03,
        "Autre": 0.02,
    },
    "insurance": [
        ("Sans Assurance (Paiement Direct)", 0.55), ("CNSS (Sécurité Sociale)", 0.25),
        ("Assurance Militaire", 0.10), ("Assurance Privée", 0.10),
    ],
    # Young population
    "age_brackets": [((18, 29), 0.38), ((30, 44), 0.32), ((45, 59), 0.19), ((60, 85), 0.11)],
    "first_names_male": [
        "Abdi", "Mohamed", "Ahmed", "Hassan", "Ali", "Ibrahim", "Omar", "Yusuf",
        "Abdirahman", "Mahamoud", "Idriss", "Farah", "Houssein", "Kamil", "Guedi",
        "Djama", "Aden", "Ismael", "Saïd", "Bouh", "Robleh", "Waberi",
        "Awaleh", "Hared", "Elmi",
    ],
    "first_names_female": [
        "Fatouma", "Amina", "Halima", "Kadra", "Zahra", "Hodan", "Deka", "Nasra",
        "Ayan", "Sahra", "Ubah", "Faduma", "Ifrah", "Mariam", "Asli", "Roda",
        "Hibo", "Ismahan", "Nima", "Basra", "Khadija", "Farhia",
        "Samira", "Muna", "Warsan",
    ],
    "last_names": [
        "Mohamed", "Ahmed", "Hassan", "Ali", "Abdi", "Ibrahim", "Omar", "Farah",
        "Guedi", "Djama", "Aden", "Robleh", "Waberi", "Hared", "Elmi", "Barkat",
        "Kamil", "Idriss", "Bouh", "Awaleh", "Ismael", "Houmed", "Miguil",
        "Doualeh", "Ougoureh",
    ],
    "conditions": {
        "Type 2 Diabetes": {"base_prob": 0.06},
        "Hypertension": {"base_prob": 0.18},
        "Cardiovascular Disease": {"base_prob": 0.05},
        "Obesity": {"base_prob": 0.08},
        "Asthma / COPD": {"base_prob": 0.06},
        "Tuberculosis": {"base_prob": 0.02},
        "HIV/AIDS": {"base_prob": 0.015},
        "Malaria": {"base_prob": 0.04},
        "Cancer": {"base_prob": 0.02},
        "Depression / Anxiety": {"base_prob": 0.06},
    },
}
