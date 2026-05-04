import os
import random
import pandas as pd
import math


# -----------------------------
# Utility: Generate Linear Equation
# -----------------------------

def generate_linear(difficulty):

    if difficulty == 1:
        a = random.randint(1, 5)
        x = random.randint(1, 10)
        b = random.randint(1, 10)
        c = a * x + b

        question = f"Solve: {a}x + {b} = {c}"
        correct = x
        explanation = f"Subtract {b} from both sides → {a}x = {c-b}. Divide by {a} → x = {x}"

    elif difficulty == 2:
        a = random.randint(2, 10)
        x = random.randint(-10, 10)
        b = random.randint(-10, 10)
        c = a * x + b

        question = f"Solve: {a}x + ({b}) = {c}"
        correct = x
        explanation = f"Move {b} to right side → {a}x = {c-b}. Divide by {a} → x = {x}"

    else:
        a = random.randint(2, 10)
        b = random.randint(2, 10)
        x = random.randint(-5, 5)
        c = a * (b * x + 3)

        question = f"Solve: {a}({b}x + 3) = {c}"
        correct = x
        explanation = f"Divide by {a} → {b}x + 3 = {c//a}. Subtract 3 → {b}x = {(c//a)-3}. Divide by {b} → x = {x}"

    options = generate_options(correct)

    return question, options, explanation


# -----------------------------
# PHYSICS GENERATORS
# -----------------------------

def generate_kinematics(difficulty):

    u = random.randint(0, 10)
    a = random.randint(1, 5)
    t = random.randint(1, 10)

    v = u + a * t

    question = f"Given u={u} m/s, a={a} m/s², t={t} s. Find final velocity."
    correct = v
    explanation = f"Using v = u + at → v = {u} + {a}×{t} = {v}"

    options = generate_options(correct)

    return question, options, explanation


def generate_newton(difficulty):

    m = random.randint(1, 10)
    a = random.randint(1, 5)

    F = m * a

    question = f"Mass = {m} kg, Acceleration = {a} m/s². Find Force."
    correct = F
    explanation = f"Using F = ma → {m} × {a} = {F}"

    options = generate_options(correct)

    return question, options, explanation


def generate_work(difficulty):

    F = random.randint(1, 20)
    d = random.randint(1, 10)

    W = F * d

    question = f"Force = {F} N, Displacement = {d} m. Find Work."
    correct = W
    explanation = f"Using W = F × d → {F} × {d} = {W} Joules"

    options = generate_options(correct)

    return question, options, explanation


def generate_momentum(difficulty):

    m = random.randint(1, 10)
    v = random.randint(1, 10)

    p = m * v

    question = f"Mass = {m} kg, Velocity = {v} m/s. Find Momentum."
    correct = p
    explanation = f"Using p = mv → {m} × {v} = {p}"

    options = generate_options(correct)

    return question, options, explanation

# -----------------------------
# PROGRAMMING GENERATORS
# -----------------------------

def generate_variables(difficulty):

    x = random.randint(1, 10)
    y = random.randint(1, 10)

    question = f"What is output of: x={x}; y={y}; print(x+y)?"
    correct = x + y
    explanation = f"x+y = {x}+{y} = {correct}"

    options = generate_options(correct)

    return question, options, explanation


def generate_datatypes(difficulty):

    question = "Which data type is: 3.14 ?"
    correct = "float"
    explanation = "3.14 is a floating point number."

    options = ["int", "float", "string", "boolean"]
    random.shuffle(options)
    correct_letter = ["A","B","C","D"][options.index(correct)]

    return question, (options, correct_letter), explanation


def generate_operators(difficulty):

    question = "What is output of: print(2+3*2)?"
    correct = 8
    explanation = "Multiplication first → 3*2=6 → 2+6=8"

    options = generate_options(correct)

    return question, options, explanation


