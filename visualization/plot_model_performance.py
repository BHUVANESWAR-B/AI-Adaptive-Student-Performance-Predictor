import pandas as pd
import matplotlib.pyplot as plt

# Load model results
df = pd.read_csv("results/performance_summary.csv")

subjects = df["subject"]
accuracy = df["accuracy"]
auc = df["auc"]

plt.figure(figsize=(8,5))

plt.plot(subjects, accuracy, marker="o", label="Accuracy")
plt.plot(subjects, auc, marker="s", label="AUC")

plt.xlabel("Subject")
plt.ylabel("Score")
plt.title("Model Performance Across Subjects")

plt.legend()

plt.savefig("results/model_performance.png")

plt.show()