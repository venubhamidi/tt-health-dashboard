"""Mali country configuration. Display language: French."""

CONFIG = {
    "code": "ML",
    "name": "Mali",
    "name_local": "Mali",
    "language": "fr",
    "regions": [
        "Bamako", "Sikasso", "Koulikoro", "Ségou", "Mopti", "Kayes", "Gao",
        "Tombouctou", "Kidal", "Ménaka", "Taoudénit",
    ],
    "ethnicities": {
        "Bambara": 0.33,
        "Peul (Fula)": 0.13,
        "Sarakolé (Soninké)": 0.10,
        "Tuareg/Maure": 0.10,
        "Malinké": 0.09,
        "Dogon": 0.08,
        "Songhaï": 0.07,
        "Senufo": 0.05,
        "Bobo": 0.03,
        "Autre": 0.02,
    },
    "insurance": [
        ("Paiement Direct", 0.65), ("AMO (Assurance Maladie Obligatoire)", 0.15),
        ("RAMED (Indigents)", 0.10), ("Mutuelle/Privé", 0.10),
    ],
    # Very young population
    "age_brackets": [((18, 29), 0.44), ((30, 44), 0.33), ((45, 59), 0.15), ((60, 85), 0.08)],
    "first_names_male": [
        "Amadou", "Moussa", "Ibrahim", "Modibo", "Oumar", "Seydou", "Bakary",
        "Adama", "Mamadou", "Boubacar", "Cheick", "Drissa", "Souleymane", "Yaya",
        "Alassane", "Bourama", "Fousseyni", "Karim", "Sekou", "Abdoulaye",
        "Issa", "Mahamadou", "Broulaye", "Daouda", "Tiémoko",
    ],
    "first_names_female": [
        "Aminata", "Fatoumata", "Mariam", "Kadiatou", "Awa", "Rokia", "Assitan",
        "Oumou", "Djeneba", "Fanta", "Nana", "Sanata", "Coumba", "Hawa", "Bintou",
        "Salimata", "Ramata", "Aïcha", "Kadidia", "Néné", "Mah", "Djelika",
        "Korotoumou", "Assétou", "Maïmouna",
    ],
    "last_names": [
        "Traoré", "Coulibaly", "Keïta", "Diarra", "Konaté", "Diallo", "Sidibé",
        "Touré", "Cissé", "Sangaré", "Doumbia", "Camara", "Maïga", "Kanté",
        "Bah", "Dembélé", "Fofana", "Sissoko", "Samaké", "Bagayoko",
        "Guindo", "Sow", "Diakité", "Kone", "Berthé",
    ],
    "conditions": {
        "Type 2 Diabetes": {"base_prob": 0.04},
        "Hypertension": {"base_prob": 0.18},
        "Cardiovascular Disease": {"base_prob": 0.03},
        "Asthma / COPD": {"base_prob": 0.05},
        "Malaria": {"base_prob": 0.12},
        "Tuberculosis": {"base_prob": 0.015},
        "HIV/AIDS": {"base_prob": 0.012},
        "Schistosomiasis": {"base_prob": 0.04},
        "Sickle Cell Disease": {"base_prob": 0.03, "ethnicity_adjust": {"Tuareg/Maure": 0.3}},
        "Cancer": {"base_prob": 0.015},
        "Depression / Anxiety": {"base_prob": 0.05},
    },
}
