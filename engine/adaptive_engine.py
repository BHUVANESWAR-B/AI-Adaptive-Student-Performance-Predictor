import pandas as pd


class AdaptiveEngine:

    # ------------------------------------------------
    # Initialize Engine
    # ------------------------------------------------
    def __init__(self, subject):

        self.subject = subject

        # Load question bank
        self.question_bank = pd.read_csv(
            f"data/question_bank/{subject}_questions.csv"
        )

        # Track asked questions
        self.asked_questions = set()

        # Skill name mapping
        self.skill_name_map = (
            self.question_bank[["skill_id", "skill_name"]]
            .drop_duplicates()
            .set_index("skill_id")["skill_name"]
            .to_dict()
        )

        # Initialize skill statistics
        self.skill_stats = self.initialize_skills()

    # ------------------------------------------------
    # Initialize Skill Mastery
    # ------------------------------------------------
    def initialize_skills(self):

        skills = self.question_bank["skill_id"].unique()

        skill_stats = {}

        for skill in skills:
            skill_stats[skill] = {
                "attempts": 0,
                "correct": 0,
                "mastery": 0.5,
                "completed": False
            }

        return skill_stats

    # ------------------------------------------------
    # Update Skill Mastery
    # ------------------------------------------------
    def update_mastery(self, skill_id, correct):

        stats = self.skill_stats[skill_id]

        stats["attempts"] += 1
        stats["correct"] += correct

        stats["mastery"] = stats["correct"] / stats["attempts"]

        # Mark skill completed
        if stats["mastery"] >= 0.85 and stats["attempts"] >= 3:
            stats["completed"] = True

    # ------------------------------------------------
    # Select Weakest Skill
    # ------------------------------------------------
    def select_weakest_skill(self):

        incomplete_skills = {
            k: v for k, v in self.skill_stats.items()
            if not v["completed"]
        }

        if not incomplete_skills:
            return None

        return min(incomplete_skills, key=lambda k: incomplete_skills[k]["mastery"])

    # ------------------------------------------------
    # Determine Difficulty (ZPD)
    # ------------------------------------------------
    def determine_difficulty(self, skill_id):

        mastery = self.skill_stats[skill_id]["mastery"]

        if mastery < 0.4:
            return 1
        elif mastery < 0.7:
            return 2
        else:
            return 3

    # ------------------------------------------------
    # Select Question (No repetition)
    # ------------------------------------------------
    def select_question(self):

        skill_id = self.select_weakest_skill()

        if skill_id is None:
            return None

        difficulty = self.determine_difficulty(skill_id)

        available = self.question_bank[
            (self.question_bank["skill_id"] == skill_id) &
            (self.question_bank["difficulty"] == difficulty) &
            (~self.question_bank["question_id"].isin(self.asked_questions))
        ]

        # If no question in difficulty, try any difficulty
        if available.empty:

            available = self.question_bank[
                (self.question_bank["skill_id"] == skill_id) &
                (~self.question_bank["question_id"].isin(self.asked_questions))
            ]

        # If still empty → finished
        if available.empty:
            return None

        question = available.sample(1).iloc[0]

        self.asked_questions.add(question["question_id"])

        return question

    # ------------------------------------------------
    # Update After Student Answer
    # ------------------------------------------------
    def update_state(self, skill_id, correct):

        self.update_mastery(skill_id, correct)

    # ------------------------------------------------
    # Get Current Skill Mastery (Dashboard)
    # ------------------------------------------------
    def get_current_mastery(self):

        mastery = {}

        for skill_id, stats in self.skill_stats.items():

            skill_name = self.skill_name_map.get(skill_id, f"Skill {skill_id}")

            mastery[skill_name] = stats["mastery"]

        return mastery

    # ------------------------------------------------
    # Get Summary for Results Page
    # ------------------------------------------------
    def get_summary(self):

        strong = []
        moderate = []
        weak = []

        total_mastery = 0
        count = 0

        for skill_id, stats in self.skill_stats.items():

            mastery = stats["mastery"]
            skill_name = self.skill_name_map.get(skill_id, f"Skill {skill_id}")

            total_mastery += mastery
            count += 1

            if mastery >= 0.75:
                strong.append(skill_name)

            elif mastery >= 0.4:
                moderate.append(skill_name)

            else:
                weak.append(skill_name)

        overall = round((total_mastery / count) * 100, 2)

        return {
            "strong": strong,
            "moderate": moderate,
            "weak": weak,
            "overall": overall
        }

    # ------------------------------------------------
    # Wrapper used by Quiz Page
    # ------------------------------------------------
    def get_next_question(self):

        return self.select_question()