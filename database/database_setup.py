import sqlite3
import os

#define the path to the database file
DB_PATH = os.path.join(os.path.dirname(__file__), 'study_companion.db')

def get_connection():
    """Create and return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON')  # Enable foreign key support
    return conn

def initialise_database():
    """Create all tables if they don't already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Courses Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses(
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            course_code TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL 
            )
        """)
    
    # Tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT NOT NULL,
            priority TEXT NOT NULL,
            estimated_hours INTEGER,
            status TEXT NOT NULL DEFAULT 'Not Started',
            completion_status TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT,
            FOREIGN KEY (course_id) REFERENCES courses(course_id) 
                ON DELETE SET NULL
            )
        """)
    
    # Weekly Plans table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weekly_plans(
            plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            week_start TEXT NOT NULL,
            week_end TEXT NOT NULL,
            created_at TEXT NOT NULL
            )
        """)
    
    # Plans Items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plan_items(
            plan_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            plan_id INTEGER NOT NULL,
            task_id INTEGER NOT NULL,
            scheduled_day TEXT NOT NULL,
            hours_planned REAL,
            FOREIGN KEY (plan_id) REFERENCES Weekly_Plans(plan_id)
                ON DELETE CASCADE,
            FOREIGN KEY (task_id) REFERENCES Tasks(task_id)
                ON DELETE CASCADE
            )
        """)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    initialise_database()


