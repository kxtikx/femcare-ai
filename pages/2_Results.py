import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

from utils.preprocessing import preprocess, FEATURES
from utils.models import get_cluster_profile, query_bayesian, get_risk_level

st.set_page_config(page_title="Your Results", page_icon="🌸", layout="wide")

# ─── Check if user filled form ───────────────────────
if 'user_input' not in st.session_state:
    st.warning("⚠️ Please complete the questionnaire first.")
    if st.button("Go to Questionnaire"):
        st.switch_page("pages/1_Questionnaire.py")
    st.stop()

st.markdown("## 🌸 Your Health Assessment Results")
st.markdown("Based on **GMM Clustering + Bayesian Network + Ensemble AI**")
st.divider()

user_input = st.session_state['user_input']

# ─── Load models ─────────────────────────────────────
try:
    gmm      = joblib.load("models/gmm.pkl")
    ensemble = joblib.load("models/ensemble.pkl")
    bn       = joblib.load("models/bayesian_network.pkl")
    imputer  = joblib.load("models/imputer.pkl")
    scaler   = joblib.load("models/scaler.pkl")
except FileNotFoundError:
    st.error("❌ Models not found! Please run `python train.py` first in your terminal.")
    st.stop()

# ─── Preprocess input ────────────────────────────────
input_df = pd.DataFrame([user_input])
input_df = input_df[[c for c in FEATURES if c in input_df.columns]]
X_input  = imputer.transform(input_df)
X_scaled = scaler.transform(X_input)

# ─── Run all 3 models ────────────────────────────────
cluster_id      = int(gmm.predict(X_scaled)[0])
ensemble_prob   = float(ensemble.predict_proba(X_scaled)[0][1])
bayesian_prob   = query_bayesian(
    bn,
    weight_gain      = user_input['Weight gain(Y/N)'],
    skin_darkening   = user_input['Skin darkening (Y/N)'],
    hair_growth      = user_input['hair growth(Y/N)'],
    pimples          = user_input['Pimples(Y/N)'],
    irregular_cycle  = 1 if user_input['Cycle(R/I)'] == 4 else 0
)

# Combined final score
# Boost score slightly if extra symptoms or family history present
extra  = st.session_state.get('extra_symptom_score', 0)
f_pcos = st.session_state.get('family_pcos', False)
boost  = min(0.10, extra * 0.008 + (0.05 if f_pcos else 0))
final_score = round((ensemble_prob * 0.5) + (bayesian_prob * 0.5) + boost, 3)
final_score = min(1.0, final_score)
risk        = get_risk_level(final_score)
profile     = get_cluster_profile(cluster_id)

