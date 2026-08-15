"""Cuba country configuration."""

CONFIG = {
    "code": "CU",
    "name": "Cuba",
    "name_local": "Cuba",
    "language": "es",
    "regions": [
        "La Habana", "Santiago de Cuba", "Holguín", "Camagüey", "Villa Clara",
        "Granma", "Matanzas", "Pinar del Río", "Las Tunas", "Cienfuegos",
        "Sancti Spíritus", "Ciego de Ávila", "Guantánamo", "Artemisa", "Mayabeque",
    ],
    "ethnicities": {
        "Blanca": 0.64,
        "Mulata/Mestiza": 0.27,
        "Negra": 0.09,
    },
    "insurance": [
        ("Sistema Nacional de Salud (Universal)", 0.97), ("Servicios Internacionales", 0.03),
    ],
    # Aging population
    "age_brackets": [((18, 29), 0.20), ((30, 44), 0.26), ((45, 59), 0.26), ((60, 85), 0.28)],
    "first_names_male": [
        "José", "Juan", "Luis", "Carlos", "Jorge", "Alejandro", "Yoel", "Yasmany",
        "Reinier", "Osmani", "Dariel", "Yunior", "Michel", "Roberto", "Ernesto",
        "Ariel", "Frank", "Yandy", "Leandro", "Rolando", "Osvaldo", "Yordan",
        "Raúl", "Orlando", "Maikel",
    ],
    "first_names_female": [
        "María", "Yolanda", "Dayana", "Yanet", "Yaima", "Marisol", "Odalys",
        "Dulce", "Belkis", "Yusimí", "Grettel", "Leidy", "Mailín", "Damaris",
        "Caridad", "Yamila", "Anisley", "Niurka", "Bárbara", "Idalmis",
        "Yaneisy", "Dianelys", "Mercedes", "Yudith", "Liset",
    ],
    "last_names": [
        "Pérez", "González", "Rodríguez", "García", "Hernández", "Martínez",
        "López", "Díaz", "Sánchez", "Ramírez", "Torres", "Fernández", "Gómez",
        "Álvarez", "Castro", "Herrera", "Núñez", "Reyes", "Cruz", "Valdés",
        "Ortiz", "Ramos", "Rivero", "Betancourt", "Aguilar",
    ],
    "conditions": {
        "Type 2 Diabetes": {"base_prob": 0.11},
        "Hypertension": {"base_prob": 0.32},
        "Cardiovascular Disease": {"base_prob": 0.13},
        "Obesity": {"base_prob": 0.20},
        "Asthma / COPD": {"base_prob": 0.10},
        "Chronic Kidney Disease": {"base_prob": 0.05},
        "Cancer": {"base_prob": 0.08},
        "Depression / Anxiety": {"base_prob": 0.10},
        "Dengue / Arbovirus": {"base_prob": 0.04},
        "Sickle Cell Disease": {"base_prob": 0.01, "ethnicity_adjust": {"Negra": 3.0, "Blanca": 0.2}},
        "HIV/AIDS": {"base_prob": 0.004},
    },
}
