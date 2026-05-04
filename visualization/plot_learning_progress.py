import matplotlib.pyplot as plt

progress = [10,15,18,17,20,25,30]

plt.plot(progress,marker='o')

plt.xlabel("Quiz Attempts")
plt.ylabel("Score")

plt.title("Learning Progress Trend")

plt.savefig("results/learning_progress.png")

plt.show()