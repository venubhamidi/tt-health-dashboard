"""
Display-time translation layer.

Design: the database stores canonical ENGLISH coded values and English is the
source language. Nothing here changes what is queried or stored — these maps are
applied only when rendering. Two helpers:

    t(lang, key)   -> translate a UI chrome string (falls back to English)
    tv(lang, value)-> translate a categorical DATA value such as a condition
                      name or adherence level (falls back to the value itself)

Proper nouns (patient names, region names, medication/drug names) are NOT
translated — they are rendered exactly as stored in every language.

pt/es/fr strings are translated in full. sw (Swahili) and ti (Tigrinya) cover
the high-visibility chrome and the clinical vocabulary; anything not present
falls back to English. Swahili and Tigrinya medical terms should be confirmed
by a native clinical reviewer before production use.
"""

LANGUAGES = {
    "en": "English",
    "pt": "Português",
    "es": "Español",
    "fr": "Français",
    "sw": "Kiswahili",
    "ti": "ትግርኛ",
}

# Full language name used when instructing the AI which language to answer in.
AI_LANGUAGE_NAME = {
    "en": "English",
    "pt": "Portuguese",
    "es": "Spanish",
    "fr": "French",
    "sw": "Swahili",
    "ti": "Tigrinya",
}

# ---------------------------------------------------------------------------
# UI chrome strings
# ---------------------------------------------------------------------------
_UI = {
    "en": {
        "subtitle": "Medication Distribution Analytics",
        "patient_db": "Patient Database",
        "tab_medication": "Medication Distribution",
        "tab_condition": "Condition Overview",
        "tab_demographics": "Demographics & Lifestyle",
        "tab_explorer": "Patient Explorer",
        "tab_ai": "AI Health Assistant",
        "tab_agent": "AI Agent (LangGraph)",
        "agent_caption": "A tool-using agent that queries the live data to answer your question.",
        "agent_steps": "Agent steps (tools called)",
        "agent_examples": "Example questions (click one — the agent will query the live data):",
        "agent_tools_header": "Tools available to this agent",
        "agent_not_installed": "LangGraph / LangChain not installed. Install with: pip install langgraph langchain-anthropic",
        "kpi_total": "Total Patients",
        "kpi_conditions": "Active Conditions",
        "kpi_meds": "Medications Prescribed",
        "kpi_avg_risk": "Avg Risk Score",
        "kpi_high_risk": "High Risk Patients",
        "filters": "Filters",
        "country": "Country",
        "language": "Language",
        "f_region": "Region",
        "f_age": "Age Group",
        "f_gender": "Gender",
        "f_ethnicity": "Ethnicity",
        "f_insurance": "Insurance",
        "sec_med_analysis": "Medication Distribution Analysis",
        "sec_condition": "Condition Prevalence & Analysis",
        "sec_demographics": "Demographics & Lifestyle Factors",
        "sec_explorer": "Patient Explorer",
        "ai_caption": "Ask questions about medication distribution, patient demographics, and population health trends.",
        "ai_suggested": "Suggested questions:",
        "ai_placeholder": "Ask about medication distribution, demographics, trends...",
        "ai_analyzing": "Analyzing population data...",
        "ai_no_key": "ANTHROPIC_API_KEY environment variable is not set. Please set it and restart the app.",
    },
    "pt": {
        "subtitle": "Análise de Distribuição de Medicamentos",
        "patient_db": "Base de Pacientes",
        "tab_medication": "Distribuição de Medicamentos",
        "tab_condition": "Visão Geral das Condições",
        "tab_demographics": "Demografia e Estilo de Vida",
        "tab_explorer": "Explorador de Pacientes",
        "tab_ai": "Assistente de Saúde IA",
        "tab_agent": "Agente IA (LangGraph)",
        "agent_caption": "Um agente que usa ferramentas para consultar os dados e responder à sua pergunta.",
        "agent_steps": "Etapas do agente (ferramentas usadas)",
        "agent_examples": "Perguntas de exemplo (clique numa — o agente consultará os dados ao vivo):",
        "agent_tools_header": "Ferramentas disponíveis para este agente",
        "agent_not_installed": "LangGraph / LangChain não instalado. Instale com: pip install langgraph langchain-anthropic",
        "kpi_total": "Total de Pacientes",
        "kpi_conditions": "Condições Ativas",
        "kpi_meds": "Medicamentos Prescritos",
        "kpi_avg_risk": "Risco Médio",
        "kpi_high_risk": "Pacientes de Alto Risco",
        "filters": "Filtros",
        "country": "País",
        "language": "Idioma",
        "f_region": "Região",
        "f_age": "Faixa Etária",
        "f_gender": "Sexo",
        "f_ethnicity": "Etnia",
        "f_insurance": "Cobertura",
        "sec_med_analysis": "Análise da Distribuição de Medicamentos",
        "sec_condition": "Prevalência e Análise de Condições",
        "sec_demographics": "Fatores Demográficos e de Estilo de Vida",
        "sec_explorer": "Explorador de Pacientes",
        "ai_caption": "Faça perguntas sobre distribuição de medicamentos, demografia dos pacientes e tendências de saúde populacional.",
        "ai_suggested": "Perguntas sugeridas:",
        "ai_placeholder": "Pergunte sobre medicamentos, demografia, tendências...",
        "ai_analyzing": "Analisando dados populacionais...",
        "ai_no_key": "A variável de ambiente ANTHROPIC_API_KEY não está definida. Defina-a e reinicie o aplicativo.",
    },
    "es": {
        "subtitle": "Análisis de Distribución de Medicamentos",
        "patient_db": "Base de Pacientes",
        "tab_medication": "Distribución de Medicamentos",
        "tab_condition": "Resumen de Enfermedades",
        "tab_demographics": "Demografía y Estilo de Vida",
        "tab_explorer": "Explorador de Pacientes",
        "tab_ai": "Asistente de Salud IA",
        "tab_agent": "Agente IA (LangGraph)",
        "agent_caption": "Un agente que usa herramientas para consultar los datos y responder su pregunta.",
        "agent_steps": "Pasos del agente (herramientas usadas)",
        "agent_examples": "Preguntas de ejemplo (haga clic en una — el agente consultará los datos en vivo):",
        "agent_tools_header": "Herramientas disponibles para este agente",
        "agent_not_installed": "LangGraph / LangChain no instalado. Instálelo con: pip install langgraph langchain-anthropic",
        "kpi_total": "Total de Pacientes",
        "kpi_conditions": "Enfermedades Activas",
        "kpi_meds": "Medicamentos Recetados",
        "kpi_avg_risk": "Riesgo Promedio",
        "kpi_high_risk": "Pacientes de Alto Riesgo",
        "filters": "Filtros",
        "country": "País",
        "language": "Idioma",
        "f_region": "Región",
        "f_age": "Grupo de Edad",
        "f_gender": "Sexo",
        "f_ethnicity": "Etnia",
        "f_insurance": "Cobertura",
        "sec_med_analysis": "Análisis de Distribución de Medicamentos",
        "sec_condition": "Prevalencia y Análisis de Enfermedades",
        "sec_demographics": "Factores Demográficos y de Estilo de Vida",
        "sec_explorer": "Explorador de Pacientes",
        "ai_caption": "Haga preguntas sobre distribución de medicamentos, demografía de pacientes y tendencias de salud poblacional.",
        "ai_suggested": "Preguntas sugeridas:",
        "ai_placeholder": "Pregunte sobre medicamentos, demografía, tendencias...",
        "ai_analyzing": "Analizando datos poblacionales...",
        "ai_no_key": "La variable de entorno ANTHROPIC_API_KEY no está definida. Configúrela y reinicie la aplicación.",
    },
    "fr": {
        "subtitle": "Analyse de la Distribution des Médicaments",
        "patient_db": "Base de Patients",
        "tab_medication": "Distribution des Médicaments",
        "tab_condition": "Aperçu des Pathologies",
        "tab_demographics": "Démographie et Mode de Vie",
        "tab_explorer": "Explorateur de Patients",
        "tab_ai": "Assistant Santé IA",
        "tab_agent": "Agent IA (LangGraph)",
        "agent_caption": "Un agent qui utilise des outils pour interroger les données et répondre à votre question.",
        "agent_steps": "Étapes de l'agent (outils utilisés)",
        "agent_examples": "Questions d'exemple (cliquez sur une — l'agent interrogera les données en direct) :",
        "agent_tools_header": "Outils disponibles pour cet agent",
        "agent_not_installed": "LangGraph / LangChain non installé. Installez avec : pip install langgraph langchain-anthropic",
        "kpi_total": "Total des Patients",
        "kpi_conditions": "Pathologies Actives",
        "kpi_meds": "Médicaments Prescrits",
        "kpi_avg_risk": "Score de Risque Moyen",
        "kpi_high_risk": "Patients à Haut Risque",
        "filters": "Filtres",
        "country": "Pays",
        "language": "Langue",
        "f_region": "Région",
        "f_age": "Tranche d'Âge",
        "f_gender": "Sexe",
        "f_ethnicity": "Ethnicité",
        "f_insurance": "Couverture",
        "sec_med_analysis": "Analyse de la Distribution des Médicaments",
        "sec_condition": "Prévalence et Analyse des Pathologies",
        "sec_demographics": "Facteurs Démographiques et de Mode de Vie",
        "sec_explorer": "Explorateur de Patients",
        "ai_caption": "Posez des questions sur la distribution des médicaments, la démographie des patients et les tendances de santé publique.",
        "ai_suggested": "Questions suggérées :",
        "ai_placeholder": "Posez une question sur les médicaments, la démographie, les tendances...",
        "ai_analyzing": "Analyse des données de population...",
        "ai_no_key": "La variable d'environnement ANTHROPIC_API_KEY n'est pas définie. Définissez-la et redémarrez l'application.",
    },
    "sw": {
        "subtitle": "Uchambuzi wa Usambazaji wa Dawa",
        "patient_db": "Hifadhidata ya Wagonjwa",
        "tab_medication": "Usambazaji wa Dawa",
        "tab_condition": "Muhtasari wa Magonjwa",
        "tab_demographics": "Idadi ya Watu na Mtindo wa Maisha",
        "tab_explorer": "Kichunguzi cha Wagonjwa",
        "tab_ai": "Msaidizi wa Afya wa AI",
        "agent_tools_header": "Zana zinazopatikana kwa wakala huyu",
        "kpi_total": "Jumla ya Wagonjwa",
        "kpi_conditions": "Magonjwa Yaliyopo",
        "kpi_meds": "Dawa Zilizoandikwa",
        "kpi_avg_risk": "Wastani wa Hatari",
        "kpi_high_risk": "Wagonjwa wa Hatari Kubwa",
        "filters": "Vichujio",
        "country": "Nchi",
        "language": "Lugha",
        "f_region": "Mkoa",
        "f_age": "Kikundi cha Umri",
        "f_gender": "Jinsia",
        "f_ethnicity": "Kabila",
        "f_insurance": "Bima",
        "sec_med_analysis": "Uchambuzi wa Usambazaji wa Dawa",
        "sec_condition": "Kuenea na Uchambuzi wa Magonjwa",
        "sec_demographics": "Mambo ya Idadi ya Watu na Mtindo wa Maisha",
        "sec_explorer": "Kichunguzi cha Wagonjwa",
        "ai_caption": "Uliza maswali kuhusu usambazaji wa dawa, idadi ya wagonjwa, na mwelekeo wa afya ya jamii.",
        "ai_suggested": "Maswali yanayopendekezwa:",
        "ai_placeholder": "Uliza kuhusu dawa, idadi ya watu, mwelekeo...",
        "ai_analyzing": "Inachambua data ya idadi ya watu...",
        "ai_no_key": "Kigezo cha mazingira ANTHROPIC_API_KEY hakijawekwa. Kiweke kisha uanzishe upya programu.",
    },
    "ti": {
        "subtitle": "ትንተና ምክፍፋል መድሓኒት",
        "patient_db": "ዳታቤዝ ሕሙማት",
        "tab_medication": "ምክፍፋል መድሓኒት",
        "tab_condition": "ሓፈሻዊ ትሕዝቶ ሕማማት",
        "tab_demographics": "ስነ-ህዝቢን ኣነባብራን",
        "tab_explorer": "መርማሪ ሕሙማት",
        "tab_ai": "ናይ ጥዕና ሓጋዚ AI",
        "kpi_total": "ጠቕላላ ሕሙማት",
        "kpi_conditions": "ንጡፍ ሕማማት",
        "kpi_meds": "እተኣዘዙ መድሓኒታት",
        "kpi_avg_risk": "ማእከላይ ሓደጋ",
        "kpi_high_risk": "ልዑል ሓደጋ ዘለዎም ሕሙማት",
        "filters": "መጻረዪታት",
        "country": "ሃገር",
        "language": "ቋንቋ",
        "f_region": "ዞባ",
        "f_age": "ጉጅለ ዕድመ",
        "f_gender": "ጾታ",
        "f_ethnicity": "ብሄር",
        "f_insurance": "መድሕን",
        "sec_med_analysis": "ትንተና ምክፍፋል መድሓኒት",
        "sec_condition": "ስርጭትን ትንተናን ሕማማት",
        "sec_demographics": "ስነ-ህዝብን ኣነባብራን ረቛሒታት",
        "sec_explorer": "መርማሪ ሕሙማት",
        "ai_caption": "ብዛዕባ ምክፍፋል መድሓኒት፡ ስነ-ህዝቢ ሕሙማትን ኣንፈት ጥዕና ህዝብን ሕተት።",
        "ai_suggested": "ዝሕመሙ ሕቶታት፦",
        "ai_placeholder": "ብዛዕባ መድሓኒት፡ ስነ-ህዝቢ፡ ኣንፈት ሕተት...",
        "ai_analyzing": "ናይ ህዝቢ ዳታ ይትንትን ኣሎ...",
        "ai_no_key": "ናይ ANTHROPIC_API_KEY ተለዋዋጢ ኣይተቐመጠን። ኣቐሚጥካ ነቲ መተግበሪ እንደገና ኣበግሶ።",
    },
}

