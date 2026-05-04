import sqlite3

DB_PATH = "database/edutrace.db"


# --------------------------------------------------
# Database Connection
# --------------------------------------------------
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


# --------------------------------------------------
# Initialize Database Tables
# --------------------------------------------------
def initialize_db():

    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # Quiz results table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        skill TEXT,
        correct INTEGER
    )
    """)

    conn.commit()
    conn.close()


# --------------------------------------------------
# Create Default Admin
# --------------------------------------------------
def create_default_admin():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO users (email, password, role)
    VALUES (?, ?, ?)
    """, ("admin@edutrace.com", "admin123", "admin"))

    conn.commit()
    conn.close()


# --------------------------------------------------
# Register New Student
# --------------------------------------------------
def register_student(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO users (email, password, role)
        VALUES (?, ?, ?)
        """, (email, password, "student"))

        conn.commit()
        conn.close()

        return True

    except:
        conn.close()
        return False


# --------------------------------------------------
# Authenticate User Login
# --------------------------------------------------
def authenticate_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT role FROM users
    WHERE email = ? AND password = ?
    """, (email, password))

    user = cursor.fetchone()

    conn.close()

    if user:
        return user[0]
    else:
        return None


# --------------------------------------------------
# Save Quiz Result
# --------------------------------------------------
def save_quiz_result(user_email, skill, correct):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO quiz_results (user_email, skill, correct)
    VALUES (?, ?, ?)
    """, (user_email, skill, int(correct)))

    conn.commit()
    conn.close()


# --------------------------------------------------
# Get All Quiz Results (Admin)
# --------------------------------------------------
def get_all_results():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT user_email, skill, correct
    FROM quiz_results
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# --------------------------------------------------
# Get Results For Specific Student
# --------------------------------------------------
def get_student_results(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT skill, correct
    FROM quiz_results
    WHERE user_email = ?
    """, (email,))

    rows = cursor.fetchall()

    conn.close()

    return rows


# --------------------------------------------------
# Get System Analytics
# --------------------------------------------------
def get_system_stats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users WHERE role='student'")
    students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM quiz_results")
    attempts = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(correct) FROM quiz_results")
    avg_accuracy = cursor.fetchone()[0]

    conn.close()

    if avg_accuracy is None:
        avg_accuracy = 0

    return {
        "students": students,
        "attempts": attempts,
        "accuracy": round(avg_accuracy * 100, 2)
    }