import pandas as pd
import numpy as np
import tensorflow as tf
import ast
import os
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ==========================
# CONFIG
# ==========================

MAX_SEQ_LEN = 100
SUBJECTS = ["math", "physics", "programming"]

MODEL_PATHS = {
    "math": "models/akt_math.keras",
    "physics": "models/akt_physics.keras",
    "programming": "models/akt_programming.keras"
}

TEST_PATHS = {
    "math": "data/eval/math_test.csv",
    "physics": "data/eval/physics_test.csv",
    "programming": "data/eval/programming_test.csv"
}

os.makedirs("results/plots", exist_ok=True)

# ==========================
# FUNCTION TO LOAD DATA
# ==========================

def load_sequences(path):
    df = pd.read_csv(path)

    df["skill_sequence"] = df["skill_sequence"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )

    X = pad_sequences(
        df["skill_sequence"].tolist(),
        maxlen=MAX_SEQ_LEN,
        padding="post",
        truncating="post"
    )

    return X

# ==========================
# PLOT STABILITY
# ==========================

plt.figure(figsize=(12, 6))

for subject in SUBJECTS:
    print(f"Processing {subject}...")

    model = load_model(MODEL_PATHS[subject])
    X_test = load_sequences(TEST_PATHS[subject])

    predictions = model.predict(X_test)

    # Average prediction per timestep
    avg_mastery = np.mean(predictions.squeeze(), axis=0)

    plt.plot(avg_mastery, label=subject.capitalize())

plt.title("AKT Stability Comparison Across Subjects")
plt.xlabel("Time Step (Interaction Index)")
plt.ylabel("Average Predicted Mastery")
plt.legend()
plt.grid(True)

plt.savefig("results/plots/stability_all_subjects.png")
plt.show()

print("\nStability comparison graph saved successfully ✅")
