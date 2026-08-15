# Multi-Country Population Health Dashboard

A Streamlit dashboard for population-health / medication-distribution analytics,
with synthetic patient data for multiple countries and a multilingual AI
assistant. Country is a **dimension**, not a fork: one codebase, one database,
one app, driven by per-country configuration.

Currently configured for: 🇧🇷 Brazil · 🇺🇾 Uruguay · 🇵🇾 Paraguay ·
🇹🇹 Trinidad & Tobago · 🇨🇺 Cuba · 🇩🇯 Djibouti · 🇪🇷 Eritrea · 🇹🇿 Tanzania ·
🇲🇱 Mali — **1,000 synthetic patients each (9,000 total).**

---

## Core architecture pattern

> **One app + one database. Country is a column and a config file, never a fork.**

Nine forks of the app/generator would mean every bug fix and every new chart is
done nine times and drifts out of sync. Instead, everything country-specific
lives in `countries/<code>.py`, and the engine/app/DB are country-agnostic.

```
                 ┌─────────────────────┐
                 │  countries/*.py     │  ← per-country CONFIG (data + language)
                 │  (regions, names,   │
                 │   ethnicity, payers,│
                 │   age, diseases)    │
                 └──────────┬──────────┘
                            │ REGISTRY
        ┌───────────────────┼────────────────────┐
        ▼                   ▼                     ▼
 generate_data.py      load_db.py             app.py
 (engine, loops    →   (adds `country`   →    (country picker →
  registry, 1000/       column, loads          WHERE country=… →
  country)              all rows)              translate on display)
                                                     │
                                              translations.py
                                        (labels + categorical values,
                                         store-English/display-local)
```

### Two golden rules

1. **Store canonical English, translate only at display time.** The database
   stores English coded values (`"Type 2 Diabetes"`, `"Poor"`). Queries always
   run on those stable English keys, so **the language toggle never touches the
   query layer**. Translation is a thin presentation concern.

2. **Translate labels, not proper nouns.** Patient names, region names and drug
   names are generated *country-appropriate* and rendered **as-is in every
   language** (a patient in Mali is `Amadou Traoré` in French and in English).
   Only the closed categorical vocabulary (condition names, adherence, gender)
   and UI chrome get translated.

---

## Directory layout

| Path | Responsibility |
|------|----------------|
| `countries/base.py` | Shared **condition library**: medications, severity bands, cancer subtypes, and generic age-risk curves. Universal across countries. |
| `countries/<cc>.py` | One **CONFIG** per country: regions, curated names, ethnicity mix, payer/insurance system, age structure, curated disease list w/ prevalence, language. |
| `countries/__init__.py` | `REGISTRY` = `{code: CONFIG}` in display order. |
| `generate_data.py` | Country-agnostic **generator engine**. Loops the registry, emits `RECORDS_PER_COUNTRY` patients each → `data/patients.json`. |
| `load_db.py` | Creates `patients`/`conditions`/`medications` tables (with a `country` column + index) and loads the JSON into Postgres. |
| `app.py` | Streamlit dashboard: country picker → per-country query → localized display + multilingual AI assistant. |
| `translations.py` | UI strings + categorical-value dictionaries per language; `t()` / `tv()` helpers. |
| `data/patients.json` | Generated dataset (all countries, flat list; each record carries `country`). |

---

## What data is generated

Each **patient record** (see `generate_data.py::generate_patient`):

```jsonc
{
  "patient_id": "ML-0042",          // "<COUNTRY>-<seq>"
  "country": "ML",
  "first_name": "Amadou",           // country-appropriate curated name
  "last_name": "Traoré",
  "gender": "Male", "age": 47, "date_of_birth": "…",
  "ethnicity": "Bambara",           // from the country's ethnicity mix
  "region": "Sikasso",              // real administrative division
  "insurance": "Paiement Direct",   // real payer/financing type
  "bmi": 27.4, "blood_pressure": "148/94", "systolic": 148, "diastolic": 94,
  "hba1c": 8.1, "fasting_glucose": 172.0,
  "smoker": false, "alcohol_use": "Social", "exercise_frequency": "1-2x/week",
  "conditions":  [ { "condition": "Malaria", "severity": "Uncomplicated", "diagnosed_date": "…" } ],
  "medications": [ { "medication": "Artemether/Lumefantrine (ACT)", "for_condition": "Malaria",
                     "frequency": "Twice daily", "adherence": "Good" } ],
  "last_visit": "…",
  "risk_score": 38                  // composite 0–100, computed
}
```

