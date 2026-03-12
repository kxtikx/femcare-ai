import streamlit as st

st.set_page_config(
    page_title="FemCare AI",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fdf2f8 0%, #fce7f3 100%);
    }
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    .main-header h1 {
        font-size: 3rem;
        color: #be185d;
        margin-bottom: 0.5rem;
    }
    .main-header p {
        font-size: 1.1rem;
        color: #9d174d;
    }
    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #fbcfe8;
        text-align: center;
        box-shadow: 0 2px 12px rgba(190,24,93,0.07);
    }
    .stButton > button {
        background: linear-gradient(135deg, #ec4899, #be185d);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #be185d, #9d174d);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🌸 FemCare AI</h1>
    <p>Advanced Women's Health Risk Assessment powered by AI</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Feature cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h2>🔵</h2>
        <h3>GMM Clustering</h3>
        <p style="color:#6b7280">Groups your health profile into one of 3 medically relevant clusters</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h2>🟡</h2>
        <h3>Bayesian Network</h3>
        <p style="color:#6b7280">Calculates conditional probability of PCOS based on your symptoms</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h2>🟠</h2>
        <h3>Ensemble Model</h3>
        <p style="color:#6b7280">Combines Random Forest + Gradient Boosting + Logistic Regression</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# CTA
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🌸 Start Health Assessment →"):
        st.switch_page("pages/1_Questionnaire.py")

# Disclaimer
st.markdown("<br>", unsafe_allow_html=True)
st.info("⚕️ **Medical Disclaimer:** FemCare AI is a screening tool only. Results do not constitute a medical diagnosis. Please consult a qualified gynaecologist for professional evaluation.")