# ─── TOP SUMMARY ROW ─────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="background:{risk['bg']};border-radius:16px;padding:1.5rem;
                border:2px solid {risk['color']};text-align:center">
        <h1 style="font-size:3rem;margin:0">{risk['icon']}</h1>
        <h2 style="color:{risk['color']};margin:0.5rem 0">{risk['level']}</h2>
        <p style="color:#6b7280;margin:0">Overall Risk Level</p>
        <h1 style="color:{risk['color']};font-size:2.5rem;margin:0.5rem 0">
            {int(final_score * 100)}%
        </h1>
        <p style="color:#6b7280;font-size:0.85rem">Combined AI Score</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background:#fdf4ff;border-radius:16px;padding:1.5rem;
                border:2px solid #d946ef;text-align:center">
        <h1 style="font-size:2rem;margin:0">{profile['icon']}</h1>
        <h3 style="color:#a21caf;margin:0.5rem 0">{profile['name']}</h3>
        <p style="color:#6b7280;font-size:0.85rem;margin:0">{profile['description']}</p>
        <p style="margin-top:0.75rem;font-size:0.8rem;color:#a21caf">
            <b>GMM Cluster {cluster_id}</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background:#fff7ed;border-radius:16px;padding:1.5rem;
                border:2px solid #fb923c;text-align:center">
        <h1 style="font-size:2rem;margin:0">🧠</h1>
        <h3 style="color:#ea580c;margin:0.5rem 0">Model Breakdown</h3>
        <p style="margin:0.3rem 0;color:#6b7280;font-size:0.85rem">
            Ensemble Model: <b style="color:#ea580c">{int(ensemble_prob*100)}%</b>
        </p>
        <p style="margin:0.3rem 0;color:#6b7280;font-size:0.85rem">
            Bayesian Network: <b style="color:#ea580c">{int(bayesian_prob*100)}%</b>
        </p>
        <p style="margin:0.3rem 0;color:#6b7280;font-size:0.85rem">
            Final Score: <b style="color:#ea580c">{int(final_score*100)}%</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── CHARTS ROW ──────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎯 Risk Score Gauge")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(final_score * 100, 1),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "PCOS Risk Score", 'font': {'size': 16}},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': risk['color']},
            'steps': [
                {'range': [0,  45], 'color': "#dcfce7"},
                {'range': [45, 70], 'color': "#ffedd5"},
                {'range': [70, 100],'color': "#fee2e2"},
            ],
            'threshold': {
                'line': {'color': "black", 'width': 3},
                'thickness': 0.75,
                'value': final_score * 100
            }
        }
    ))
    fig.update_layout(height=280, margin=dict(t=40, b=20, l=20, r=20))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### 📊 Model Comparison")
    fig2 = go.Figure(go.Bar(
        x=['Ensemble Model', 'Bayesian Network', 'Combined Score'],
        y=[
            round(ensemble_prob * 100, 1),
            round(bayesian_prob * 100, 1),
            round(final_score * 100, 1)
        ],
        marker_color=['#ec4899', '#8b5cf6', '#f97316'],
        text=[
            f"{round(ensemble_prob*100,1)}%",
            f"{round(bayesian_prob*100,1)}%",
            f"{round(final_score*100,1)}%"
        ],
        textposition='auto'
    ))
    fig2.update_layout(
        height=280,
        yaxis=dict(range=[0, 100], title="Risk Probability (%)"),
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ─── RECOMMENDATIONS ─────────────────────────────────
st.markdown("### 💊 Personalised Recommendations")

RECOMMENDATIONS = {
    "High Risk": [
        "🏥 Consult a gynaecologist or endocrinologist as soon as possible",
        "🩸 Request hormone panel blood tests (LH, FSH, testosterone, insulin)",
        "🥗 Adopt a low-glycemic index diet to manage insulin resistance",
        "🏃 Aim for 150 minutes of moderate exercise per week",
        "💊 Discuss Metformin or hormonal therapy options with your doctor",
        "😴 Prioritise sleep — hormonal balance is closely tied to sleep quality",
    ],
    "Moderate Risk": [
        "📅 Schedule a routine gynaecological check-up within the next month",
        "🥦 Reduce processed food and sugar intake significantly",
        "🏋️ Start regular physical activity — even 30 min walks help",
        "📊 Track your menstrual cycle using an app for 3 months",
        "🧘 Manage stress — cortisol worsens hormonal imbalance",
        "💧 Stay hydrated and maintain consistent sleep schedule",
    ],
    "Low Risk": [
        "✅ Your indicators look healthy — keep up the good work!",
        "📅 Continue annual gynaecological check-ups",
        "🥗 Maintain a balanced diet rich in fibre and antioxidants",
        "🏃 Stay physically active — at least 3 days a week",
        "📱 Retest every 6 months to monitor any changes",
        "🌿 Avoid smoking and limit alcohol consumption",
    ]
}

recs = RECOMMENDATIONS[risk['level']]
col1, col2 = st.columns(2)
for i, rec in enumerate(recs):
    if i % 2 == 0:
        col1.success(rec)
    else:
        col2.success(rec)

st.divider()

# ─── DISCLAIMER & ACTIONS ────────────────────────────
st.info("⚕️ **Medical Disclaimer:** This is a screening tool only and does not constitute a medical diagnosis. Please consult a qualified gynaecologist for a comprehensive evaluation.")

col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Retake Assessment"):
        del st.session_state['user_input']
        st.switch_page("pages/1_Questionnaire.py")
with col2:
    if st.button("🏥 Find Gynaecologist Near Me"):
        st.markdown("[Click here](https://www.google.com/maps/search/gynaecologist+near+me)", unsafe_allow_html=True)