# ---------------------------------------------------------------------------
# Categorical DATA values (stored in English, displayed translated)
# ---------------------------------------------------------------------------
_CONDITIONS = {
    "Type 2 Diabetes":        {"pt": "Diabetes Tipo 2", "es": "Diabetes Tipo 2", "fr": "Diabète de type 2", "sw": "Kisukari (Aina ya 2)", "ti": "ሽኮርያ (ዓይነት 2)"},
    "Hypertension":           {"pt": "Hipertensão", "es": "Hipertensión", "fr": "Hypertension", "sw": "Shinikizo la Damu", "ti": "ላዕለዋይ ጸቕጢ ደም"},
    "Cardiovascular Disease": {"pt": "Doença Cardiovascular", "es": "Enfermedad Cardiovascular", "fr": "Maladie cardiovasculaire", "sw": "Ugonjwa wa Moyo na Mishipa", "ti": "ሕማም ልቢ"},
    "Obesity":                {"pt": "Obesidade", "es": "Obesidad", "fr": "Obésité", "sw": "Unene Uliokithiri", "ti": "ውፍረት"},
    "Asthma / COPD":          {"pt": "Asma / DPOC", "es": "Asma / EPOC", "fr": "Asthme / BPCO", "sw": "Pumu / COPD", "ti": "ኣዝማ / ሕማም ሳምቡእ"},
    "Chronic Kidney Disease": {"pt": "Doença Renal Crônica", "es": "Enfermedad Renal Crónica", "fr": "Maladie rénale chronique", "sw": "Ugonjwa wa Figo Sugu", "ti": "ስር-የጠቐለለ ሕማም ኩሊት"},
    "Cancer":                 {"pt": "Câncer", "es": "Cáncer", "fr": "Cancer", "sw": "Saratani", "ti": "መንሽሮ"},
    "Depression / Anxiety":   {"pt": "Depressão / Ansiedade", "es": "Depresión / Ansiedad", "fr": "Dépression / Anxiété", "sw": "Msongo wa Mawazo / Wasiwasi", "ti": "ጭንቀት / ስክፍታ"},
    "Sickle Cell Disease":    {"pt": "Doença Falciforme", "es": "Enfermedad de Células Falciformes", "fr": "Drépanocytose", "sw": "Ugonjwa wa Selimundu", "ti": "ሕማም ማንጩ ደም"},
    "HIV/AIDS":               {"pt": "HIV/AIDS", "es": "VIH/SIDA", "fr": "VIH/SIDA", "sw": "VVU/UKIMWI", "ti": "ኤች.ኣይ.ቪ / ኤድስ"},
    "Tuberculosis":           {"pt": "Tuberculose", "es": "Tuberculosis", "fr": "Tuberculose", "sw": "Kifua Kikuu (TB)", "ti": "ስዓል (ቲቢ)"},
    "Malaria":                {"pt": "Malária", "es": "Malaria", "fr": "Paludisme", "sw": "Malaria", "ti": "ዓሶ"},
    "Dengue / Arbovirus":     {"pt": "Dengue / Arbovírus", "es": "Dengue / Arbovirus", "fr": "Dengue / Arbovirose", "sw": "Homa ya Dengue", "ti": "ደንጊ"},
    "Schistosomiasis":        {"pt": "Esquistossomose", "es": "Esquistosomiasis", "fr": "Schistosomiase", "sw": "Kichocho", "ti": "ቢልሃርዝያ"},
    "Chagas Disease":         {"pt": "Doença de Chagas", "es": "Enfermedad de Chagas", "fr": "Maladie de Chagas", "sw": "Ugonjwa wa Chagas", "ti": "ሕማም ቻጋስ"},
}

