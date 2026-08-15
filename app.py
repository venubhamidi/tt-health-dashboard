"""
Multi-Country Population Health Dashboard
Focused on Medication Distribution Analytics with a multilingual, tool-using
LangGraph AI agent. Country is selected in the sidebar and drives every query;
display language defaults to each country's primary official language.
"""

import json
import os

from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
import streamlit as st

from countries import REGISTRY, COUNTRY_NAMES
from translations import (
    t, tv, LANGUAGES, AI_LANGUAGE_NAME,
    agent_suggestions, tool_desc,
)

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Population Health Analytics",
    page_icon="++",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

@st.cache_data(ttl=300)
def load_data(country_code):
    db_url = os.environ.get("DATABASE_URL", "")

    if db_url:
        conn = psycopg2.connect(db_url)
        df_patients = pd.read_sql("SELECT * FROM patients WHERE country = %s", conn, params=(country_code,))
        df_meds_raw = pd.read_sql("SELECT * FROM medications WHERE country = %s", conn, params=(country_code,))
        df_conds_raw = pd.read_sql("SELECT * FROM conditions WHERE country = %s", conn, params=(country_code,))
        conn.close()

        # Build condition_list for patient rows
        cond_lists = df_conds_raw.groupby("patient_id")["condition"].apply(
            lambda x: ", ".join(x)
        ).rename("condition_list")
        df_patients = df_patients.merge(cond_lists, on="patient_id", how="left")
        df_patients["condition_list"] = df_patients["condition_list"].fillna("")

        # Join demographics onto medications
        demo_cols = ["patient_id", "age", "gender", "ethnicity", "region", "insurance", "risk_score"]
        df_meds = df_meds_raw.merge(df_patients[demo_cols], on="patient_id", how="left")
        df_conditions = df_conds_raw.merge(
            df_patients[["patient_id", "age", "gender", "ethnicity", "region"]], on="patient_id", how="left"
        )

        # Reconstruct patients_raw list for patient detail view
        patients_raw = []
        for _, row in df_patients.iterrows():
            p = row.to_dict()
            pid = p["patient_id"]
            p["conditions"] = df_conds_raw[df_conds_raw["patient_id"] == pid][
                ["condition", "severity", "diagnosed_date", "subtype"]
            ].to_dict("records")
            p["medications"] = df_meds_raw[df_meds_raw["patient_id"] == pid][
                ["medication", "for_condition", "frequency", "adherence"]
            ].to_dict("records")
            patients_raw.append(p)

        return patients_raw, df_patients, df_meds, df_conditions

    # Fallback to JSON file
    with open("data/patients.json") as f:
        patients = json.load(f)
    patients = [p for p in patients if p.get("country") == country_code]

    rows = []
    for p in patients:
        base = {k: v for k, v in p.items() if k not in ("conditions", "medications")}
        base["num_conditions"] = len(p["conditions"])
        base["num_medications"] = len(p["medications"])
        base["condition_list"] = ", ".join(c["condition"] for c in p["conditions"])
        rows.append(base)
    df_patients = pd.DataFrame(rows)

    med_rows = []
    for p in patients:
        for m in p["medications"]:
            med_rows.append({
                "patient_id": p["patient_id"],
                "age": p["age"],
                "gender": p["gender"],
                "ethnicity": p["ethnicity"],
                "region": p["region"],
                "insurance": p["insurance"],
                "risk_score": p["risk_score"],
                **m,
            })
    df_meds = pd.DataFrame(med_rows)

    cond_rows = []
    for p in patients:
        for c in p["conditions"]:
            cond_rows.append({
                "patient_id": p["patient_id"],
                "age": p["age"],
                "gender": p["gender"],
                "ethnicity": p["ethnicity"],
                "region": p["region"],
                **c,
            })
    df_conditions = pd.DataFrame(cond_rows)

    return patients, df_patients, df_meds, df_conditions


# ---------------------------------------------------------------------------
# Country + language selection (drives every query and all display strings)
# ---------------------------------------------------------------------------
def _flag(code):
    """Regional-indicator flag emoji from a 2-letter ISO country code."""
    return "".join(chr(0x1F1E6 + ord(ch) - ord("A")) for ch in code[:2])

