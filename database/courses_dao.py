import sqlite3
from datetime import datetime
from database.database_setup import get_connection

def create_course(course_name, course_code=None):
    """Insert a new course into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Courses (course_name, course_code, created_at)
        VALUES (?, ?, ?)
        """, (course_name, course_code, datetime.now().isoformat()))
    conn.commit()
    course_id = cursor.lastrowid
    conn.close()
    return course_id

def get_all_courses():
    """ Retrieve all courses from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT course_id, course_name, course_code, created_at
        FROM Courses
        ORDER BY course_name ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_course_by_id(course_id):
    """Retrieve a course by its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT course_id, course_name, course_code, created_at
        FROM Courses
        WHERE course_id = ?           
    """, (course_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_course(course_id, course_name, course_code=None):
    """Update an existing course."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Courses
        SET course_name = ?, course_code = ?
        WHERE course_id = ?
    """, (course_name, course_code, course_id))
    conn.commit()
    conn.close()

def delete_course(course_id):
    """Delete a course by its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM Courses
        WHERE course_id = ?
    """, (course_id,))
    conn.commit()
    conn.close()

    