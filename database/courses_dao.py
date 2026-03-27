import sqlite3
from datetime import datetime
from database.database_setup import get_connection

def create_course(course_name, course_code):
    """Insert a new course into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO courses (course_name, course_code, created_at)
        VALUES (?, ?, ?)
    """, (course_name, course_code, datetime.now().isoformat()))

    conn.commit()
    course_id = cursor.lastrowid
    conn.close()
    return course_id

def get_course_by_id(course_id):
    """Retrieve a course by its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT course_id, course_name, course_code, created_at
        FROM Courses           
           """)