def _country_label(code):
    c = REGISTRY[code]
    label = f"{_flag(code)}  {c['name']}"
    if c["name_local"] != c["name"]:
        label += f" ({c['name_local']})"
    return label

country_code = st.sidebar.selectbox(
    "Country / País / Pays",
    options=list(REGISTRY.keys()),
    format_func=_country_label,
    key="country_select",
)
cfg = REGISTRY[country_code]

# Language options = the country's own language(s) + English (always available
# for English-speaking demo/super users). Defaults to the primary language.
# A country config may declare an explicit "languages" list; otherwise it is
# derived as [primary language, English].
allowed_langs = list(dict.fromkeys(cfg.get("languages", [cfg["language"]]) + ["en"]))
lang = st.sidebar.selectbox(
    t(cfg["language"], "language"),
    options=allowed_langs,
    index=0,  # primary language of the country
    format_func=lambda c: LANGUAGES[c],
    key=f"lang_select_{country_code}",
)

patients_raw, df_patients, df_meds, df_conditions = load_data(country_code)

# Age group helper
def age_group(age):
    if age < 30:
        return "18-29"
    elif age < 40:
        return "30-39"
    elif age < 50:
        return "40-49"
    elif age < 60:
        return "50-59"
    elif age < 70:
        return "60-69"
    else:
        return "70+"

df_patients["age_group"] = df_patients["age"].apply(age_group)
if not df_meds.empty:
    df_meds["age_group"] = df_meds["age"].apply(age_group)
if not df_conditions.empty:
    df_conditions["age_group"] = df_conditions["age"].apply(age_group)

AGE_ORDER = ["18-29", "30-39", "40-49", "50-59", "60-69", "70+"]

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    .block-container { padding-top: 1rem; }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #667eea22, #764ba222);
        border-radius: 10px;
        padding: 15px;
        border-left: 4px solid #667eea;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
        padding: 8px 20px;
    }
    /* Force readable dark text on the light (unselected) tabs, incl. in dark mode */
    .stTabs [data-baseweb="tab"] p {
        color: #262730 !important;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
    }
    .stTabs [aria-selected="true"] p {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
st.sidebar.title(t(lang, "filters"))

selected_regions = st.sidebar.multiselect(
    t(lang, "f_region"), options=sorted(df_patients["region"].unique()), default=[]
)
selected_age_groups = st.sidebar.multiselect(
    t(lang, "f_age"), options=AGE_ORDER, default=[]
)
selected_genders = st.sidebar.multiselect(
    t(lang, "f_gender"), options=["Male", "Female"],
    default=[], format_func=lambda g: tv(lang, g),
)
selected_ethnicities = st.sidebar.multiselect(
    t(lang, "f_ethnicity"), options=sorted(df_patients["ethnicity"].unique()), default=[]
)
selected_insurance = st.sidebar.multiselect(
    t(lang, "f_insurance"), options=sorted(df_patients["insurance"].unique()), default=[]
)

# Apply filters
mask_p = pd.Series(True, index=df_patients.index)
mask_m = pd.Series(True, index=df_meds.index) if not df_meds.empty else pd.Series(dtype=bool)
mask_c = pd.Series(True, index=df_conditions.index) if not df_conditions.empty else pd.Series(dtype=bool)

if selected_regions:
    mask_p &= df_patients["region"].isin(selected_regions)
    if not df_meds.empty:
        mask_m &= df_meds["region"].isin(selected_regions)
    if not df_conditions.empty:
        mask_c &= df_conditions["region"].isin(selected_regions)
if selected_age_groups:
    mask_p &= df_patients["age_group"].isin(selected_age_groups)
    if not df_meds.empty:
        mask_m &= df_meds["age_group"].isin(selected_age_groups)
    if not df_conditions.empty:
        mask_c &= df_conditions["age_group"].isin(selected_age_groups)
if selected_genders:
    mask_p &= df_patients["gender"].isin(selected_genders)
    if not df_meds.empty:
        mask_m &= df_meds["gender"].isin(selected_genders)
    if not df_conditions.empty:
        mask_c &= df_conditions["gender"].isin(selected_genders)
if selected_ethnicities:
    mask_p &= df_patients["ethnicity"].isin(selected_ethnicities)
    if not df_meds.empty:
        mask_m &= df_meds["ethnicity"].isin(selected_ethnicities)
    if not df_conditions.empty:
        mask_c &= df_conditions["ethnicity"].isin(selected_ethnicities)
if selected_insurance:
    mask_p &= df_patients["insurance"].isin(selected_insurance)
    if not df_meds.empty:
        mask_m &= df_meds["insurance"].isin(selected_insurance)

fp = df_patients[mask_p]
fm = df_meds[mask_m] if not df_meds.empty else df_meds
fc = df_conditions[mask_c] if not df_conditions.empty else df_conditions

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title(f"{cfg['name_local']} — {t(lang, 'subtitle')}")
st.caption(f"{t(lang, 'subtitle')} | {len(fp)} {t(lang, 'patient_db')}")

# ---------------------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------------------
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric(t(lang, "kpi_total"), len(fp))
k2.metric(t(lang, "kpi_conditions"), int(fp["num_conditions"].sum()))
k3.metric(t(lang, "kpi_meds"), len(fm))
k4.metric(t(lang, "kpi_avg_risk"), f"{fp['risk_score'].mean():.0f}/100" if len(fp) else "N/A")
k5.metric(t(lang, "kpi_high_risk"), int((fp["risk_score"] > 60).sum()))

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    t(lang, "tab_medication"),
    t(lang, "tab_condition"),
    t(lang, "tab_demographics"),
    t(lang, "tab_explorer"),
    t(lang, "tab_agent"),
])

