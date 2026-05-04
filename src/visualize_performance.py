import os
import pandas as pd
import matplotlib.pyplot as plt

# ===============================
# CONFIG
# ===============================

RESULT_FILES = {
    "Math": "results/math_comparison.csv",
    "Physics": "results/physics_comparison.csv",
    "Programming": "results/programming_comparison.csv"
}

os.makedirs("results/plots", exist_ok=True)

subjects = []
akt_acc = []
dkt_acc = []
akt_auc = []
dkt_auc = []

# ===============================
# LOAD RESULTS
# ===============================

for subject, path in RESULT_FILES.items():
    if os.path.exists(path):
        df = pd.read_csv(path)
        subjects.append(subject)
        akt_acc.append(df["AKT_Accuracy"][0])
        dkt_acc.append(df["DKT_Accuracy"][0])
        akt_auc.append(df["AKT_AUC"][0])
        dkt_auc.append(df["DKT_AUC"][0])

# ===============================
# ACCURACY PLOT
# ===============================

plt.figure()
plt.plot(subjects, akt_acc, marker="o")
plt.plot(subjects, dkt_acc, marker="o")
plt.title("AKT vs DKT Accuracy Comparison")
plt.xlabel("Subjects")
plt.ylabel("Accuracy")
plt.legend(["AKT", "DKT"])
plt.savefig("results/plots/accuracy_comparison.png")
plt.close()

# ===============================
# AUC PLOT
# ===============================

plt.figure()
plt.plot(subjects, akt_auc, marker="o")
plt.plot(subjects, dkt_auc, marker="o")
plt.title("AKT vs DKT AUC Comparison")
plt.xlabel("Subjects")
plt.ylabel("AUC")
plt.legend(["AKT", "DKT"])
plt.savefig("results/plots/auc_comparison.png")
plt.close()

print("\nPerformance graphs generated successfully ✅")
print("Saved inside results/plots/")