**Conditions** are drawn per patient from the country's curated list, with
probability = `base_prob × age_multiplier × ethnicity_adjust` (capped). This
produces realistic epidemiology, e.g.:

- Malaria dominant in Mali/Tanzania/Eritrea; HIV prominent in Tanzania.
- Cancer + cardiovascular high in the older Cuba/Uruguay populations.
- Sickle cell weighted up for Afro-descendant groups, down for others.
- Dengue/Chagas in South America; TB across low-income settings.

**Database schema** (`load_db.py`): three tables — `patients`, `conditions`,
`medications` — all carrying `country`, indexed on it. The app filters every
read with `WHERE country = %s`.

The dataset is **synthetic** (seeded RNG, `random.seed(42)` → reproducible). It
is for analytics/demo purposes and is not real patient data.

---

## Running it

```bash
pip install -r requirements.txt

# 1. Generate the dataset (writes data/patients.json)
python generate_data.py

# 2. (optional) Load into Postgres — needs DATABASE_URL in .env or the environment
python load_db.py

# 3. Run the dashboard
streamlit run app.py
```

- Without `DATABASE_URL`, the app **falls back to `data/patients.json`** (filtered
  by the selected country), so it runs fully offline.
- The AI assistant needs `ANTHROPIC_API_KEY`; without it, only that tab is disabled.

### UI flow

1. **Pick a country** (flagged picker, shows local name).
2. **Language** auto-defaults to the country's primary official language; the
   dropdown offers **that language + English** (English always available for
   English-speaking demo/super users).

### Database configuration (Postgres / Railway)

Credentials live in a **local `.env` file only** — never in the code or this
README (`.env` is gitignored; `.env.example` shows the shape). Create your
`.env` from the example and fill in your own values:

```bash
cp .env.example .env
# then edit .env:
#   DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
#   ANTHROPIC_API_KEY=sk-ant-…
```

`load_db.py` and `app.py` read `DATABASE_URL` from the environment (via
`python-dotenv`). To (re)build the database after generating data:

```bash
python generate_data.py      # writes data/patients.json
python load_db.py            # DROPs & recreates tables, loads all ~9,000 rows
```

> `load_db.py` **drops and recreates** `patients` / `conditions` / `medications`
> every run — it is a full reload, not a migration. Never paste a real
> connection string into a tracked file; if one is ever exposed, rotate the
> database password.

---

## How to add a NEW COUNTRY

Everything is one new file plus a one-line registry edit.

1. **Create `countries/<cc>.py`** (e.g. `gh.py` for Ghana). Copy an existing
   config with a similar profile and edit. `<cc>` should be the **ISO 3166-1
   alpha-2 code** (used for the ID prefix *and* the flag emoji, which is derived
   automatically — no image assets needed).

   Required `CONFIG` keys:

   | Key | What |
   |-----|------|
   | `code` | Country code, e.g. `"GH"`. |
   | `name` / `name_local` | English name / local-language name (shown in picker). |
   | `language` | Primary display language code (`en/pt/es/fr/sw/ti/…`). |
   | `regions` | Real administrative divisions (list). |
   | `ethnicities` | `{group: probability}` (should sum to ~1.0). |
   | `insurance` | `[(payer, weight), …]` — real financing types. |
   | `age_brackets` | `[((lo, hi), weight), …]` — models the age pyramid. |
   | `first_names_male` / `first_names_female` / `last_names` | Curated, ethnolinguistically appropriate. |
   | `conditions` | `{condition_name: {"base_prob": p, "ethnicity_adjust": {grp: mult}}}` — **condition_name must exist in `base.py::CONDITION_LIBRARY`.** |
   | `languages` *(optional)* | Explicit language list for the selector; defaults to `[language]` (English is always appended). |

2. **Register it** in `countries/__init__.py`: add to the `from . import …`
   line and to the `REGISTRY` tuple (registry order = picker order).

