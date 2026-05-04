import pandas as pd
import numpy as np
import ast
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ==========================
# CONFIG
# ==========================

MAX_SEQ_LEN = 100
SUBJECTS = ["math", "physics", "programming"]

os.makedirs("results/plots", exist_ok=True)

# ==========================
# HELPER FUNCTION
# ==========================

def load_test_data(subject):
    path = f"data/eval/{subject}_test.csv"
    df = pd.read_csv(path)

    # Convert string sequences to lists
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

    y = pad_sequences(
        df["correct_sequence"].tolist(),
        maxlen=MAX_SEQ_LEN,
        padding="post",
        truncating="post"
    )

    y = y.flatten()
    return X, y


def evaluate_model(subject, model_type):
    model_path = f"models/{model_type}_{subject}.keras"
    model = load_model(model_path)

    X, y_true = load_test_data(subject)

    y_pred = model.predict(X)
    y_pred = y_pred.flatten()
    y_pred_binary = (y_pred > 0.5).astype(int)

    return y_true, y_pred_binary


def plot_confusion_matrix(y_true, y_pred, subject, model_type):
    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(5,4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title(f"{model_type.upper()} - {subject.capitalize()} Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    save_path = f"results/plots/{model_type}_{subject}_confusion_matrix.png"
    plt.savefig(save_path)
    plt.close()

    print(f"Saved: {save_path}")


# ==========================
# MAIN LOOP
# ==========================

for subject in SUBJECTS:
    print(f"\nGenerating confusion matrices for {subject.upper()}")

    # AKT
    y_true, y_pred = evaluate_model(subject, "akt")
    plot_confusion_matrix(y_true, y_pred, subject, "akt")

    # DKT
    y_true, y_pred = evaluate_model(subject, "dkt")
    plot_confusion_matrix(y_true, y_pred, subject, "dkt")

print("\nAll confusion matrices generated successfully ✅")
