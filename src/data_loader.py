import pandas as pd

datasets = {
    "Math": "data/raw/math/skill_builder_data.csv",
    "Physics": "data/raw/physics/training.csv",
    "Programming": "data/raw/languages/data.csv"
}

for name, path in datasets.items():
    print(f"\nLoading {name} dataset")

    df = pd.read_csv(path, encoding="latin1", low_memory=False)

    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist()[:15])
