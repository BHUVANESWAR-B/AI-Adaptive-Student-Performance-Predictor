import pandas as pd

print("Loading processed programming data...")

df = pd.read_csv("data/processed/programming_processed.csv")

# Group by student
grouped = df.groupby("user_id")

sequences = []

for user, group in grouped:
    skills = group["skill_encoded"].tolist()
    correct = group["correct"].tolist()

    sequences.append({
        "user_id": user,
        "skill_sequence": skills,
        "correct_sequence": correct
    })

seq_df = pd.DataFrame(sequences)

seq_df.to_csv("data/processed/programming_sequences.csv", index=False)

print("Programming sequences created successfully ✅")
print("Total students:", len(seq_df))