_ADHERENCE = {
    "Good":     {"pt": "Boa", "es": "Buena", "fr": "Bonne", "sw": "Nzuri", "ti": "ጽቡቕ"},
    "Moderate": {"pt": "Moderada", "es": "Moderada", "fr": "Modérée", "sw": "Wastani", "ti": "ማእከላይ"},
    "Poor":     {"pt": "Baixa", "es": "Baja", "fr": "Faible", "sw": "Hafifu", "ti": "ትሑት"},
}

_GENDER = {
    "Male":   {"pt": "Masculino", "es": "Masculino", "fr": "Homme", "sw": "Mwanaume", "ti": "ተባዕታይ"},
    "Female": {"pt": "Feminino", "es": "Femenino", "fr": "Femme", "sw": "Mwanamke", "ti": "ኣንስተይቲ"},
}

# Merge all value maps into one lookup for tv()
_VALUES = {}
for _m in (_CONDITIONS, _ADHERENCE, _GENDER):
    _VALUES.update(_m)


def t(lang, key):
    """Translate a UI chrome string, falling back to English."""
    return _UI.get(lang, {}).get(key) or _UI["en"].get(key, key)


def tv(lang, value):
    """Translate a categorical data value, falling back to the value itself."""
    if lang == "en" or value is None:
        return value
    return _VALUES.get(value, {}).get(lang, value)


