from adaptive_engine import AdaptiveEngine


def run_quiz():

    print("Adaptive Intelligent Tutoring System")
    print("-----------------------------------")

    subject = input("Select subject (math/physics/programming): ").lower().strip()

    if subject not in ["math", "physics", "programming"]:
        print("Invalid subject.")
        return

    engine = AdaptiveEngine(subject)

    question_number = 1

    while True:

        question = engine.select_question()

        if question is None:
            print("\nAll skills mastered or no questions left!")
            break

        print(f"\nQuestion {question_number}")
        print(question["question_text"])
        print("A)", question["option_a"])
        print("B)", question["option_b"])
        print("C)", question["option_c"])
        print("D)", question["option_d"])

        user_answer = input("Your answer (A/B/C/D): ").upper().strip()

        if user_answer not in ["A", "B", "C", "D"]:
            print("Invalid input. Marked incorrect.")
            correct = 0
        else:
            correct = 1 if user_answer == question["correct_option"] else 0

        engine.update_state(question["skill_id"], correct)

        if correct:
            print("Correct!")
        else:
            print("Incorrect.")
            print("Explanation:", question["explanation"])

        question_number += 1

    # 🔥 PERFORMANCE SUMMARY (INSIDE FUNCTION)
    print("\nPerformance Summary")
    print("--------------------")

    summary = engine.get_summary()

    print(f"Overall Mastery: {summary['overall']}%")

    print("\nStrong Skills:")
    for skill in summary["strong"]:
        print("-", skill)

    print("\nModerate Skills:")
    for skill in summary["moderate"]:
        print("-", skill)

    print("\nNeeds Improvement:")
    for skill in summary["weak"]:
        print("-", skill)

    if summary["weak"]:
     print("\nRecommendation:")

     if len(summary["weak"]) == 1:
        print(f"Focus on improving {summary['weak'][0]}.")
     else:
        weak_list = ", ".join(summary["weak"][:-1]) + " and " + summary["weak"][-1]
        print(f"Focus on improving {weak_list}.")

     print("Practice more beginner and intermediate level questions for these topics.")

    elif summary["moderate"]:
     print("\nRecommendation:")
     print("You are doing well. Strengthen moderate skills to reach mastery level.")

    else:
     print("\nExcellent performance! All skills are strong. Try harder problems.")


if __name__ == "__main__":
    run_quiz()