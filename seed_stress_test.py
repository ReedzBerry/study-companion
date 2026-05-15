from database.database_setup import get_connection, initialise_database
from datetime import datetime, timedelta
import random

def seed_stress_test():
    """Insert 100+ tasks for stress testing purposes."""
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.today().date()
    now = datetime.now().isoformat()

    # Get existing courses or create some if none exist
    cursor.execute("SELECT course_id, course_name FROM Courses")
    courses = cursor.fetchall()

    if not courses:
        print("No courses found - creating stress test courses first...")
        test_courses = [
            ("Stress Test Course A", "STA101"),
            ("Stress Test Course B", "STB101"),
            ("Stress Test Course C", "STC101"),
        ]
        for name, code in test_courses:
            cursor.execute("""
                INSERT INTO Courses (course_name, course_code, created_at)
                VALUES (?, ?, ?)
            """, (name, code, now))
        conn.commit()
        cursor.execute("SELECT course_id, course_name FROM Courses")
        courses = cursor.fetchall()

    course_ids = [c[0] for c in courses]

    priorities = ["Low", "Medium", "High"]
    statuses = ["Not Started", "In Progress", "Done"]
    descriptions = [
        "Complete all required readings",
        "Submit via the online portal",
        "Review lecture notes before starting",
        "Group collaboration required",
        "Individual assessment",
        "Refer to marking rubric",
        "Check course handbook for details",
        None,
        None,
    ]

    task_names = [
        "Assignment", "Assessment", "Quiz", "Lab Report", "Essay",
        "Presentation", "Research Task", "Practical", "Tutorial Exercise",
        "Reading Summary", "Case Study", "Project Milestone", "Review Task",
        "Portfolio Entry", "Reflection", "Workshop Activity", "Test Prep",
        "Discussion Post", "Peer Review", "Final Exam Prep"
    ]

    print("Inserting 120 stress test tasks...")
    count = 0

    for i in range(1, 121):
        task_name = f"{random.choice(task_names)} {i}"
        course_id = random.choice(course_ids + [None])
        priority = random.choice(priorities)
        status = random.choice(statuses)
        estimated_hours = round(random.uniform(0.5, 12.0) * 2) / 2  # 0.5 increments
        description = random.choice(descriptions)

        # Spread due dates from 30 days ago to 60 days from now
        days_offset = random.randint(-30, 60)
        due_date = (today + timedelta(days=days_offset)).isoformat()

        # If status is Done, set a completion date
        completion_date = None
        if status == "Done":
            completion_date = (today - timedelta(days=random.randint(1, 20))).isoformat()

        cursor.execute("""
            INSERT INTO Tasks (course_id, task_name, task_description, due_date,
            priority, estimated_hours, status, completion_date, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (course_id, task_name, description, due_date,
              priority, estimated_hours, status, completion_date, now))
        count += 1

    conn.commit()
    conn.close()
    print(f"Stress test complete! {count} tasks inserted.")
    print("You can now test the app with a full task load.")
    print("Run seed_data.py to reset back to demo data when done.")

if __name__ == "__main__":
    initialise_database()
    seed_stress_test()