def generate_conditionals(difficulty):

    question = "What is output? if 5>3: print('Yes')"
    correct = "Yes"
    explanation = "5 is greater than 3, so condition is True."

    options = ["Yes", "No", "Error", "Nothing"]
    random.shuffle(options)
    correct_letter = ["A","B","C","D"][options.index(correct)]

    return question, (options, correct_letter), explanation


def generate_loops(difficulty):

    question = "How many times will this run? for i in range(5): print(i)"
    correct = 5
    explanation = "range(5) runs from 0 to 4 → 5 times."

    options = generate_options(correct)

    return question, options, explanation


def generate_functions(difficulty):

    question = "What is output? def f(): return 5\nprint(f())"
    correct = 5
    explanation = "Function returns 5."

    options = generate_options(correct)

    return question, options, explanation


def generate_lists(difficulty):

    question = "What is output? print([1,2,3][1])"
    correct = 2
    explanation = "Index starts at 0. Index 1 → 2."

    options = generate_options(correct)

    return question, options, explanation


def generate_strings(difficulty):

    question = "What is len('AI')?"
    correct = 2
    explanation = "String 'AI' has 2 characters."

    options = generate_options(correct)

    return question, options, explanation


def generate_complexity(difficulty):

    question = "Time complexity of binary search?"
    correct = "O(log n)"
    explanation = "Binary search halves the search space each step."

    options = ["O(n)", "O(log n)", "O(n²)", "O(1)"]
    random.shuffle(options)
    correct_letter = ["A","B","C","D"][options.index(correct)]

    return question, (options, correct_letter), explanation


def generate_oop(difficulty):

    question = "OOP stands for?"
    correct = "Object Oriented Programming"
    explanation = "OOP = Object Oriented Programming."

    options = ["Object Oriented Programming", "Only Object Process",
               "Operational Object Program", "None"]
    random.shuffle(options)
    correct_letter = ["A","B","C","D"][options.index(correct)]

    return question, (options, correct_letter), explanation


# -----------------------------
# Utility: Generate Quadratic
# -----------------------------

def generate_quadratic(difficulty):

    if difficulty == 1:
        x = random.randint(1, 5)
        question = f"Solve: x² - {x*x} = 0"
        correct = x
        explanation = f"x² = {x*x}. So x = ±{x}. Correct answer is {x}."

    elif difficulty == 2:
        r1 = random.randint(1, 5)
        r2 = random.randint(1, 5)
        question = f"One root of x² - {(r1+r2)}x + {(r1*r2)} = 0 is?"
        correct = r1
        explanation = f"Using sum and product of roots. Roots are {r1} and {r2}."

    else:
        a = random.randint(1, 3)
        b = random.randint(1, 5)
        c = random.randint(1, 5)
        question = f"Find discriminant of {a}x² + {b}x + {c}"
        correct = b*b - 4*a*c
        explanation = f"Discriminant D = b² - 4ac = {b}² - 4×{a}×{c} = {correct}"

    options = generate_options(correct)

    return question, options, explanation

# -----------------------------
# Trigonometry Generator
# -----------------------------

def generate_trigonometry(difficulty):

    angles = [0, 30, 45, 60, 90]
    angle = random.choice(angles)

    if difficulty == 1:
        question = f"Find sin({angle}°)"
        correct = round(math.sin(math.radians(angle)), 2)
        explanation = f"Using calculator: sin({angle}) = {correct}"

    elif difficulty == 2:
        question = f"Find cos({angle}°)"
        correct = round(math.cos(math.radians(angle)), 2)
        explanation = f"Using calculator: cos({angle}) = {correct}"

    else:
        question = f"Find tan({angle}°)"
        correct = round(math.tan(math.radians(angle)), 2)
        explanation = f"Using calculator: tan({angle}) = {correct}"

    options = generate_options(correct)

    return question, options, explanation



# -----------------------------
# Probability Generator
# -----------------------------