# ========================== TAB 1: MEDICATION DISTRIBUTION ==================
with tab1:
    st.subheader(t(lang, "sec_med_analysis"))

    if fm.empty:
        st.info("No medication data for the current filter selection.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            med_counts = fm["medication"].value_counts().head(15)
            fig = px.bar(
                x=med_counts.values, y=med_counts.index,
                orientation="h",
                labels={"x": "Prescriptions", "y": "Medication"},
                title="Top 15 Most Prescribed Medications (click a bar to drill down)",
                color=med_counts.values,
                color_continuous_scale="Viridis",
            )
            fig.update_layout(height=500, showlegend=False, yaxis=dict(autorange="reversed"))
            event_med = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="med_chart")

        with col2:
            cond_med = fm.groupby("for_condition")["medication"].count().sort_values(ascending=False)
            fig2 = px.pie(
                names=[tv(lang, c) for c in cond_med.index], values=cond_med.values,
                title="Prescriptions by Condition Category (click a slice to drill down)",
                color_discrete_sequence=px.colors.qualitative.Set2,
            )
            fig2.update_layout(height=500)
            event_cond_pie = st.plotly_chart(fig2, use_container_width=True, on_select="rerun", key="cond_pie_chart")

        # Resolve clicked medication from chart event
        clicked_med = None
        if event_med and event_med.selection and event_med.selection.points:
            point = event_med.selection.points[0]
            clicked_med = point.get("y") or point.get("label")

        # Drill-down: select a medication
        st.markdown("---")
        st.subheader("Medication Drill-Down")

        med_options = sorted(fm["medication"].unique().tolist())
        default_idx = 0
        if clicked_med and clicked_med in med_options:
            default_idx = med_options.index(clicked_med) + 1

        selected_med = st.selectbox(
            "Select a medication to explore (or click a bar above)",
            options=["-- Select --"] + med_options,
            index=default_idx,
        )

        if selected_med != "-- Select --":
            med_data = fm[fm["medication"] == selected_med]

            d1, d2, d3 = st.columns(3)
            d1.metric("Total Prescriptions", len(med_data))
            d2.metric("Unique Patients", med_data["patient_id"].nunique())
            d3.metric("Primary Condition", med_data["for_condition"].mode().iloc[0] if len(med_data) else "N/A")

            dc1, dc2 = st.columns(2)

            with dc1:
                adh = med_data["adherence"].value_counts()
                fig_adh = px.pie(
                    names=adh.index, values=adh.values,
                    title=f"Adherence Rates - {selected_med}",
                    color=adh.index,
                    color_discrete_map={"Good": "#2ecc71", "Moderate": "#f39c12", "Poor": "#e74c3c"},
                )
                st.plotly_chart(fig_adh, use_container_width=True)

            with dc2:
                age_dist = med_data["age_group"].value_counts().reindex(AGE_ORDER).fillna(0)
                fig_age = px.bar(
                    x=age_dist.index, y=age_dist.values,
                    title=f"Age Distribution - {selected_med}",
                    labels={"x": "Age Group", "y": "Prescriptions"},
                    color=age_dist.values,
                    color_continuous_scale="Blues",
                )
                fig_age.update_layout(showlegend=False)
                st.plotly_chart(fig_age, use_container_width=True)

            dc3, dc4 = st.columns(2)

            with dc3:
                gender_dist = med_data["gender"].value_counts()
                fig_gen = px.pie(
                    names=gender_dist.index, values=gender_dist.values,
                    title=f"Gender Split - {selected_med}",
                    color_discrete_sequence=["#3498db", "#e91e8a"],
                )
                st.plotly_chart(fig_gen, use_container_width=True)

            with dc4:
                ins_dist = med_data["insurance"].value_counts()
                fig_ins = px.bar(
                    x=ins_dist.index, y=ins_dist.values,
                    title=f"Insurance Coverage - {selected_med}",
                    labels={"x": "Insurance", "y": "Count"},
                    color=ins_dist.index,
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                )
                fig_ins.update_layout(showlegend=False)
                st.plotly_chart(fig_ins, use_container_width=True)

            # Region breakdown
            region_dist = med_data["region"].value_counts()
            fig_reg = px.bar(
                x=region_dist.index, y=region_dist.values,
                title=f"Regional Distribution - {selected_med}",
                labels={"x": "Region", "y": "Prescriptions"},
                color=region_dist.values,
                color_continuous_scale="Tealgrn",
            )
            fig_reg.update_layout(showlegend=False, xaxis_tickangle=-45)
            st.plotly_chart(fig_reg, use_container_width=True)

        # Medication by age group heatmap
        st.markdown("---")
        st.subheader("Medication x Age Group Heatmap")
        top_meds = fm["medication"].value_counts().head(10).index.tolist()
        heatmap_data = fm[fm["medication"].isin(top_meds)].groupby(
            ["medication", "age_group"]
        ).size().unstack(fill_value=0)
        heatmap_data = heatmap_data.reindex(columns=AGE_ORDER, fill_value=0)

        fig_heat = px.imshow(
            heatmap_data.values,
            x=heatmap_data.columns.tolist(),
            y=heatmap_data.index.tolist(),
            color_continuous_scale="YlOrRd",
            labels=dict(x="Age Group", y="Medication", color="Count"),
            title="Prescription Density: Top 10 Medications by Age Group",
        )
        fig_heat.update_layout(height=450)
        event_heat = st.plotly_chart(fig_heat, use_container_width=True, on_select="rerun", key="heatmap_chart")

        # If user clicks a heatmap cell, show details
        if event_heat and event_heat.selection and event_heat.selection.points:
            hp = event_heat.selection.points[0]
            heat_med = heatmap_data.index[hp.get("y", 0)] if isinstance(hp.get("y"), int) else hp.get("y")
            heat_age = hp.get("x")
            if heat_med and heat_age:
                heat_slice = fm[(fm["medication"] == heat_med) & (fm["age_group"] == heat_age)]
                st.info(f"**{heat_med}** in age group **{heat_age}**: {len(heat_slice)} prescriptions | "
                        f"Adherence - Good: {(heat_slice['adherence']=='Good').sum()}, "
                        f"Moderate: {(heat_slice['adherence']=='Moderate').sum()}, "
                        f"Poor: {(heat_slice['adherence']=='Poor').sum()}")

        # Adherence overview
        st.markdown("---")
        st.subheader("Medication Adherence Overview")

        ac1, ac2 = st.columns(2)
        with ac1:
            overall_adh = fm["adherence"].value_counts()
            fig_oadh = px.pie(
                names=overall_adh.index, values=overall_adh.values,
                title="Overall Medication Adherence",
                color=overall_adh.index,
                color_discrete_map={"Good": "#2ecc71", "Moderate": "#f39c12", "Poor": "#e74c3c"},
            )
            st.plotly_chart(fig_oadh, use_container_width=True)

        with ac2:
            adh_by_cond = fm.groupby(["for_condition", "adherence"]).size().unstack(fill_value=0)
            fig_adh_cond = px.bar(
                adh_by_cond,
                title="Adherence by Condition",
                barmode="group",
                color_discrete_map={"Good": "#2ecc71", "Moderate": "#f39c12", "Poor": "#e74c3c"},
            )
            fig_adh_cond.update_layout(xaxis_tickangle=-30)
            st.plotly_chart(fig_adh_cond, use_container_width=True)


