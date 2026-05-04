import pandas as pd

print("Building Programming Sequences...")

df = pd.read_csv("data/processed/programming_processed.csv")

# Group by student
grouped = df.groupby("user_id")

sequences = []

for user_id, group in grouped:
    skill_seq = group["skill_encoded"].tolist()
    correct_seq = group["correct"].tolist()

    sequences.append({
        "user_id": user_id,
        "skill_sequence": skill_seq,
        "correct_sequence": correct_seq
    })

seq_df = pd.DataFrame(sequences)

seq_df.to_csv("data/processed/programming_sequences.csv", index=False)

print("Programming sequences built successfully ✅")
print("Total students:", len(seq_df))
