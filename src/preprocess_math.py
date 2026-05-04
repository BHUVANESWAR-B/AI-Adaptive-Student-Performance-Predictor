import pandas as pd
from sklearn.preprocessing import LabelEncoder

print("STEP 2: Safe preprocessing started")

# Load dataset
df = pd.read_csv(
    "data/raw/skill_builder_data.csv",
    encoding="latin1",
    low_memory=False
)

print("Initial shape:", df.shape)

# ---- SAFETY CHECK ----
required_cols = ['user_id', 'skill_id', 'correct', 'order_id']
print("Checking required columns...")

for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Missing column: {col}")

print("All required columns found ✅")

# Select required columns
df = df[required_cols]
print("After column selection:", df.shape)

# Drop rows where skill or correct is missing ONLY
df = df.dropna(subset=['skill_id', 'correct'])
print("After dropping null skill/correct:", df.shape)

# Encode skill
le = LabelEncoder()
df['skill_encoded'] = le.fit_transform(df['skill_id'])
print("Skill encoding done")

# Sort by student learning order
df = df.sort_values(by=['user_id', 'order_id'])
print("Sorting done")

# FINAL SAFETY CHECK
if df.empty:
    raise ValueError("DataFrame is EMPTY. Cannot save.")

# Save processed file
df.to_csv("data/processed/assistments_sequences.csv", index=False)
print("STEP 2 COMPLETED ✅ File saved successfully")