# ========================== TAB 2: CONDITION OVERVIEW =======================
with tab2:
    st.subheader(t(lang, "sec_condition"))

    if fc.empty:
        st.info("No condition data for the current filter selection.")
    else:
        cc1, cc2 = st.columns(2)

        with cc1:
            cond_counts = fc["condition"].value_counts()
            fig_cond = px.bar(
                x=cond_counts.values, y=[tv(lang, c) for c in cond_counts.index],
                orientation="h",
                title="Condition Prevalence (click a bar to drill down)",
                labels={"x": "Patient Count", "y": "Condition"},
                color=cond_counts.values,
                color_continuous_scale="Reds",
            )
            fig_cond.update_layout(height=450, showlegend=False, yaxis=dict(autorange="reversed"))
            event_cond = st.plotly_chart(fig_cond, use_container_width=True, on_select="rerun", key="cond_chart")

        with cc2:
            sev_data = fc.groupby(["condition", "severity"]).size().reset_index(name="count")
            fig_sev = px.sunburst(
                sev_data, path=["condition", "severity"], values="count",
                title="Conditions by Severity (Sunburst)",
                color_discrete_sequence=px.colors.qualitative.Dark2,
            )
            fig_sev.update_layout(height=450)
            st.plotly_chart(fig_sev, use_container_width=True)

        # Resolve clicked condition
        clicked_cond = None
        if event_cond and event_cond.selection and event_cond.selection.points:
            point = event_cond.selection.points[0]
            clicked_cond = point.get("y") or point.get("label")

        # Condition drill-down
        st.markdown("---")
        cond_options = sorted(fc["condition"].unique().tolist())
        default_cond_idx = 0
        if clicked_cond and clicked_cond in cond_options:
            default_cond_idx = cond_options.index(clicked_cond) + 1

        selected_cond = st.selectbox(
            "Select a condition to drill down (or click a bar above)",
            options=["-- Select --"] + cond_options,
            index=default_cond_idx,
        )

        if selected_cond != "-- Select --":
            cond_data = fc[fc["condition"] == selected_cond]

            cd1, cd2, cd3 = st.columns(3)
            with cd1:
                sev = cond_data["severity"].value_counts()
                fig_s = px.pie(names=sev.index, values=sev.values, title="Severity Distribution")
                st.plotly_chart(fig_s, use_container_width=True)
            with cd2:
                age_d = cond_data["age_group"].value_counts().reindex(AGE_ORDER).fillna(0)
                fig_a = px.bar(x=age_d.index, y=age_d.values, title="By Age Group",
                               labels={"x": "Age Group", "y": "Patients"})
                st.plotly_chart(fig_a, use_container_width=True)
            with cd3:
                eth_d = cond_data["ethnicity"].value_counts()
                fig_e = px.pie(names=eth_d.index, values=eth_d.values, title="By Ethnicity")
                st.plotly_chart(fig_e, use_container_width=True)

            # What medications are used for this condition
            if not fm.empty:
                cond_meds = fm[fm["for_condition"] == selected_cond]["medication"].value_counts()
                if not cond_meds.empty:
                    fig_cm = px.bar(
                        x=cond_meds.index, y=cond_meds.values,
                        title=f"Medications Prescribed for {selected_cond}",
                        labels={"x": "Medication", "y": "Prescriptions"},
                        color=cond_meds.values, color_continuous_scale="Purples",
                    )
                    fig_cm.update_layout(showlegend=False, xaxis_tickangle=-30)
                    st.plotly_chart(fig_cm, use_container_width=True)