# ---------------------------------------------------------------------------
# Example questions for the LangGraph agent tab. Each is phrased to trigger the
# agent's tools (adherence, risk, comorbidity, demographics). Languages without
# a list fall back to English.
# ---------------------------------------------------------------------------
_AGENT_SUGGESTIONS = {
    "en": [
        "Which condition has the worst medication adherence, and what are its top 3 medications?",
        "How many high-risk patients are there and what is the average risk score?",
        "What are the top comorbidity pairs in the population?",
        "Break down the patients by insurance type.",
        "Compare medication adherence for diabetes vs hypertension.",
    ],
    "pt": [
        "Qual condição tem a pior adesão à medicação e quais são os seus 3 principais medicamentos?",
        "Quantos pacientes são de alto risco e qual é a pontuação média de risco?",
        "Quais são os principais pares de comorbidade na população?",
        "Distribua os pacientes por tipo de plano de saúde.",
        "Compare a adesão à medicação entre diabetes e hipertensão.",
    ],
    "es": [
        "¿Qué enfermedad tiene la peor adherencia a la medicación y cuáles son sus 3 medicamentos principales?",
        "¿Cuántos pacientes son de alto riesgo y cuál es la puntuación media de riesgo?",
        "¿Cuáles son los principales pares de comorbilidad en la población?",
        "Distribuya los pacientes por tipo de cobertura.",
        "Compare la adherencia a la medicación entre diabetes e hipertensión.",
    ],
    "fr": [
        "Quelle pathologie présente la pire observance thérapeutique et quels sont ses 3 principaux médicaments ?",
        "Combien de patients sont à haut risque et quel est le score de risque moyen ?",
        "Quelles sont les principales paires de comorbidités dans la population ?",
        "Répartissez les patients par type de couverture santé.",
        "Comparez l'observance thérapeutique entre le diabète et l'hypertension.",
    ],
    "sw": [
        "Ni ugonjwa gani wenye uzingatiaji mbaya zaidi wa dawa, na dawa zake 3 kuu ni zipi?",
        "Kuna wagonjwa wangapi wa hatari kubwa na wastani wa alama ya hatari ni upi?",
        "Ni jozi zipi kuu za magonjwa yanayoambatana katika idadi ya watu?",
        "Gawanya wagonjwa kwa aina ya bima.",
        "Linganisha uzingatiaji wa dawa kati ya kisukari na shinikizo la damu.",
    ],
}


