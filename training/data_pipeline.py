import os
import json
import pandas as pd
from sklearn.model_selection import train_test_split


# -----------------------------
# 1. Load Raw Data
# -----------------------------

def load_raw_data(subject):
    path = f"data/raw/{subject}/{subject}.csv"

    if not os.path.exists(path):
        raise FileNotFoundError(f"Raw data not found at {path}")

    # Try UTF-8 first, fallback to latin1 if needed
    try:
        df = pd.read_csv(path)
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin1")

    return df


# -----------------------------
# 2. Standardize Columns
# -----------------------------

def preprocess_data(df, subject):

    if subject == "math":
        df = df[["user_id", "skill_id", "correct", "ms_first_response"]]
        df = df.rename(columns={"ms_first_response": "timestamp"})

    elif subject == "physics":
        df = df[["user_id", "question_id", "correct", "answered_at"]]
        df = df.rename(columns={
            "question_id": "skill_id",
            "answered_at": "timestamp"
        })

    elif subject == "programming":
        df = df[["user", "activity", "result", "timestamp"]]
        df = df.rename(columns={
            "user": "user_id",
            "activity": "skill_id",
            "result": "correct"
        })

        # Convert result column to binary
        df["correct"] = df["correct"].apply(
            lambda x: 1 if str(x).lower() in
            ["1", "true", "correct", "success", "accepted", "yes"]
            else 0
        )

    else:
        raise ValueError("Invalid subject")

    df = df.sort_values(by=["user_id", "timestamp"])

    return df


# -----------------------------
# 3. Encode Skills (Safe JSON)
# -----------------------------

def encode_skills(df):

    unique_skills = df["skill_id"].unique()

    # Convert skill keys to string for safe JSON storage
    skill_mapping = {str(skill): idx for idx, skill in enumerate(unique_skills)}

    # Map skills using string conversion
    df["skill_id"] = df["skill_id"].astype(str).map(skill_mapping)

    os.makedirs("data/processed", exist_ok=True)

    with open("data/processed/skill_mapping.json", "w") as f:
        json.dump(skill_mapping, f)

    return df


# -----------------------------
# 4. Build Sequences Per Student
# -----------------------------

def build_sequences(df):

    sequences = []
    grouped = df.groupby("user_id")

    for user_id, group in grouped:
        skill_seq = group["skill_id"].tolist()
        correct_seq = group["correct"].tolist()

        sequences.append((skill_seq, correct_seq))

    return sequences


# -----------------------------
# 5. Train-Test Split
# -----------------------------

def split_sequences(sequences, test_size=0.2):

    train_seq, test_seq = train_test_split(
        sequences,
        test_size=test_size,
        random_state=42
    )

    return train_seq, test_seq


# -----------------------------
# 6. Save Splits
# -----------------------------

def save_splits(train_seq, test_seq, subject):

    os.makedirs("data/splits", exist_ok=True)

    train_df = pd.DataFrame(train_seq, columns=["skill_sequence", "correct_sequence"])
    test_df = pd.DataFrame(test_seq, columns=["skill_sequence", "correct_sequence"])

    train_df.to_csv(f"data/splits/{subject}_train.csv", index=False)
    test_df.to_csv(f"data/splits/{subject}_test.csv", index=False)

    print(f"{subject} splits saved successfully.")


# -----------------------------
# Run Full Pipeline
# -----------------------------

def run_pipeline(subject):

    print(f"Running pipeline for {subject}...")

    df = load_raw_data(subject)
    df = preprocess_data(df, subject)
    df = encode_skills(df)
    sequences = build_sequences(df)
    train_seq, test_seq = split_sequences(sequences)
    save_splits(train_seq, test_seq, subject)

    print("Pipeline completed successfully.")


# -----------------------------
# CLI Execution
# -----------------------------

if __name__ == "__main__":

    subject = input("Enter subject (math/physics/programming): ").lower().strip()

    if subject not in ["math", "physics", "programming"]:
        print("Invalid subject.")
    else:
        run_pipeline(subject)