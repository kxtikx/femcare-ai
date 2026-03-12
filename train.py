from utils.preprocessing import load_and_clean, preprocess
from utils.models import train_gmm, build_bayesian_network, train_ensemble
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os

print("🚀 Starting FemCare AI Training Pipeline")
print("=" * 50)

# ─── Step 1: Load & preprocess data ──────────────────
print("\n📂 Loading dataset...")
X, y = load_and_clean("data/PCOS_data.csv")
print(f"   Dataset shape: {X.shape}")
print(f"   PCOS cases: {y.sum()} / {len(y)}")

X_scaled = preprocess(X, fit=True)
print("   ✅ Data preprocessed and scaler saved")

# ─── Step 2: Train GMM ───────────────────────────────
print("\n🔵 Training GMM Clustering Model...")
gmm = train_gmm(X_scaled, n_components=3)
labels = gmm.predict(X_scaled)
print(f"   Cluster distribution: {dict(zip(*[list(range(3)), [list(labels).count(i) for i in range(3)]])) }")

# ─── Step 3: Build Bayesian Network ──────────────────
print("\n🟡 Building Bayesian Network...")
bn = build_bayesian_network()

# ─── Step 4: Train Ensemble ──────────────────────────
print("\n🟠 Training Ensemble Model...")
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)
ensemble = train_ensemble(X_train, y_train)

# ─── Step 5: Evaluate ────────────────────────────────
print("\n📊 Ensemble Model Evaluation:")
y_pred = ensemble.predict(X_test)
print(classification_report(y_test, y_pred, target_names=["No PCOS", "PCOS"]))

print("\n" + "=" * 50)
print("✅ All models trained and saved to /models folder")
print("   Run: streamlit run app.py")