import numpy as np
import joblib
from sklearn.mixture import GaussianMixture
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import warnings
warnings.filterwarnings("ignore")

# ─── GMM ─────────────────────────────────────────────────────────────────────
def train_gmm(X, n_components=3):
    gmm = GaussianMixture(
        n_components=n_components,
        covariance_type='full',
        random_state=42,
        max_iter=200
    )
    gmm.fit(X)
    joblib.dump(gmm, "models/gmm.pkl")
    print(f"✅ GMM trained with {n_components} clusters")
    return gmm

def get_cluster_profile(cluster_id):
    profiles = {
        0: {
            "name": "Metabolic Risk Profile",
            "description": "Indicators suggest metabolic imbalance — watch BMI, diet and blood pressure.",
            "color": "#f97316",
            "icon": "⚠️"
        },
        1: {
            "name": "Hormonal Imbalance Profile",
            "description": "Signs of hormonal irregularity detected — cycle patterns and symptoms suggest hormonal review.",
            "color": "#ef4444",
            "icon": "🔴"
        },
        2: {
            "name": "Low Risk Profile",
            "description": "Your health indicators are largely within normal range. Keep up healthy habits!",
            "color": "#22c55e",
            "icon": "✅"
        }
    }
    return profiles.get(cluster_id, profiles[2])

# ─── Bayesian Network ─────────────────────────────────────────────────────────
def build_bayesian_network():
    """
    Simplified Bayesian Network for women's health risk
    Nodes: WeightGain, SkinDarkening, HairGrowth, Pimples, IrregularCycle → PCOS Risk
    """
    model = BayesianNetwork([
        ('WeightGain',      'PCOSRisk'),
        ('SkinDarkening',   'PCOSRisk'),
        ('HairGrowth',      'PCOSRisk'),
        ('Pimples',         'PCOSRisk'),
        ('IrregularCycle',  'PCOSRisk'),
    ])

    cpd_wg  = TabularCPD('WeightGain',     2, [[0.45], [0.55]])
    cpd_sd  = TabularCPD('SkinDarkening',  2, [[0.60], [0.40]])
    cpd_hg  = TabularCPD('HairGrowth',     2, [[0.55], [0.45]])
    cpd_pm  = TabularCPD('Pimples',        2, [[0.50], [0.50]])
    cpd_ic  = TabularCPD('IrregularCycle', 2, [[0.40], [0.60]])

    # PCOS Risk CPD — 2^5 = 32 combinations
    # Probabilities estimated from medical literature
    pcos_probs = []
    no_pcos_probs = []
    for wg in [0,1]:
        for sd in [0,1]:
            for hg in [0,1]:
                for pm in [0,1]:
                    for ic in [0,1]:
                        score = wg*0.25 + sd*0.20 + hg*0.20 + pm*0.15 + ic*0.20
                        p_pcos = min(0.95, max(0.05, score))
                        pcos_probs.append(p_pcos)
                        no_pcos_probs.append(1 - p_pcos)

    cpd_pcos = TabularCPD(
        variable='PCOSRisk',
        variable_card=2,
        values=[no_pcos_probs, pcos_probs],
        evidence=['WeightGain', 'SkinDarkening', 'HairGrowth', 'Pimples', 'IrregularCycle'],
        evidence_card=[2, 2, 2, 2, 2]
    )

    model.add_cpds(cpd_wg, cpd_sd, cpd_hg, cpd_pm, cpd_ic, cpd_pcos)
    assert model.check_model()
    joblib.dump(model, "models/bayesian_network.pkl")
    print("✅ Bayesian Network built and saved")
    return model

def query_bayesian(model, weight_gain, skin_darkening, hair_growth, pimples, irregular_cycle):
    inference = VariableElimination(model)
    evidence = {
        'WeightGain':      int(weight_gain),
        'SkinDarkening':   int(skin_darkening),
        'HairGrowth':      int(hair_growth),
        'Pimples':         int(pimples),
        'IrregularCycle':  int(irregular_cycle),
    }
    result = inference.query(variables=['PCOSRisk'], evidence=evidence)
    pcos_prob = result.values[1]  # probability of PCOS risk
    return round(float(pcos_prob), 3)

# ─── Ensemble ─────────────────────────────────────────────────────────────────
def train_ensemble(X_train, y_train):
    rf  = RandomForestClassifier(n_estimators=100, random_state=42)
    gb  = GradientBoostingClassifier(n_estimators=100, random_state=42)
    lr  = LogisticRegression(max_iter=1000, random_state=42)

    ensemble = VotingClassifier(
        estimators=[('rf', rf), ('gb', gb), ('lr', lr)],
        voting='soft'
    )
    ensemble.fit(X_train, y_train)
    joblib.dump(ensemble, "models/ensemble.pkl")
    print("✅ Ensemble model trained and saved")
    return ensemble

def get_risk_level(score):
    if score >= 0.70:
        return {"level": "High Risk",    "color": "#ef4444", "bg": "#fef2f2", "icon": "🔴"}
    elif score >= 0.45:
        return {"level": "Moderate Risk","color": "#f97316", "bg": "#fff7ed", "icon": "🟠"}
    else:
        return {"level": "Low Risk",     "color": "#22c55e", "bg": "#f0fdf4", "icon": "🟢"}