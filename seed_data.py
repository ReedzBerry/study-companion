import os
from database.database_setup import get_connection, initialise_database
from datetime import datetime, timedelta

def clear_database():
    """Clear all data from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Plan_Items")
    cursor.execute("DELETE FROM Weekly_Plans")
    cursor.execute("DELETE FROM Tasks")
    cursor.execute("DELETE FROM Courses")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='Courses'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='Tasks'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='Weekly_Plans'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='Plan_Items'")
    conn.commit()
    conn.close()
    print("Database cleared.")

def seed_data():
    """Insert demo data into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.today().date()
    now = datetime.now().isoformat()

    # ── Courses ──────────────────────────────────────────
    courses = [
        ("Web Development and Design", "WDD701"),
        ("Information Technology Project", "BIT701"),
        ("Database Management", "DBM601"),
    ]
    for name, code in courses:
        cursor.execute("""
            INSERT INTO Courses (course_name, course_code, created_at)
            VALUES (?, ?, ?)
        """, (name, code, now))
    conn.commit()

    # Get course IDs
    cursor.execute("SELECT course_id, course_name FROM Courses")
    course_map = {name: cid for cid, name in cursor.fetchall()}

    # ── Tasks ─────────────────────────────────────────────
    # Each task: (course_id, task_name, task_description, due_date, priority, estimated_hours, status)
    tasks = [
        # Overdue tasks
        (
            course_map["Web Development and Design"],
            "Assignment 1 - HTML/CSS",
            "Build a responsive landing page",
            (today - timedelta(days=10)).isoformat(),
            "High", 8, "Not Started"
        ),
        (
            course_map["Database Management"],
            "ER Diagram Submission",
            "Complete the entity relationship diagram",
            (today - timedelta(days=3)).isoformat(),
            "High", 4, "In Progress"
        ),

        # Due this week
        (
            course_map["Information Technology Project"],
            "Project Proposal",
            "Final project proposal document",
            (today + timedelta(days=2)).isoformat(),
            "High", 6, "In Progress"
        ),
        (
            course_map["Web Development and Design"],
            "JavaScript Quiz",
            "Online quiz covering JS fundamentals",
            (today + timedelta(days=4)).isoformat(),
            "Medium", 2, "Not Started"
        ),
        (
            course_map["Database Management"],
            "SQL Lab Exercise",
            "Complete all SQL exercises",
            (today + timedelta(days=5)).isoformat(),
            "Medium", 3, "Not Started"
        ),

        # Due next week
        (
            course_map["Information Technology Project"],
            "Progress Report",
            "Weekly progress update for supervisor",
            (today + timedelta(days=9)).isoformat(),
            "Medium", 4, "Not Started"
        ),
        (
            course_map["Web Development and Design"],
            "Assignment 2 - JavaScript",
            "Build an interactive web application",
            (today + timedelta(days=12)).isoformat(),
            "High", 10, "Not Started"
        ),

        # Completed tasks
        (
            course_map["Database Management"],
            "Database Design Quiz",
            "Multiple choice quiz on database concepts",
            (today - timedelta(days=14)).isoformat(),
            "Low", 2, "Done"
        ),
        (
            course_map["Information Technology Project"],
            "Project Scoping Document",
            "Initial project scope and requirements",
            (today - timedelta(days=7)).isoformat(),
            "High", 5, "Done"
        ),

        # Non-course task
        (
            None,
            "Buy new notebook",
            "For study notes",
            (today + timedelta(days=1)).isoformat(),
            "Low", 0.5, "Not Started"
        ),
    ]

    for course_id, task_name, task_description, due_date, priority, estimated_hours, status in tasks:
        cursor.execute("""
            INSERT INTO Tasks (course_id, task_name, task_description, due_date, 
            priority, estimated_hours, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (course_id, task_name, task_description, due_date, priority, estimated_hours, status, now))
    conn.commit()

    # ── Weekly Plan ───────────────────────────────────────
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    cursor.execute("""
        INSERT INTO Weekly_Plans (week_start, week_end, created_at)
        VALUES (?, ?, ?)
    """, (week_start.isoformat(), week_end.isoformat(), now))
    conn.commit()

    plan_id = cursor.lastrowid

    # Get task IDs
    cursor.execute("SELECT task_id, task_name FROM Tasks")
    task_map = {name: tid for tid, name in cursor.fetchall()}

    # ── Plan Items ────────────────────────────────────────
    plan_items = [
        (plan_id, task_map["Project Proposal"],     "Monday",    3),
        (plan_id, task_map["Project Proposal"],     "Tuesday",   3),
        (plan_id, task_map["JavaScript Quiz"],      "Wednesday", 2),
        (plan_id, task_map["SQL Lab Exercise"],     "Wednesday", 2),
        (plan_id, task_map["SQL Lab Exercise"],     "Thursday",  1),
        (plan_id, task_map["Buy new notebook"],     "Friday",    0.5),
    ]

    for plan_id_, task_id, scheduled_day, hours_planned in plan_items:
        cursor.execute("""
            INSERT INTO Plan_Items (plan_id, task_id, scheduled_day, hours_planned)
            VALUES (?, ?, ?, ?)
        """, (plan_id_, task_id, scheduled_day, hours_planned))
    conn.commit()
    conn.close()

    print("Demo data inserted successfully!")
    print(f"  - {len(courses)} courses")
    print(f"  - {len(tasks)} tasks")
    print(f"  - 1 weekly plan with {len(plan_items)} scheduled items")

if __name__ == "__main__":
    initialise_database()
    clear_database()
    seed_data()