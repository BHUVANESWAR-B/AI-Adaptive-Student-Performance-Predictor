import pandas as pd
from sklearn.model_selection import train_test_split

print("Loading programming sequences...")

df = pd.read_csv("data/processed/programming_sequences.csv")

train_df, test_df = train_test_split(
    df,
    test_size=0.2,
    random_state=42
)

train_df.to_csv("data/eval/programming_train.csv", index=False)
test_df.to_csv("data/eval/programming_test.csv", index=False)

print("Programming Train/Test split completed ✅")
