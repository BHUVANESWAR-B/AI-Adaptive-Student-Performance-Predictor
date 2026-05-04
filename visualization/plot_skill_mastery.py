import matplotlib.pyplot as plt

skills = ["Algebra","Calculus","Probability"]
mastery = [0.92,0.68,0.45]

plt.bar(skills,mastery)

plt.ylabel("Mastery Level")

plt.title("Skill Mastery Distribution")

plt.savefig("results/skill_mastery_distribution.png")

plt.show()