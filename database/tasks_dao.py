import sqlite3
from database.database_setup import get_connection
from datetime import datetime

def create_task(course_id, task_name, due_date=None, task_description=None, priority='Medium', estimated_hours=None, status='Not Started'):
    """Insert a new task into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Tasks (course_id, task_name, due_date, task_description, priority, estimated_hours, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (course_id, task_name, due_date, task_description, priority, estimated_hours, status, datetime.now().isoformat()))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def get_all_tasks():
    """ Retrieve all tasks from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT task_id, course_id, task_name, due_date, 
        task_description, priority, estimated_hours, 
        status, completion_date, created_at, updated_at
        FROM Tasks
        ORDER BY due_date ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_task_by_id(task_id):
    """Retrieve a task by its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT task_id, course_id, task_name, due_date, 
        task_description, priority, estimated_hours, 
        status, completion_date, created_at, updated_at
        FROM Tasks
        WHERE task_id = ?           
    """, (task_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_tasks_by_course(course_id):
    """Retrieve all tasks for a specific course."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT task_id, course_id, task_name, due_date,
        task_description, priority, estimated_hours, 
        status, completion_date, created_at, updated_at
        FROM Tasks
        WHERE course_id = ?
        ORDER BY due_date ASC
    """, (course_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_overdue_tasks():
    """Retrieve all overdue tasks."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT task_id, course_id, task_name, due_date, 
        task_description, priority, estimated_hours, 
        status, completion_date, created_at, updated_at
        FROM Tasks
        WHERE due_date < date('now') AND status != 'Done'
        ORDER BY due_date ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_task(task_id, task_name=None, due_date=None, task_description=None, priority=None, estimated_hours=None, status=None):
    """Update an existing task."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Tasks
        SET task_name = ?, due_date = ?, task_description = ?,
        priority = ?, estimated_hours = ?, status = ?, updated_at = ? 
        WHERE task_id = ?
    """, (task_name, due_date, task_description, priority, estimated_hours, status, datetime.now().isoformat(), task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    """Delete a task by its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM Tasks
        WHERE task_id = ?
    """, (task_id,))
    conn.commit()
    conn.close()

def mark_task_completed(task_id):
    """Mark a task as completed."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Tasks
        SET status = 'Done', completion_date = ?
        WHERE task_id = ?
    """, (datetime.now().isoformat(), task_id,))
    conn.commit()
    conn.close()