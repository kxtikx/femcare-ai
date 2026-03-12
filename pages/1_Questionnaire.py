import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Health Questionnaire", page_icon="📋", layout="centered")

st.markdown("## 📋 Health Questionnaire")
st.markdown("Please answer all questions honestly. All information is processed locally and kept private.")
st.divider()

# ─── Section 1: Basic Info — OUTSIDE form so BMI updates live ────────────
st.markdown("### 👤 Basic Information")
col1, col2 = st.columns(2)
with col1:
    age    = st.number_input("Age (years)", min_value=12, max_value=60, value=25)
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=150.0, value=60.0, step=0.5)
with col2:
    height       = st.number_input("Height (cm)", min_value=130.0, max_value=200.0, value=158.0, step=0.5)
    marriage_yrs = st.number_input("Years since Marriage (0 if unmarried)", min_value=0, max_value=40, value=0)

# Live BMI calculation
bmi = round(weight / ((height / 100) ** 2), 2)
bmi_label = (
    "🔵 Underweight" if bmi < 18.5 else
    "🟢 Normal"      if bmi < 25   else
    "🟡 Overweight"  if bmi < 30   else
    "🔴 Obese"
)
st.info(f"📊 Your calculated BMI: **{bmi}** — {bmi_label}")

st.divider()

with st.form("health_form"):

    # ─── Section 2: Menstrual Health ─────────────────────────────────────────
    st.markdown("### 🩸 Menstrual Health")
    col1, col2 = st.columns(2)
    with col1:
        cycle_type   = st.selectbox("How would you describe your periods?", [
            "Regular (comes every month on time)",
            "Irregular (unpredictable or skipped months)"
        ])
        cycle_length = st.slider("Average cycle length (days)", min_value=21, max_value=60, value=28)
        abortions    = st.number_input("Number of miscarriages / abortions (if any)", min_value=0, max_value=10, value=0)
    with col2:
        period_pain = st.selectbox("How painful are your periods?", [
            "No pain",
            "Mild pain",
            "Moderate pain",
            "Severe pain — affects daily life"
        ])
        period_flow = st.selectbox("How heavy is your menstrual flow?", [
            "Light",
            "Normal",
            "Heavy",
            "Very heavy with clots"
        ])
        pregnant = st.selectbox("Have you ever been pregnant?", ["No", "Yes"])

    st.divider()

    # ─── Section 3: Physical Symptoms ────────────────────────────────────────
    st.markdown("### 🌡️ Physical Symptoms")
    st.markdown("*Select all that apply to you:*")

    col1, col2 = st.columns(2)
    with col1:
        weight_gain    = st.checkbox("Unexplained weight gain (especially around belly)")
        hair_growth    = st.checkbox("Excess hair growth on face, chest or back")
        hair_loss      = st.checkbox("Hair thinning or loss from scalp")
        skin_darkening = st.checkbox("Skin darkening around neck, armpits or groin")
        pimples        = st.checkbox("Frequent acne / pimples (especially jawline)")
    with col2:
        fatigue        = st.checkbox("Constant tiredness or fatigue")
        mood_swings    = st.checkbox("Frequent mood swings or anxiety")
        bloating       = st.checkbox("Abdominal bloating or discomfort")
        headaches      = st.checkbox("Frequent headaches")
        sleep_issues   = st.checkbox("Difficulty sleeping or insomnia")

    st.divider()

    # ─── Section 4: Lifestyle ─────────────────────────────────────────────────
    st.markdown("### 🏃 Lifestyle & Habits")
    col1, col2 = st.columns(2)
    with col1:
        fast_food  = st.selectbox("How often do you eat fast food / junk food?", [
            "Rarely or never",
            "1–2 times a week",
            "3–4 times a week",
            "Daily"
        ])
        exercise   = st.selectbox("How often do you exercise?", [
            "Never",
            "1–2 times a week",
            "3–4 times a week",
            "Daily"
        ])
        sleep_hrs  = st.slider("Average sleep per night (hours)", min_value=3, max_value=12, value=7)
    with col2:
        stress     = st.selectbox("How would you rate your stress level?", [
            "Low — generally relaxed",
            "Moderate — occasional stress",
            "High — frequently stressed",
            "Very high — constantly overwhelmed"
        ])
        water      = st.selectbox("How much water do you drink daily?", [
            "Less than 1 litre",
            "1–2 litres",
            "2–3 litres",
            "More than 3 litres"
        ])
        smoking    = st.checkbox("Do you smoke?")
        alcohol    = st.checkbox("Do you consume alcohol regularly?")

    st.divider()

    # ─── Section 5: Family History ────────────────────────────────────────────
    st.markdown("### 🧬 Family History")
    col1, col2 = st.columns(2)
    with col1:
        family_pcos     = st.checkbox("Mother or sister has PCOS")
        family_diabetes = st.checkbox("Family history of diabetes")
    with col2:
        family_thyroid  = st.checkbox("Family history of thyroid disorders")
        family_bp       = st.checkbox("Family history of high blood pressure")

    st.divider()
    submitted = st.form_submit_button("🔍 Analyse My Health →")

