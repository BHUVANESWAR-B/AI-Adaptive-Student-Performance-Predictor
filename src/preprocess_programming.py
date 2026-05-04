import pandas as pd
from sklearn.preprocessing import LabelEncoder

print("Loading Programming dataset...")

df = pd.read_csv("data/raw/programming/java_submissions.csv")

print("Original columns:", df.columns)

# Rename columns properly
df = df.rename(columns={
    "user": "user_id",
    "activity": "skill_id"
})

# Convert result to binary
df["correct"] = df["result"].apply(
    lambda x: 1 if str(x).lower().startswith("success") else 0
)

# Encode skill_id
le = LabelEncoder()
df["skill_encoded"] = le.fit_transform(df["skill_id"])

# Sort by user and timestamp
df = df.sort_values(["user_id", "timestamp"])

# Keep only required columns
df = df[["user_id", "skill_encoded", "correct"]]

# Save processed file
df.to_csv("data/processed/programming_processed.csv", index=False)

print("Programming preprocessing complete ✅")
print("\nLabel distribution:")
print(df["correct"].value_counts())
