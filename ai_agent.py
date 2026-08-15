"""
LangGraph ReAct agent for the AI Agent tab.

Unlike the simple assistant (a single Anthropic call over a precomputed static
summary), this agent is given typed, READ-ONLY pandas tools and decides for
itself which to call to answer a question. Every tool closes over the currently
selected country's dataframes, so the agent is physically scoped to one country
and cannot mutate anything.

LangChain/LangGraph are imported lazily inside build_agent() so the rest of the
dashboard runs even if those packages aren't installed.
"""

import json

from countries.base import AGE_ORDER, age_group

# Canonical list of the tools the agent is given (order = display order).
# Keep in sync with the @tool functions defined in build_agent(); the UI reads
# this to show users what the agent can query.
AGENT_TOOL_NAMES = [
    "condition_prevalence",
    "top_medications",
    "medication_adherence",
    "demographics_breakdown",
    "risk_summary",
    "comorbidity_pairs",
]


def build_agent(df_patients, df_meds, df_conditions, country_name, answer_language,
                api_key, model="claude-sonnet-4-6"):
    """Construct a LangGraph ReAct agent bound to one country's data.

    Returns the compiled agent (call .invoke({"messages": [...]})).
    Raises ImportError if langgraph / langchain-anthropic are not installed.
    """
    from langchain_core.tools import tool
    from langchain_anthropic import ChatAnthropic
    from langgraph.prebuilt import create_react_agent

    # Defensive copies with an age_group column for grouping.
    dp = df_patients.copy()
    if "age_group" not in dp.columns and not dp.empty:
        dp["age_group"] = dp["age"].apply(age_group)
    dm = df_meds.copy()
    if not dm.empty and "age_group" not in dm.columns:
        dm["age_group"] = dm["age"].apply(age_group)
    dc = df_conditions.copy()
    if not dc.empty and "age_group" not in dc.columns:
        dc["age_group"] = dc["age"].apply(age_group)

    n_patients = len(dp)

    # ----------------------------- TOOLS ----------------------------------
    @tool
    def condition_prevalence() -> str:
        """Prevalence of every medical condition: patient count and % of the population.
        Use for questions about which diseases are most common."""
        if dc.empty:
            return "No condition data."
        out = []
        for cond, count in dc["condition"].value_counts().items():
            out.append({"condition": cond, "patients": int(count),
                        "pct_of_population": round(count / n_patients * 100, 1)})
        return json.dumps(out)

    @tool
    def top_medications(condition: str = None, age_group: str = None, limit: int = 10) -> str:
        """Most-prescribed medications. Optionally filter by condition (e.g. 'Hypertension')
        and/or age_group (one of 18-29, 30-39, 40-49, 50-59, 60-69, 70+). Returns up to `limit`."""
        if dm.empty:
            return "No medication data."
        d = dm
        if condition:
            d = d[d["for_condition"] == condition]
        if age_group:
            d = d[d["age_group"] == age_group]
        if d.empty:
            return "No prescriptions match that filter."
        out = [{"medication": m, "prescriptions": int(c)}
               for m, c in d["medication"].value_counts().head(limit).items()]
        return json.dumps(out)

    @tool
    def medication_adherence(condition: str = None) -> str:
        """Medication adherence breakdown (Good/Moderate/Poor counts and %).
        Optionally scope to one condition to find where adherence is worst."""
        if dm.empty:
            return "No medication data."
        d = dm if not condition else dm[dm["for_condition"] == condition]
        if d.empty:
            return "No prescriptions match that filter."
        total = len(d)
        out = {a: {"count": int(c), "pct": round(c / total * 100, 1)}
               for a, c in d["adherence"].value_counts().items()}
        return json.dumps({"scope": condition or "all", "total_prescriptions": total, "adherence": out})

    @tool
    def demographics_breakdown(dimension: str) -> str:
        """Patient counts by a demographic dimension. `dimension` must be one of:
        age_group, gender, ethnicity, insurance, region."""
        valid = {"age_group", "gender", "ethnicity", "insurance", "region"}
        if dimension not in valid:
            return f"Invalid dimension. Choose one of: {', '.join(sorted(valid))}."
        out = {str(k): int(v) for k, v in dp[dimension].value_counts().items()}
        return json.dumps({"dimension": dimension, "counts": out})

    @tool
    def risk_summary() -> str:
        """Population risk-score summary: average, and counts of high (>60),
        medium (30-60) and low (<30) risk patients."""
        if dp.empty:
            return "No patient data."
        rs = dp["risk_score"]
        return json.dumps({
            "avg_risk": round(float(rs.mean()), 1),
            "high_gt60": int((rs > 60).sum()),
            "medium_30_60": int(((rs >= 30) & (rs <= 60)).sum()),
            "low_lt30": int((rs < 30).sum()),
        })

    @tool
    def comorbidity_pairs(limit: int = 10) -> str:
        """Most common pairs of co-occurring conditions in the same patient (top `limit`)."""
        if dc.empty:
            return "No condition data."
        from collections import Counter
        pairs = Counter()
        for _, conds in dc.groupby("patient_id")["condition"]:
            cs = sorted(set(conds))
            for i in range(len(cs)):
                for j in range(i + 1, len(cs)):
                    pairs[(cs[i], cs[j])] += 1
        out = [{"pair": f"{a} + {b}", "patients": int(c)} for (a, b), c in pairs.most_common(limit)]
        return json.dumps(out)

    tools = [condition_prevalence, top_medications, medication_adherence,
             demographics_breakdown, risk_summary, comorbidity_pairs]

    llm = ChatAnthropic(model=model, api_key=api_key, max_tokens=1500)

    system_prompt = f"""You are a population health analytics agent for {country_name}.
You answer questions about a database of {n_patients} patients using the tools provided.

INSTRUCTIONS:
- ALWAYS use the tools to get real numbers. Never invent statistics.
- Call multiple tools if needed, then synthesize a clear, data-driven answer.
- Respond ONLY in {answer_language}, regardless of the language of the question.
- Focus on medication distribution, prescription patterns, adherence and population risk.
- When relevant, mention {country_name}-specific public-health context and suggest interventions.
- Use headers and bullet points. If the data can't answer the question, say so.
"""

    # The system-prompt kwarg was renamed across LangGraph versions
    # (state_modifier in 0.2.x -> prompt in 0.3+). Support both.
    try:
        return create_react_agent(llm, tools, prompt=system_prompt)
    except TypeError:
        return create_react_agent(llm, tools, state_modifier=system_prompt)