def agent_suggestions(lang):
    """Return example agent questions for a language (English fallback)."""
    return _AGENT_SUGGESTIONS.get(lang, _AGENT_SUGGESTIONS["en"])


# ---------------------------------------------------------------------------
# Suggested questions for the simple AI Health Assistant tab.
# ---------------------------------------------------------------------------
_ASSISTANT_SUGGESTIONS = {
    "en": [
        "What are the most commonly prescribed medications and for which conditions?",
        "How does medication usage differ across age groups?",
        "What is the medication adherence rate and which conditions have the worst adherence?",
        "Which regions have the highest prescription volumes?",
        "What are the top comorbidity pairs and how do they affect medication loads?",
        "Compare medication patterns between male and female patients.",
        "Which insurance types are associated with the most prescriptions?",
        "What interventions would you recommend for the high-risk patient group?",
    ],
    "pt": [
        "Quais são os medicamentos mais prescritos e para quais condições?",
        "Como o uso de medicamentos varia entre as faixas etárias?",
        "Qual é a taxa de adesão à medicação e quais condições têm a pior adesão?",
        "Quais regiões têm os maiores volumes de prescrição?",
        "Quais são os principais pares de comorbidade e como afetam a carga de medicamentos?",
        "Compare os padrões de medicação entre pacientes homens e mulheres.",
        "Quais tipos de plano de saúde estão associados a mais prescrições?",
        "Quais intervenções você recomendaria para o grupo de pacientes de alto risco?",
    ],
    "es": [
        "¿Cuáles son los medicamentos más recetados y para qué enfermedades?",
        "¿Cómo varía el uso de medicamentos entre los grupos de edad?",
        "¿Cuál es la tasa de adherencia y qué enfermedades tienen la peor adherencia?",
        "¿Qué regiones tienen los mayores volúmenes de prescripción?",
        "¿Cuáles son los principales pares de comorbilidad y cómo afectan la carga de medicamentos?",
        "Compare los patrones de medicación entre pacientes hombres y mujeres.",
        "¿Qué tipos de cobertura se asocian con más prescripciones?",
        "¿Qué intervenciones recomendaría para el grupo de pacientes de alto riesgo?",
    ],
    "fr": [
        "Quels sont les médicaments les plus prescrits et pour quelles pathologies ?",
        "Comment l'usage des médicaments varie-t-il selon les tranches d'âge ?",
        "Quel est le taux d'observance et quelles pathologies ont la pire observance ?",
        "Quelles régions ont les plus gros volumes de prescription ?",
        "Quelles sont les principales paires de comorbidités et comment affectent-elles la charge médicamenteuse ?",
        "Comparez les schémas de médication entre les patients hommes et femmes.",
        "Quels types de couverture sont associés au plus de prescriptions ?",
        "Quelles interventions recommanderiez-vous pour le groupe de patients à haut risque ?",
    ],
    "sw": [
        "Ni dawa zipi zinazoandikwa zaidi na kwa magonjwa gani?",
        "Matumizi ya dawa yanatofautianaje kati ya vikundi vya umri?",
        "Kiwango cha uzingatiaji wa dawa ni kipi na magonjwa yapi yana uzingatiaji mbaya zaidi?",
        "Ni mikoa ipi yenye viwango vikubwa zaidi vya maagizo ya dawa?",
        "Ni jozi zipi kuu za magonjwa yanayoambatana na zinaathirije mzigo wa dawa?",
        "Linganisha mifumo ya dawa kati ya wagonjwa wa kiume na wa kike.",
        "Ni aina zipi za bima zinazohusiana na maagizo mengi zaidi?",
        "Ni hatua zipi ungependekeza kwa kundi la wagonjwa wa hatari kubwa?",
    ],
}