# ========================== TAB 3: DEMOGRAPHICS ============================
with tab3:
    st.subheader(t(lang, "sec_demographics"))

    dm1, dm2, dm3 = st.columns(3)

    with dm1:
        age_counts = fp["age_group"].value_counts().reindex(AGE_ORDER).fillna(0)
        fig_age = px.bar(
            x=age_counts.index, y=age_counts.values,
            title="Age Distribution",
            labels={"x": "Age Group", "y": "Patients"},
            color=age_counts.values, color_continuous_scale="Blues",
        )
        fig_age.update_layout(showlegend=False)
        st.plotly_chart(fig_age, use_container_width=True)

    with dm2:
        gen_counts = fp["gender"].value_counts()
        fig_gen = px.pie(names=gen_counts.index, values=gen_counts.values, title="Gender Distribution")
        st.plotly_chart(fig_gen, use_container_width=True)

    with dm3:
        eth_counts = fp["ethnicity"].value_counts()
        fig_eth = px.pie(names=eth_counts.index, values=eth_counts.values, title="Ethnicity Distribution")
        st.plotly_chart(fig_eth, use_container_width=True)

    st.markdown("---")

    lf1, lf2, lf3 = st.columns(3)

    with lf1:
        smoke = fp["smoker"].value_counts().rename({True: "Smoker", False: "Non-Smoker"})
        fig_sm = px.pie(names=smoke.index, values=smoke.values, title="Smoking Status",
                        color_discrete_sequence=["#e74c3c", "#2ecc71"])
        st.plotly_chart(fig_sm, use_container_width=True)

    with lf2:
        alc = fp["alcohol_use"].value_counts()
        fig_al = px.bar(x=alc.index, y=alc.values, title="Alcohol Use",
                        labels={"x": "Level", "y": "Patients"},
                        color=alc.index, color_discrete_sequence=px.colors.qualitative.Set3)
        fig_al.update_layout(showlegend=False)
        st.plotly_chart(fig_al, use_container_width=True)

    with lf3:
        ex = fp["exercise_frequency"].value_counts()
        fig_ex = px.bar(x=ex.index, y=ex.values, title="Exercise Frequency",
                        labels={"x": "Frequency", "y": "Patients"},
                        color=ex.index, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_ex.update_layout(showlegend=False)
        st.plotly_chart(fig_ex, use_container_width=True)

    # Risk distribution
    st.markdown("---")
    st.subheader("Risk Score Distribution")
    fig_risk = px.histogram(
        fp, x="risk_score", nbins=20,
        title="Patient Risk Score Distribution",
        labels={"risk_score": "Risk Score", "count": "Patients"},
        color_discrete_sequence=["#667eea"],
    )
    fig_risk.add_vrect(x0=60, x1=100, fillcolor="red", opacity=0.08, annotation_text="High Risk")
    fig_risk.add_vrect(x0=30, x1=60, fillcolor="orange", opacity=0.06, annotation_text="Medium Risk")
    st.plotly_chart(fig_risk, use_container_width=True)

    # Insurance
    ins_counts = fp["insurance"].value_counts()
    fig_ins = px.pie(names=ins_counts.index, values=ins_counts.values,
                     title="Insurance Coverage Distribution",
                     color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(fig_ins, use_container_width=True)


# ========================== TAB 4: PATIENT EXPLORER ========================
with tab4:
    st.subheader(t(lang, "sec_explorer"))

    risk_filter = st.select_slider(
        "Risk Score Range",
        options=list(range(0, 101)),
        value=(0, 100),
    )

    cond_filter = st.multiselect(
        "Filter by Condition",
        options=sorted(df_conditions["condition"].unique()) if not df_conditions.empty else [],
        default=[],
    )

    explorer_df = fp[
        (fp["risk_score"] >= risk_filter[0]) & (fp["risk_score"] <= risk_filter[1])
    ]

    if cond_filter:
        patients_with_cond = fc[fc["condition"].isin(cond_filter)]["patient_id"].unique()
        explorer_df = explorer_df[explorer_df["patient_id"].isin(patients_with_cond)]

    display_cols = [
        "patient_id", "first_name", "last_name", "age", "gender", "ethnicity",
        "region", "bmi", "blood_pressure", "hba1c", "risk_score",
        "num_conditions", "num_medications", "condition_list", "insurance",
    ]
    st.dataframe(
        explorer_df[display_cols].sort_values("risk_score", ascending=False),
        use_container_width=True,
        height=500,
    )

    # Patient detail card
    st.markdown("---")
    selected_pid = st.selectbox(
        "Select a patient for detail view",
        options=["-- Select --"] + explorer_df["patient_id"].tolist(),
    )

    if selected_pid != "-- Select --":
        patient = next(p for p in patients_raw if p["patient_id"] == selected_pid)

        pc1, pc2 = st.columns(2)
        with pc1:
            st.markdown(f"### {patient['first_name']} {patient['last_name']}")
            st.markdown(f"**ID:** {patient['patient_id']}")
            st.markdown(f"**Age:** {patient['age']} | **Gender:** {patient['gender']}")
            st.markdown(f"**Ethnicity:** {patient['ethnicity']}")
            st.markdown(f"**Region:** {patient['region']}")
            st.markdown(f"**Insurance:** {patient['insurance']}")
            st.markdown(f"**Last Visit:** {patient['last_visit']}")

        with pc2:
            st.markdown("### Vitals")
            v1, v2, v3 = st.columns(3)
            v1.metric("BMI", patient["bmi"])
            v2.metric("BP", patient["blood_pressure"])
            v3.metric("HbA1c", patient["hba1c"])
            st.metric("Risk Score", f"{patient['risk_score']}/100")
            st.markdown(f"**Smoker:** {'Yes' if patient['smoker'] else 'No'} | "
                        f"**Alcohol:** {patient['alcohol_use']} | "
                        f"**Exercise:** {patient['exercise_frequency']}")

        if patient["conditions"]:
            st.markdown("#### Conditions")
            cond_df = pd.DataFrame(patient["conditions"])
            st.dataframe(cond_df, use_container_width=True)

        if patient["medications"]:
            st.markdown("#### Medications")
            med_df = pd.DataFrame(patient["medications"])
            st.dataframe(med_df, use_container_width=True)


# ========================== TAB 5: AI AGENT (LANGGRAPH) ====================
with tab5:
    st.subheader(t(lang, "tab_agent"))
    st.caption(t(lang, "agent_caption"))

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        st.error(t(lang, "ai_no_key"))
    else:
        try:
            from ai_agent import build_agent, AGENT_TOOL_NAMES
        except ImportError:
            st.warning(t(lang, "agent_not_installed"))
        else:
            # Show the tools the agent can call (its live-data capabilities).
            with st.expander(f"🧰 {t(lang, 'agent_tools_header')}"):
                for name in AGENT_TOOL_NAMES:
                    st.markdown(f"- **`{name}`** — {tool_desc(lang, name)}")

            # Separate chat history from the simple assistant. Stored as plain
            # (role, text) turns; tool traffic is not replayed across turns.
            if "agent_messages" not in st.session_state:
                st.session_state.agent_messages = []

            # Clickable example questions (localized). A click sets the prompt.
            example_clicked = None
            st.markdown(f"**{t(lang, 'agent_examples')}**")
            for i, ex in enumerate(agent_suggestions(lang)):
                if st.button(ex, key=f"agent_ex_{i}", use_container_width=True):
                    example_clicked = ex

            for msg in st.session_state.agent_messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            typed = st.chat_input(t(lang, "ai_placeholder"), key="agent_input")
            if prompt := (example_clicked or typed):
                st.session_state.agent_messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    with st.spinner(t(lang, "ai_analyzing")):
                        agent = build_agent(
                            df_patients, df_meds, df_conditions,
                            cfg["name"], AI_LANGUAGE_NAME.get(lang, "English"), api_key,
                        )
                        history = [(m["role"], m["content"]) for m in st.session_state.agent_messages]
                        result = agent.invoke({"messages": history})
                        out_messages = result["messages"]

                        # Collect the tool calls the agent made, for a demo trace.
                        tool_calls = []
                        for m in out_messages:
                            for tc in getattr(m, "tool_calls", None) or []:
                                tool_calls.append(f"{tc['name']}({', '.join(f'{k}={v}' for k, v in (tc.get('args') or {}).items())})")

                        # Final answer = content of the last message.
                        final = out_messages[-1].content
                        if isinstance(final, list):
                            final = "".join(b.get("text", "") for b in final if isinstance(b, dict))

                        if tool_calls:
                            with st.expander(f"🔧 {t(lang, 'agent_steps')}"):
                                for i, call in enumerate(tool_calls, 1):
                                    st.markdown(f"{i}. `{call}`")

                        st.markdown(final)
                        st.session_state.agent_messages.append({"role": "assistant", "content": final})