3. **Regenerate + reload**: `python generate_data.py` (&& `python load_db.py`).

That's it — the picker, flag, per-country queries, KPIs and charts all pick it
up automatically. **No changes to `app.py`.**

> **Need a condition not yet in the library?** Add it once to
> `CONDITION_LIBRARY` in `countries/base.py` (medications, severity bands,
> `category` for the age curve), then reference it from any country's
> `conditions`. Add its translations to `translations.py::_CONDITIONS`.

---

## How to add a NEW LANGUAGE

1. In `translations.py`, add the code to `LANGUAGES` (display name) and
   `AI_LANGUAGE_NAME` (full name used to instruct the AI which language to
   answer in).
2. Add a block for the code in `_UI` (UI chrome strings). Missing keys fall
   back to English automatically, so you can start partial.
3. Add the language column to `_CONDITIONS`, `_ADHERENCE`, `_GENDER` value
   maps. Missing values fall back to the English value.
4. To make a country default to it, set that country's `language` (and/or
   `languages`).

No `app.py` changes needed — `t()` / `tv()` resolve everything, with graceful
English fallback for anything untranslated.

---

## AI layer — two approaches, side by side

The dashboard ships **two AI tabs** so you can contrast the patterns:

| Tab | File | Pattern |
|-----|------|---------|
| **AI Health Assistant** | `app.py` (tab 5) | Single Anthropic SDK call over a **precomputed static English summary** injected into the system prompt. Simple, cheap, one-shot. |
| **AI Agent (LangGraph)** | `ai_agent.py` (tab 6) | **LangGraph ReAct agent** with typed, read-only **pandas tools**. The agent decides which tools to call, runs them against the live per-country dataframes, and synthesizes an answer. A tool-call trace is shown in an expander. |

Both answer **in the country's language** (English data in, localized prose out).

**Agent tools** (`ai_agent.py::build_agent`) are read-only functions that close
over the selected country's dataframes — so the agent is physically scoped to
one country and cannot mutate anything:

- `condition_prevalence()` · `top_medications(condition?, age_group?, limit)`
- `medication_adherence(condition?)` · `demographics_breakdown(dimension)`
- `risk_summary()` · `comorbidity_pairs(limit)`

**To add a tool:** add a `@tool`-decorated function inside `build_agent()` (it
closes over `dp`/`dm`/`dc`), append it to the `tools` list. Return JSON/text;
keep it read-only. No other file changes.

> Why typed pandas tools instead of open text-to-SQL? No injection surface, no
> way to escape the country scope, deterministic for live demos — while still
> showing genuine multi-step tool use. Extra deps: `langgraph`,
> `langchain-anthropic`, `langchain-core`.

## Design considerations & caveats

- **Language is presentation-only.** Because coded values are stored in English,
  interactive drill-down selectors and the DB queries operate on canonical
  English keys; only display labels are localized. This keeps queries stable and
  the toggle cheap. (Trade-off: a clicked translated chart bar may not
  pre-select its English drill-down — cosmetic.)
- **AI assistant is fully multilingual.** The data summary sent to the model
  stays in English (the model reasons well in English), but the system prompt
  instructs it to answer **entirely in the country's language**, regardless of
  the question's language.
- **Proper nouns are never translated** — names, regions, and drug names render
  as stored. Get them right at *generation* time via the country config.
- **Swahili & Tigrinya need native clinical review.** pt/es/fr translations are
  high-confidence; the Swahili and Ge'ez-script Tigrinya medical terms are
  best-effort and flagged in `translations.py`. Severity bands and drug names
  are intentionally left in clinical English (common in practice).
- **Synthetic data.** Seeded and reproducible; prevalence figures are tuned to
  be *plausible*, not authoritative. Do not use for real epidemiological claims.
- **Caching.** `load_data(country_code)` and `build_data_summary(country_code)`
  are `@st.cache_data` keyed by country, so switching countries recomputes
  correctly. Chat history persists across country switches (session state).
- **Scale.** ~9,000 rows is trivial for Postgres; the `country` indexes keep
  per-country reads fast. Raise `RECORDS_PER_COUNTRY` in `generate_data.py` to
  grow the dataset.