def assistant_suggestions(lang):
    """Return suggested questions for the simple assistant (English fallback)."""
    return _ASSISTANT_SUGGESTIONS.get(lang, _ASSISTANT_SUGGESTIONS["en"])


# ---------------------------------------------------------------------------
# One-line descriptions of the agent's tools (keyed by tool name), per language.
# Tool names themselves stay in English (they are code identifiers).
# ---------------------------------------------------------------------------
_AGENT_TOOL_DESC = {
    "condition_prevalence": {
        "en": "Prevalence of each condition (patient counts and %).",
        "pt": "Prevalência de cada condição (contagem de pacientes e %).",
        "es": "Prevalencia de cada enfermedad (número de pacientes y %).",
        "fr": "Prévalence de chaque pathologie (nombre de patients et %).",
        "sw": "Kuenea kwa kila ugonjwa (idadi ya wagonjwa na %).",
    },
    "top_medications": {
        "en": "Most-prescribed medications, optionally by condition / age group.",
        "pt": "Medicamentos mais prescritos, opcionalmente por condição / faixa etária.",
        "es": "Medicamentos más recetados, opcionalmente por enfermedad / grupo de edad.",
        "fr": "Médicaments les plus prescrits, éventuellement par pathologie / tranche d'âge.",
        "sw": "Dawa zinazoandikwa zaidi, kwa hiari kwa ugonjwa / kikundi cha umri.",
    },
    "medication_adherence": {
        "en": "Adherence breakdown (Good/Moderate/Poor), optionally per condition.",
        "pt": "Distribuição da adesão (Boa/Moderada/Baixa), opcionalmente por condição.",
        "es": "Distribución de adherencia (Buena/Moderada/Baja), opcionalmente por enfermedad.",
        "fr": "Répartition de l'observance (Bonne/Modérée/Faible), éventuellement par pathologie.",
        "sw": "Mgawanyo wa uzingatiaji (Nzuri/Wastani/Hafifu), kwa hiari kwa ugonjwa.",
    },
    "demographics_breakdown": {
        "en": "Patient counts by age, gender, ethnicity, insurance or region.",
        "pt": "Contagem de pacientes por idade, sexo, etnia, plano de saúde ou região.",
        "es": "Número de pacientes por edad, sexo, etnia, cobertura o región.",
        "fr": "Nombre de patients par âge, sexe, ethnicité, couverture ou région.",
        "sw": "Idadi ya wagonjwa kwa umri, jinsia, kabila, bima au mkoa.",
    },
    "risk_summary": {
        "en": "Average risk score and high / medium / low risk counts.",
        "pt": "Pontuação média de risco e contagens de risco alto / médio / baixo.",
        "es": "Puntuación media de riesgo y recuentos de riesgo alto / medio / bajo.",
        "fr": "Score de risque moyen et nombres de risque élevé / moyen / faible.",
        "sw": "Wastani wa alama ya hatari na idadi za hatari kubwa / wastani / ndogo.",
    },
    "comorbidity_pairs": {
        "en": "Most common pairs of co-occurring conditions.",
        "pt": "Pares mais comuns de condições coexistentes.",
        "es": "Pares más comunes de enfermedades coexistentes.",
        "fr": "Paires les plus fréquentes de pathologies coexistantes.",
        "sw": "Jozi za kawaida za magonjwa yanayoambatana.",
    },
}


def tool_desc(lang, tool_name):
    """One-line description of an agent tool (English fallback)."""
    d = _AGENT_TOOL_DESC.get(tool_name, {})
    return d.get(lang) or d.get("en", "")
