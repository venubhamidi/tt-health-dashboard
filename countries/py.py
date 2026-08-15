"""Paraguay country configuration."""

CONFIG = {
    "code": "PY",
    "name": "Paraguay",
    "name_local": "Paraguay",
    "language": "es",
    "regions": [
        "Asunción", "Central", "Alto Paraná", "Itapúa", "Caaguazú", "San Pedro",
        "Cordillera", "Guairá", "Caazapá", "Paraguarí", "Misiones", "Ñeembucú",
        "Amambay", "Canindeyú", "Concepción",
    ],
    "ethnicities": {
        "Mestiza": 0.90,
        "Blanca (Europea)": 0.05,
        "Afrodescendiente": 0.03,
        "Indígena": 0.02,
    },
    "insurance": [
        ("Público (MSPBS)", 0.70), ("IPS (Seguro Social)", 0.20), ("Privado", 0.10),
    ],
    "age_brackets": [((18, 29), 0.32), ((30, 44), 0.31), ((45, 59), 0.22), ((60, 85), 0.15)],
    "first_names_male": [
        "José", "Juan", "Carlos", "Miguel", "Luis", "Diego", "Marcos", "Fernando",
        "Ramón", "Derlis", "Óscar", "Víctor", "Hugo", "Gustavo", "Rodrigo",
        "Sergio", "Cristian", "Néstor", "Aldo", "Blas", "Julio", "Cristhian",
        "Antonio", "Roberto", "César",
    ],
    "first_names_female": [
        "María", "Rosa", "Carmen", "Lucía", "Fátima", "Liz", "Nidia", "Gloria",
        "Mónica", "Patricia", "Analía", "Larissa", "Belén", "Celeste", "Norma",
        "Mirta", "Sandra", "Griselda", "Antonia", "Ramona", "Gladys", "Lorena",
        "Natalia", "Silvia", "Estela",
    ],
    "last_names": [
        "González", "Benítez", "Rodríguez", "Martínez", "López", "Fernández",
        "Giménez", "Villalba", "Ramírez", "Ortiz", "Cáceres", "Duarte", "Sosa",
        "Franco", "Ayala", "Vera", "Ozuna", "Riquelme", "Britez", "Insfrán",
        "Aquino", "Rojas", "Bogado", "Escobar", "Núñez",
    ],
    "conditions": {
        "Type 2 Diabetes": {"base_prob": 0.10},
        "Hypertension": {"base_prob": 0.25},
        "Cardiovascular Disease": {"base_prob": 0.08},
        "Obesity": {"base_prob": 0.20},
        "Asthma / COPD": {"base_prob": 0.08},
        "Chronic Kidney Disease": {"base_prob": 0.05},
        "Cancer": {"base_prob": 0.04},
        "Depression / Anxiety": {"base_prob": 0.10},
        "Dengue / Arbovirus": {"base_prob": 0.09},
        "Chagas Disease": {"base_prob": 0.03},
        "HIV/AIDS": {"base_prob": 0.005},
        "Tuberculosis": {"base_prob": 0.005},
    },
}
