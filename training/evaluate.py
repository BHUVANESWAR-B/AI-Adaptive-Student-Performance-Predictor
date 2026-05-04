import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix


# -----------------------------
# Utility Functions
# -----------------------------

def load_test_data(subject):
    """
    Load test dataset for a given subject.
    Expected file: data/splits/{subject}_test.csv
    """
    path = f"data/splits/{subject}_test.csv"

    if not os.path.exists(path):
        raise FileNotFoundError(f"Test file not found at {path}")

    df = pd.read_csv(path)

    # Convert string lists to actual Python lists
    df["skill_sequence"] = df["skill_sequence"].apply(eval)
    df["correct_sequence"] = df["correct_sequence"].apply(eval)

    return df


def load_trained_model(model_type, subject):
    """
    Load trained model.
    Expected path: models/{model_type}/{subject}.keras
    """
    model_path = f"models/{model_type}/{subject}.keras"

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")

    return load_model(model_path)


def plot_confusion_matrix(cm, model_type, subject):
    """
    Save confusion matrix plot
    """
    os.makedirs("results/plots", exist_ok=True)

    plt.figure()
    plt.imshow(cm)
    plt.title(f"{model_type.upper()} - {subject} Confusion Matrix")
    plt.colorbar()

    plt.xticks([0, 1], ["Incorrect", "Correct"])
    plt.yticks([0, 1], ["Incorrect", "Correct"])

    for i in range(2):
        for j in range(2):
            plt.text(j, i, cm[i, j], ha="center", va="center")

    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    save_path = f"results/plots/{model_type}_{subject}_confusion.png"
    plt.savefig(save_path)
    plt.close()

    print(f"Confusion matrix saved to {save_path}")


def save_results(model_type, subject, accuracy, auc):
    """
    Save performance results to CSV
    """
    os.makedirs("results", exist_ok=True)

    result_path = "results/performance_summary.csv"

    result_data = {
        "model": model_type,
        "subject": subject,
        "accuracy": accuracy,
        "auc": auc
    }

    if os.path.exists(result_path):
        df = pd.read_csv(result_path)
        df = pd.concat([df, pd.DataFrame([result_data])], ignore_index=True)
    else:
        df = pd.DataFrame([result_data])

    df.to_csv(result_path, index=False)

    print(f"Results saved to {result_path}")


# -----------------------------
# Main Evaluation Function
# -----------------------------

def evaluate_model(model_type, subject):
    print(f"\nEvaluating {model_type.upper()} model on {subject} dataset...\n")

    # Load test data
    df = load_test_data(subject)

    # Convert to list
    skill_sequences = df["skill_sequence"].tolist()
    correct_sequences = df["correct_sequence"].tolist()

    # Pad sequences to same length
    X_test = pad_sequences(skill_sequences,maxlen=100, padding="post", dtype="int32")
    y_test = pad_sequences(correct_sequences,maxlen=100, padding="post", dtype="int32")

    # Load model
    model = load_trained_model(model_type, subject)

    # Predict
    predictions = model.predict(X_test)

    # Flatten for metrics
    y_true = y_test.flatten()
    y_probs = predictions.flatten()
    y_pred = (y_probs > 0.5).astype(int)

    # Metrics
    accuracy = accuracy_score(y_true, y_pred)
    auc = roc_auc_score(y_true, y_probs)
    cm = confusion_matrix(y_true, y_pred)

    print("Accuracy:", round(accuracy, 4))
    print("AUC:", round(auc, 4))
    print("Confusion Matrix:\n", cm)

    # Save outputs
    plot_confusion_matrix(cm, model_type, subject)
    save_results(model_type, subject, accuracy, auc)

    return accuracy, auc, cm


# -----------------------------
# CLI Execution
# -----------------------------

if __name__ == "__main__":

    print("Model Evaluation Script")
    print("------------------------")

    model_type = input("Enter model type (dkt/akt): ").lower().strip()
    subject = input("Enter subject (math/physics/programming): ").lower().strip()

    if model_type not in ["dkt", "akt"]:
        print("Invalid model type. Choose 'dkt' or 'akt'.")
    elif subject not in ["math", "physics", "programming"]:
        print("Invalid subject.")
    else:
        evaluate_model(model_type, subject)