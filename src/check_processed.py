import pandas as pd

files = [
    "data/processed/assistments_sequences.csv",
    "data/processed/physics_sequences.csv",
    "data/processed/programming_sequences.csv"
]

for f in files:
    df = pd.read_csv(f)
    print(f, df.shape)
    print(df.head(2), "\n")
