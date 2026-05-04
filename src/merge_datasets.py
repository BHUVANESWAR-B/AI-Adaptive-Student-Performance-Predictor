import pandas as pd

print("Merging Math, Physics, and Programming datasets...")

math = pd.read_csv("data/processed/assistments_sequences.csv")
physics = pd.read_csv("data/processed/physics_sequences.csv")
programming = pd.read_csv("data/processed/programming_sequences.csv")

combined = pd.concat(
    [math, physics, programming],
    ignore_index=True
)

print("Combined dataset shape:", combined.shape)

combined.to_csv(
    "data/processed/combined_sequences.csv",
    index=False
)

print("Datasets merged successfully ✅")
