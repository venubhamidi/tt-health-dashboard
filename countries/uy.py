"""Uruguay country configuration."""

CONFIG = {
    "code": "UY",
    "name": "Uruguay",
    "name_local": "Uruguay",
    "language": "es",
    "regions": [
        "Montevideo", "Canelones", "Maldonado", "Salto", "Paysandú", "Colonia",
        "Rivera", "Tacuarembó", "Artigas", "Durazno", "Florida", "San José",
        "Soriano", "Cerro Largo", "Rocha",
    ],
    "ethnicities": {
        "Blanca (Europea)": 0.88,
        "Afrodescendiente": 0.08,
        "Mestiza": 0.03,
        "Indígena": 0.01,
    },
    "insurance": [
        ("Mutualista (IAMC)", 0.55), ("ASSE (Público)", 0.35), ("Seguro Privado", 0.10),
    ],
    # Older age structure
    "age_brackets": [((18, 29), 0.22), ((30, 44), 0.27), ((45, 59), 0.25), ((60, 85), 0.26)],
    "first_names_male": [
        "Santiago", "Mateo", "Bruno", "Agustín", "Rodrigo", "Martín", "Diego",
        "Nicolás", "Federico", "Gonzalo", "Sebastián", "Facundo", "Joaquín",
        "Andrés", "Pablo", "Gustavo", "Álvaro", "Marcelo", "Fernando", "Leandro",
        "Mauricio", "Emiliano", "Ignacio", "Matías", "Guillermo",
    ],
    "first_names_female": [
        "Sofía", "Valentina", "Lucía", "Camila", "Martina", "Florencia", "Carolina",
        "Paula", "Victoria", "Micaela", "Natalia", "Gabriela", "Verónica", "Andrea",
        "Laura", "Cecilia", "Mariana", "Daniela", "Rosa", "Beatriz",
        "Julieta", "Agustina", "Romina", "Alejandra", "Carmen",
    ],
    "last_names": [
        "González", "Rodríguez", "Fernández", "Pérez", "García", "Martínez",
        "López", "Sánchez", "Silva", "Sosa", "Cabrera", "Núñez", "Rivero",
        "Correa", "Suárez", "Píriz", "Techera", "Barreto", "Bentancor", "Méndez",
        "Olivera", "Ferreira", "Da Silva", "Castro", "Barrios",
    ],
    "conditions": {
        "Type 2 Diabetes": {"base_prob": 0.09},
        "Hypertension": {"base_prob": 0.30},
        "Cardiovascular Disease": {"base_prob": 0.12},
        "Obesity": {"base_prob": 0.25},
        "Asthma / COPD": {"base_prob": 0.08},
        "Chronic Kidney Disease": {"base_prob": 0.06},
        "Cancer": {"base_prob": 0.07},
        "Depression / Anxiety": {"base_prob": 0.12},
        "Dengue / Arbovirus": {"base_prob": 0.02},
        "HIV/AIDS": {"base_prob": 0.005},
    },
}
