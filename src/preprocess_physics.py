import pandas as pd

print("Preprocessing Physics dataset...")

df = pd.read_csv(
    "data/raw/physics/training.csv",
    encoding="latin1",
    low_memory=False
)

print("Original shape:", df.shape)

# Keep required columns
df = df[['user_id', 'question_id', 'correct', 'answered_at']]

# Drop obvious missing values
df = df.dropna(subset=['user_id', 'question_id', 'correct', 'answered_at'])
print("After initial cleaning:", df.shape)

# SAFE datetime conversion
df['answered_at'] = pd.to_datetime(
    df['answered_at'],
    errors='coerce'
)

# Drop invalid timestamps (like 0000-00-00)
df = df.dropna(subset=['answered_at'])
print("After timestamp fix:", df.shape)

# Sort by user and time
df = df.sort_values(by=['user_id', 'answered_at'])

# Create order_id per user
df['order_id'] = df.groupby('user_id').cumcount() + 1

# Rename for DKT consistency
df = df.rename(columns={'question_id': 'skill_id'})

# Add subject_id (Physics = 1)
df['subject_id'] = 1

# Save processed physics data
df.to_csv(
    "data/processed/physics_sequences.csv",
    index=False
)

print("Physics preprocessing COMPLETED ✅")
