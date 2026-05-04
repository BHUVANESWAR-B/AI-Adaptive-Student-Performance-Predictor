import pandas as pd

def build_sequences(input_path, output_path, subject_name):
    print(f"\nBuilding sequences for {subject_name}...")

    df = pd.read_csv(input_path)

    print("Original columns:", df.columns)

    # Sort properly by time
    if "order_id" in df.columns:
        df = df.sort_values(by=["user_id", "order_id"])
    elif "answered_at" in df.columns:
        df["answered_at"] = pd.to_datetime(df["answered_at"], errors="coerce")
        df = df.sort_values(by=["user_id", "answered_at"])

    sequence_data = []

    for user_id, group in df.groupby("user_id"):
        skills = group["skill_id"].tolist()
        correct = group["correct"].tolist()

        sequence_data.append({
            "user_id": user_id,
            "skill_sequence": skills,
            "correct_sequence": correct
        })

    sequence_df = pd.DataFrame(sequence_data)
    sequence_df.to_csv(output_path, index=False)

    print(f"{subject_name} sequences created successfully ✅")
    print("Total students:", len(sequence_df))


# -------- MATH (Assistments already done if needed) --------

# -------- PHYSICS --------
build_sequences(
    "data/processed/physics_sequences.csv",
    "data/processed/physics_dkt_sequences.csv",
    "Physics"
)

# -------- PROGRAMMING --------
build_sequences(
    "data/processed/programming_sequences.csv",
    "data/processed/programming_dkt_sequences.csv",
    "Programming"
)

print("\nAll sequence datasets created successfully 🚀")
