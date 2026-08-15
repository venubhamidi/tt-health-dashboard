"""Brazil country configuration."""

CONFIG = {
    "code": "BR",
    "name": "Brazil",
    "name_local": "Brasil",
    "language": "pt",
    "regions": [
        "São Paulo", "Rio de Janeiro", "Minas Gerais", "Bahia", "Paraná",
        "Rio Grande do Sul", "Pernambuco", "Ceará", "Pará", "Santa Catarina",
        "Goiás", "Maranhão", "Amazonas", "Espírito Santo", "Mato Grosso",
    ],
    # IBGE cor/raça categories
    "ethnicities": {
        "Parda": 0.45,
        "Branca": 0.43,
        "Preta": 0.10,
        "Amarela": 0.01,
        "Indígena": 0.01,
    },
    "insurance": [
        ("SUS (Público)", 0.70), ("Saúde Suplementar (Privado)", 0.25),
        ("Particular (Out-of-Pocket)", 0.05),
    ],
    "age_brackets": [((18, 29), 0.28), ((30, 44), 0.30), ((45, 59), 0.24), ((60, 85), 0.18)],
    "first_names_male": [
        "João", "José", "Antônio", "Carlos", "Paulo", "Pedro", "Lucas", "Luiz",
        "Marcos", "Gabriel", "Rafael", "Daniel", "Marcelo", "Bruno", "Eduardo",
        "Felipe", "Rodrigo", "Gustavo", "Thiago", "Leandro", "Fernando",
        "Ricardo", "Vinícius", "André", "Matheus",
    ],
    "first_names_female": [
        "Maria", "Ana", "Francisca", "Juliana", "Márcia", "Fernanda", "Patrícia",
        "Aline", "Camila", "Amanda", "Bruna", "Jéssica", "Letícia", "Larissa",
        "Beatriz", "Vanessa", "Gabriela", "Carla", "Adriana", "Sandra",
        "Luana", "Débora", "Renata", "Mariana", "Bianca",
    ],
    "last_names": [
        "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves",
        "Pereira", "Lima", "Gomes", "Costa", "Ribeiro", "Martins", "Carvalho",
        "Almeida", "Lopes", "Soares", "Fernandes", "Vieira", "Barbosa",
        "Rocha", "Dias", "Nascimento", "Araújo", "Cardoso",
    ],
    "conditions": {
        "Type 2 Diabetes": {"base_prob": 0.10},
        "Hypertension": {"base_prob": 0.24, "ethnicity_adjust": {"Preta": 1.3}},
        "Cardiovascular Disease": {"base_prob": 0.09},
        "Obesity": {"base_prob": 0.22},
        "Asthma / COPD": {"base_prob": 0.09},
        "Chronic Kidney Disease": {"base_prob": 0.05},
        "Cancer": {"base_prob": 0.05},
        "Depression / Anxiety": {"base_prob": 0.11},
        "Dengue / Arbovirus": {"base_prob": 0.08},
        "Chagas Disease": {"base_prob": 0.02},
        "Sickle Cell Disease": {"base_prob": 0.01, "ethnicity_adjust": {"Preta": 3.0, "Parda": 1.5, "Branca": 0.2}},
        "HIV/AIDS": {"base_prob": 0.006},
        "Tuberculosis": {"base_prob": 0.005},
    },
}
