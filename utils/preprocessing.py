import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import joblib
import os

# Features we will use from the dataset
FEATURES = [
    'Age (yrs)',
    'BMI',
    'Cycle(R/I)',
    'Cycle length(days)',
    'Marraige Status (Yrs)',
    'No. of aborptions',
    'Skin darkening (Y/N)',
    'hair growth(Y/N)',
    'Weight gain(Y/N)',
    'Fast food (Y/N)',
    'Pimples(Y/N)',
    'Reg.Exercise(Y/N)',
    'BP _Systolic (mmHg)',
    'BP _Diastolic (mmHg)',
    'Pulse rate(bpm)',
    'Waist:Hip Ratio',
    'FSH(mIU/mL)',
    'LH(mIU/mL)',
    'AMH(ng/mL)',
    'RBS(mg/dl)',
]

TARGET = 'PCOS (Y/N)'

def load_and_clean(path="data/PCOS_data.csv"):
    df = pd.read_csv(path)

    # Strip column name whitespace
    df.columns = df.columns.str.strip()

    # Keep only needed columns
    cols = FEATURES + [TARGET]
    df = df[[c for c in cols if c in df.columns]]

    # Convert Y/N columns to 1/0
    yn_cols = [
        'Skin darkening (Y/N)', 'hair growth(Y/N)', 'Weight gain(Y/N)',
        'Fast food (Y/N)', 'Pimples(Y/N)', 'Reg.Exercise(Y/N)'
    ]
    for col in yn_cols:
        if col in df.columns:
            df[col] = df[col].map({'Y': 1, 'N': 0, 1: 1, 0: 0})

    # Drop rows where target is missing
    df = df.dropna(subset=[TARGET])

    # Separate features and target
    X = df[[c for c in FEATURES if c in df.columns]]
    y = df[TARGET].astype(int)

    return X, y

def preprocess(X, fit=False, scaler_path="models/scaler.pkl", imputer_path="models/imputer.pkl"):
    os.makedirs("models", exist_ok=True)

    if fit:
        imputer = SimpleImputer(strategy="median")
        X_imputed = imputer.fit_transform(X)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_imputed)
        joblib.dump(imputer, imputer_path)
        joblib.dump(scaler, scaler_path)
    else:
        imputer = joblib.load(imputer_path)
        scaler = joblib.load(scaler_path)
        X_imputed = imputer.transform(X)
        X_scaled = scaler.transform(X_imputed)

    return X_scaled