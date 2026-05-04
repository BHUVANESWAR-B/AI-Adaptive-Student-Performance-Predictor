import pandas as pd

print("Building student-wise DKT sequences...")

df = pd.read_csv("data/processed/combined_sequences.csv")

sequences = df.groupby("user_id").agg({
    "skill_id": list,
    "correct": list
}).reset_index()

sequences.columns = [
    "user_id",
    "skill_sequence",
    "response_sequence"
]

print("Total students:", sequences.shape[0])

sequences.to_csv(
    "data/processed/dkt_sequences.csv",
    index=False
)

print("DKT sequence file created successfully ✅")