def generate_probability(difficulty):

    if difficulty == 1:
        question = "Probability of head in fair coin?"
        correct = 0.5
        explanation = "A fair coin has 2 outcomes. Probability = 1/2 = 0.5"

    elif difficulty == 2:
        question = "Probability of even number in dice?"
        correct = 3/6
        explanation = "Even numbers are 2,4,6 → 3 outcomes out of 6 → 3/6"

    else:
        question = "Probability of sum 7 when two dice rolled?"
        correct = 6/36
        explanation = "Total outcomes = 36. Sum 7 occurs 6 times → 6/36"

    correct = round(correct, 2)

    options = generate_options(correct)

    return question, options, explanation


# -----------------------------
# Option Generator
# -----------------------------

def generate_options(correct):

    options = set()
    options.add(correct)

    while len(options) < 4:
        fake = correct + random.randint(-3, 3)
        options.add(fake)

    options = list(options)
    random.shuffle(options)

    correct_option = ["A", "B", "C", "D"][options.index(correct)]

    return options, correct_option


# -----------------------------
# Main Math Question Builder
# -----------------------------

def generate_math_questions():

    questions = []
    question_id = 1

    skill_generators = {
        0: generate_linear,
        1: generate_quadratic,
        3: generate_trigonometry,
        4: generate_probability
    }

    for skill_id, generator in skill_generators.items():

        for difficulty in [1, 1, 2, 2, 3]:

            question_text, (options, correct_letter), explanation = generator(difficulty)

            questions.append({
                "question_id": question_id,
                "subject": "math",
                "skill_id": skill_id,
                "skill_name": "Math Skill",
                "difficulty": difficulty,
                "question_text": question_text,
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_letter,
                "explanation": explanation
            })

            question_id += 1

    df = pd.DataFrame(questions)

    os.makedirs("data/question_bank", exist_ok=True)
    df.to_csv("data/question_bank/math_questions.csv", index=False)

    print("Realistic Math question bank generated.")



def generate_physics_questions():

    questions = []
    question_id = 1

    skill_generators = {
        0: generate_kinematics,
        1: generate_newton,
        2: generate_work,
        3: generate_momentum
    }

    for skill_id, generator in skill_generators.items():

        for difficulty in [1, 1, 2, 2, 3]:

            question_text, (options, correct_letter), explanation = generator(difficulty)

            questions.append({
                "question_id": question_id,
                "subject": "physics",
                "skill_id": skill_id,
                "skill_name": "Physics Skill",
                "difficulty": difficulty,
                "question_text": question_text,
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_letter,
                "explanation": explanation
            })

            question_id += 1

    df = pd.DataFrame(questions)

    os.makedirs("data/question_bank", exist_ok=True)
    df.to_csv("data/question_bank/physics_questions.csv", index=False)

    print("Physics question bank generated.")


def generate_programming_questions():

    questions = []
    question_id = 1

    skill_generators = {
       
        0: ("Variables", generate_variables),
        1: ("Data Types", generate_datatypes),
        2: ("Operators", generate_operators),
        3: ("Conditionals", generate_conditionals),
        4: ("Loops", generate_loops),
        5: ("Functions", generate_functions),
        6: ("Lists", generate_lists),
        7: ("Strings", generate_strings),
        8: ("Time Complexity", generate_complexity),
        9: ("OOP Basics", generate_oop)

    }

    for skill_id, (skill_name, generator) in skill_generators.items():

        for difficulty in [1, 1, 2, 2, 3]:

            question_text, (options, correct_letter), explanation = generator(difficulty)

            questions.append({
                "question_id": question_id,
                "subject": "programming",
                "skill_id": skill_id,
                "skill_name": skill_name,
                "difficulty": difficulty,
                "question_text": question_text,
                "option_a": options[0],
                "option_b": options[1],
                "option_c": options[2],
                "option_d": options[3],
                "correct_option": correct_letter,
                "explanation": explanation
            })

            question_id += 1

    df = pd.DataFrame(questions)

    os.makedirs("data/question_bank", exist_ok=True)
    df.to_csv("data/question_bank/programming_questions.csv", index=False)

    print("Programming question bank generated.")    


if __name__ == "__main__":
    generate_math_questions()
    generate_physics_questions()
    generate_programming_questions()