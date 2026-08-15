"""Trinidad & Tobago country configuration."""

CONFIG = {
    "code": "TT",
    "name": "Trinidad & Tobago",
    "name_local": "Trinidad & Tobago",
    "language": "en",
    "regions": [
        "Port of Spain", "San Fernando", "Chaguanas", "Arima", "Point Fortin",
        "Scarborough (Tobago)", "Siparia", "Princes Town", "Couva", "Sangre Grande",
        "Tunapuna", "Diego Martin", "Penal", "Rio Claro", "Fyzabad",
    ],
    "ethnicities": {
        "Indo-Trinidadian": 0.35,
        "Afro-Trinidadian": 0.34,
        "Mixed": 0.23,
        "Other": 0.08,
    },
    "insurance": [
        ("Public (CDAP)", 0.40), ("Private Insurance", 0.25),
        ("Out-of-Pocket", 0.15), ("NHIS", 0.20),
    ],
    # Age-bracket weights: ((low, high), weight)
    "age_brackets": [((18, 29), 0.26), ((30, 44), 0.29), ((45, 59), 0.25), ((60, 85), 0.20)],
    "first_names_male": [
        "Avinash", "Brian", "Curtis", "Dwayne", "Emile", "Farouk", "Gregory",
        "Hamid", "Isaiah", "Jason", "Kevon", "Lester", "Marcus", "Navin",
        "Omar", "Prakash", "Ravi", "Shawn", "Tyrone", "Vijay", "Wayne",
        "Andre", "Darren", "Keron", "Rishi",
    ],
    "first_names_female": [
        "Alicia", "Brinda", "Camille", "Devika", "Esther", "Farzana", "Giselle",
        "Hema", "Indira", "Janelle", "Kamla", "Latoya", "Meera", "Nalini",
        "Priya", "Reshma", "Simone", "Tricia", "Uma", "Vanessa", "Wendy",
        "Yashoda", "Zara", "Asha", "Kavita",
    ],
    "last_names": [
        "Mohammed", "Singh", "Williams", "Ramnath", "Joseph", "Ali", "Charles",
        "Doodnath", "Edwards", "Fraser", "Garcia", "Hosein", "Isaac", "James",
        "Khan", "Lewis", "Maharaj", "Narine", "Persad", "Ramkissoon",
        "Sookdeo", "Thomas", "Warner", "Young", "Boodoo",
    ],
    "conditions": {
        "Type 2 Diabetes": {"base_prob": 0.13, "ethnicity_adjust": {"Indo-Trinidadian": 1.4}},
        "Hypertension": {"base_prob": 0.30, "ethnicity_adjust": {"Afro-Trinidadian": 1.3}},
        "Cardiovascular Disease": {"base_prob": 0.08},
        "Obesity": {"base_prob": 0.18},
        "Asthma / COPD": {"base_prob": 0.10},
        "Chronic Kidney Disease": {"base_prob": 0.05},
        "HIV/AIDS": {"base_prob": 0.015},
        "Cancer": {"base_prob": 0.04},
        "Depression / Anxiety": {"base_prob": 0.12},
        "Sickle Cell Disease": {"base_prob": 0.02, "ethnicity_adjust": {"Afro-Trinidadian": 3.0, "Indo-Trinidadian": 0.1}},
        "Dengue / Arbovirus": {"base_prob": 0.03},
    },
}
