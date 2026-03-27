import sqlite3
from database.database_setup import get_connection
from datetime import datetime

def create_weekly_plan(week_start, week_end):
    """Insert a new weekly plan into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Weekly_Plans (week_start, week_end, created_at)
        VALUES (?, ?, ?)
        """, (week_start, week_end, datetime.now().isoformat()))
    conn.commit()
    plan_id = cursor.lastrowid
    conn.close()
    return plan_id

def get_plan_by_week(week_start):
    """Retrieve a weekly plan by its start date."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT plan_id, week_start, week_end, created_at
        FROM Weekly_Plans
        WHERE  week_start = ?
    """, (week_start,))
    row = cursor.fetchone()
    conn.close()
    return row

def add_plan_item(plan_id, task_id, scheduled_day, hours_planned):
    """Add a task to a weekly plan."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Plan_Items (plan_id, task_id, scheduled_day, hours_planned)
        VALUES (?, ?, ?, ?)
        """, (plan_id, task_id, scheduled_day, hours_planned))
    conn.commit()
    plan_item_id = cursor.lastrowid
    conn.close()
    return plan_item_id

def get_items_by_plan(plan_id):
    """Retrieve all items for a specific weekly plan."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT plan_item_id, plan_id, task_id, scheduled_day, hours_planned
        FROM Plan_Items
        WHERE plan_id = ?
        ORDER BY scheduled_day ASC
    """, (plan_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_items_by_day(plan_id, scheduled_day):
    """Retrieve all items for a specific day in a weekly plan."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT plan_item_id, plan_id, task_id, scheduled_day, hours_planned
        FROM Plan_Items
        WHERE plan_id = ? AND scheduled_day = ?
        ORDER BY scheduled_day ASC
    """, (plan_id, scheduled_day))
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_plan_item(plan_item_id, scheduled_day=None, hours_planned=None):
    """Update an existing plan item."""
    conn = get_connection()
    cursor = conn.cursor()
    if scheduled_day is not None and hours_planned is not None:
        cursor.execute("""
            UPDATE Plan_Items
            SET scheduled_day = ?, hours_planned = ?
            WHERE plan_item_id = ?
        """, (scheduled_day, hours_planned, plan_item_id))
    conn.commit()
    conn.close()

def delete_plan_item(plan_item_id):
    """Delete a plan item by its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM Plan_Items
        WHERE plan_item_id = ?
    """, (plan_item_id,))
    conn.commit()
    conn.close()

def delete_weekly_plan(plan_id):
    """Delete a weekly plan and all its associated items."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM Weekly_Plans
        WHERE plan_id = ?
    """, (plan_id,))
    conn.commit()
    conn.close()