if submitted:

    # ─── Estimate clinical values from lifestyle answers ──────────────────────

    # Estimate BP from lifestyle factors
    stress_score = {"Low — generally relaxed": 0,
                    "Moderate — occasional stress": 1,
                    "High — frequently stressed": 2,
                    "Very high — constantly overwhelmed": 3}[stress]

    bp_sys_est = int(110 + (bmi - 22) * 0.8 + stress_score * 5 +
                     (5 if family_bp else 0) + (3 if smoking else 0) +
                     (2 if alcohol else 0))
    bp_dia_est = int(70 + (bmi - 22) * 0.5 + stress_score * 3 +
                     (3 if family_bp else 0))
    bp_sys_est = max(90, min(160, bp_sys_est))
    bp_dia_est = max(60, min(110, bp_dia_est))

    # Estimate pulse from exercise level
    exercise_map = {"Never": 82, "1–2 times a week": 76,
                    "3–4 times a week": 70, "Daily": 65}
    pulse_est = exercise_map[exercise] + (3 if stress_score >= 2 else 0)

    # Fast food → binary
    fast_food_bin = 0 if fast_food == "Rarely or never" else 1

    # Exercise → binary
    exercise_bin = 0 if exercise == "Never" else 1

    # Cycle type → binary (2=regular, 4=irregular to match dataset)
    cycle_bin = 2 if "Regular" in cycle_type else 4

    # Extra symptom score for risk boost
    extra_symptom_score = sum([
        fatigue, mood_swings, bloating,
        headaches, sleep_issues, hair_loss,
        smoking, alcohol,
        family_pcos, family_diabetes, family_thyroid
    ])

    # Build input matching model features
    user_input = {
        'Age (yrs)':               age,
        'BMI':                      bmi,
        'Cycle(R/I)':               cycle_bin,
        'Cycle length(days)':       cycle_length,
        'Marraige Status (Yrs)':    marriage_yrs,
        'No. of aborptions':        abortions,
        'Skin darkening (Y/N)':     int(skin_darkening),
        'hair growth(Y/N)':         int(hair_growth),
        'Weight gain(Y/N)':         int(weight_gain),
        'Fast food (Y/N)':          fast_food_bin,
        'Pimples(Y/N)':             int(pimples),
        'Reg.Exercise(Y/N)':        exercise_bin,
        'BP _Systolic (mmHg)':      bp_sys_est,
        'BP _Diastolic (mmHg)':     bp_dia_est,
        'Pulse rate(bpm)':         pulse_est,
        'Waist:Hip Ratio':          round(0.75 + (0.02 if weight_gain else 0) + (0.01 * stress_score), 3),
        'FSH(mIU/mL)':              round(6.5 - (1.5 if cycle_bin == 4 else 0), 2),
        'LH(mIU/mL)':               round(3.5 + (3.5 if cycle_bin == 4 else 0) + (1 if hair_growth else 0), 2),
        'AMH(ng/mL)':               round(2.5 + (3.5 if cycle_bin == 4 else 0) + (1 if weight_gain else 0), 2),
        'RBS(mg/dl)':               round(88 + (family_diabetes * 8) + (fast_food_bin * 5) + (bmi - 22) * 0.5, 1),
    }

    # Save extra context for results page
    st.session_state['user_input']         = user_input
    st.session_state['extra_symptom_score'] = extra_symptom_score
    st.session_state['family_pcos']         = family_pcos
    st.session_state['lifestyle_info'] = {
        'stress': stress, 'sleep_hrs': sleep_hrs,
        'water': water, 'period_pain': period_pain,
        'period_flow': period_flow, 'fatigue': fatigue,
        'mood_swings': mood_swings, 'bloating': bloating,
        'smoking': smoking, 'alcohol': alcohol,
        'family_pcos': family_pcos, 'family_diabetes': family_diabetes,
        'family_thyroid': family_thyroid,
    }

    st.success("✅ Responses saved! Redirecting to results...")
    st.switch_page("pages/2_Results.py")