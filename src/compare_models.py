import sys
import os
import ast
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.metrics import accuracy_score, roc_auc_score

# ===============================
# CONFIG
# ===============================

MAX_SEQ_LEN = 100

MODEL_PATHS = {
    "math": {
        "akt": "models/akt_math.keras",
        "dkt": "models/dkt_math.keras"
    },
    "physics": {
        "akt": "models/akt_physics.keras",
        "dkt": "models/dkt_physics.keras"
    },
    "programming": {
        "akt": "models/akt_programming.keras",
        "dkt": "models/dkt_programming.keras"
    }
}

DATA_PATHS = {
    "math": "data/eval/math_test.csv",
    "physics": "data/eval/physics_test.csv",
    "programming": "data/eval/programming_test.csv"
}

# ===============================
# CHECK ARGUMENT
# ===============================

if len(sys.argv) != 2:
    print("Usage: python src/compare_models.py [math|physics|programming]")
    sys.exit(1)

subject = sys.argv[1].lower()

if subject not in MODEL_PATHS:
    print("Invalid subject. Choose from: math, physics, programming")
    sys.exit(1)

# ===============================
# LOAD TEST DATA
# ===============================

print(f"\nLoading {subject.upper()} test data...")

df = pd.read_csv(DATA_PATHS[subject])

# Convert string sequences to list
df["skill_sequence"] = df["skill_sequence"].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
)

df["correct_sequence"] = df["correct_sequence"].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
)

X = pad_sequences(
    df["skill_sequence"].tolist(),
    maxlen=MAX_SEQ_LEN,
    padding="post",
    truncating="post"
)

y_true = pad_sequences(
    df["correct_sequence"].tolist(),
    maxlen=MAX_SEQ_LEN,
    padding="post",
    truncating="post"
)

y_true_flat = y_true.flatten()

# ===============================
# LOAD MODELS
# ===============================

print("Loading AKT model...")
akt_model = load_model(MODEL_PATHS[subject]["akt"])

print("Loading DKT model...")
dkt_model = load_model(MODEL_PATHS[subject]["dkt"])

# ===============================
# PREDICTIONS
# ===============================

print("Running AKT predictions...")
akt_preds = akt_model.predict(X)
akt_preds_flat = akt_preds.flatten()

print("Running DKT predictions...")
dkt_preds = dkt_model.predict(X)
dkt_preds_flat = dkt_preds.flatten()

# Convert probabilities to binary
akt_binary = (akt_preds_flat > 0.5).astype(int)
dkt_binary = (dkt_preds_flat > 0.5).astype(int)

# ===============================
# METRICS
# ===============================

akt_accuracy = accuracy_score(y_true_flat, akt_binary)
dkt_accuracy = accuracy_score(y_true_flat, dkt_binary)

try:
    akt_auc = roc_auc_score(y_true_flat, akt_preds_flat)
except:
    akt_auc = float("nan")

try:
    dkt_auc = roc_auc_score(y_true_flat, dkt_preds_flat)
except:
    dkt_auc = float("nan")

better_model = "AKT" if akt_accuracy > dkt_accuracy else "DKT"

# ===============================
# PRINT RESULTS
# ===============================

print("\n==============================")
print(f" Subject: {subject.upper()}")
print("==============================")
print("AKT Accuracy :", akt_accuracy)
print("DKT Accuracy :", dkt_accuracy)
print("AKT AUC      :", akt_auc)
print("DKT AUC      :", dkt_auc)
print("Better Model :", better_model)

# ===============================
# SAVE RESULTS
# ===============================

os.makedirs("results", exist_ok=True)

df_results = pd.DataFrame([[
    subject.upper(),
    akt_accuracy,
    dkt_accuracy,
    akt_auc,
    dkt_auc,
    better_model
]], columns=[
    "Subject",
    "AKT_Accuracy",
    "DKT_Accuracy",
    "AKT_AUC",
    "DKT_AUC",
    "Better_Model"
])

file_path = f"results/{subject}_comparison.csv"
df_results.to_csv(file_path, index=False)

print(f"\nResults saved to {file_path} ✅")
