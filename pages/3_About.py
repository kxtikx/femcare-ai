import streamlit as st

st.set_page_config(page_title="About FemCare AI", page_icon="🌸", layout="wide")

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem 0">
    <h1 style="color:#be185d; font-size:2.8rem">🌸 FemCare AI</h1>
    <p style="font-size:1.1rem; color:#9d174d">
        AI-powered Early Screening for PCOS & Women's Hormonal Health
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─── What is FemCare AI ───────────────────────────────────────────────────────
st.markdown("## 💡 What is FemCare AI?")
st.markdown("""
FemCare AI is an intelligent women's health screening tool that uses a combination of three 
advanced AI models to assess the risk of **PCOS (Polycystic Ovary Syndrome)** and related 
hormonal health conditions.

It is designed to be accessible to **every woman** — no medical background needed. 
Simply answer a few questions about your lifestyle, symptoms and health history, 
and FemCare AI will give you a personalised risk assessment in seconds.
""")

st.divider()

# ─── What is PCOS ─────────────────────────────────────────────────────────────
st.markdown("## 🔬 What is PCOS?")
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    **Polycystic Ovary Syndrome (PCOS)** is one of the most common hormonal disorders 
    affecting women of reproductive age. It affects **1 in 10 women worldwide**.

    PCOS occurs when the ovaries produce excess androgens (male hormones), 
    leading to a range of symptoms that affect fertility, metabolism and overall health.

    **Common symptoms include:**
    - Irregular or missed periods
    - Excess hair growth on face or body (hirsutism)
    - Acne and oily skin
    - Weight gain, especially around the abdomen
    - Thinning hair or hair loss from the scalp
    - Skin darkening around the neck or armpits
    - Difficulty getting pregnant

    **Why early detection matters:**
    PCOS is manageable when caught early. Lifestyle changes alone — 
    diet, exercise and stress management — can significantly reduce symptoms 
    and long-term risks like Type 2 diabetes, heart disease and infertility.
    """)
with col2:
    st.markdown("""
    <div style="background:#fdf2f8;border-radius:16px;padding:1.5rem;
                border:2px solid #f9a8d4;text-align:center;margin-top:1rem">
        <h1>1 in 10</h1>
        <p style="color:#be185d;font-weight:600">Women affected by PCOS worldwide</p>
        <hr style="border-color:#f9a8d4">
        <h1>70%</h1>
        <p style="color:#be185d;font-weight:600">Go undiagnosed for years</p>
        <hr style="border-color:#f9a8d4">
        <h1>Early</h1>
        <p style="color:#be185d;font-weight:600">Detection = Better outcomes</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ─── How it works ─────────────────────────────────────────────────────────────
st.markdown("## ⚙️ How FemCare AI Works")
st.markdown("FemCare AI uses **three AI models working together** for a more reliable result than any single model alone:")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background:white;border-radius:16px;padding:1.5rem;
                border:2px solid #bfdbfe;text-align:center;height:280px">
        <h2>🔵</h2>
        <h3 style="color:#1d4ed8">GMM Clustering</h3>
        <p style="color:#374151;font-size:0.9rem">
            <b>Gaussian Mixture Model</b> groups your health profile 
            into one of 3 medically relevant clusters — 
            Metabolic Risk, Hormonal Imbalance, or Low Risk — 
            based on patterns in your data.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background:white;border-radius:16px;padding:1.5rem;
                border:2px solid #fde68a;text-align:center;height:280px">
        <h2>🟡</h2>
        <h3 style="color:#b45309">Bayesian Network</h3>
        <p style="color:#374151;font-size:0.9rem">
            A <b>probabilistic graphical model</b> that calculates 
            the conditional probability of PCOS based on your 
            symptoms — weight gain, skin darkening, hair growth, 
            acne and cycle irregularity.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background:white;border-radius:16px;padding:1.5rem;
                border:2px solid #fed7aa;text-align:center;height:280px">
        <h2>🟠</h2>
        <h3 style="color:#c2410c">Ensemble Model</h3>
        <p style="color:#374151;font-size:0.9rem">
            Combines <b>Random Forest + Gradient Boosting + 
            Logistic Regression</b> using soft voting to produce 
            a robust, well-rounded prediction that reduces 
            individual model bias.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Final score explanation
st.info("""
**🧮 How the Final Score is Calculated:**
The Ensemble Model and Bayesian Network each contribute **50%** to the final risk score. 
Additional lifestyle factors and family history apply a small boost if relevant risk factors are present.
The final score is mapped to **Low / Moderate / High Risk** using WHO-aligned thresholds.
""")

st.divider()

# ─── Tech Stack ───────────────────────────────────────────────────────────────
st.markdown("## 🛠️ Technology Stack")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div style="background:white;border-radius:12px;padding:1rem;
                border:1px solid #e5e7eb;text-align:center">
        <h3>🐍</h3>
        <b>Python</b>
        <p style="color:#6b7280;font-size:0.8rem">Core language</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style="background:white;border-radius:12px;padding:1rem;
                border:1px solid #e5e7eb;text-align:center">
        <h3>🎈</h3>
        <b>Streamlit</b>
        <p style="color:#6b7280;font-size:0.8rem">Frontend UI</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div style="background:white;border-radius:12px;padding:1rem;
                border:1px solid #e5e7eb;text-align:center">
        <h3>🤖</h3>
        <b>Scikit-learn</b>
        <p style="color:#6b7280;font-size:0.8rem">ML Models</p>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div style="background:white;border-radius:12px;padding:1rem;
                border:1px solid #e5e7eb;text-align:center">
        <h3>🕸️</h3>
        <b>pgmpy</b>
        <p style="color:#6b7280;font-size:0.8rem">Bayesian Network</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ─── Disclaimer ───────────────────────────────────────────────────────────────
st.markdown("## ⚕️ Medical Disclaimer")
st.error("""
**Important:** FemCare AI is a screening and awareness tool only. 
It does **not** provide a medical diagnosis. Results are based on statistical models 
and should not replace professional medical advice.

If you are concerned about your health, please consult a **qualified gynaecologist 
or endocrinologist** for a comprehensive clinical evaluation.
""")

st.divider()



# CTA
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🌸 Take the Health Assessment Now →"):
        st.switch_page("pages/1_Questionnaire.py")