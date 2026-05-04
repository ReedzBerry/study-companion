from database import tasks_dao
from database import plans_dao
from database import courses_dao
from datetime import datetime, timedelta

def get_upcoming_tasks():
    """Fetches tasks that are due within the next 7 days."""
    today = datetime.today().date()
    seven_days = (today + timedelta(days=7)).isoformat()
    today_str = today.isoformat()

    all_tasks = tasks_dao.get_all_tasks()

    upcoming = []
    for task in all_tasks:
        due_date = task[3]  #due_date is index 3
        status = task[7]  #status is index 7
        if due_date and today_str <= due_date <= seven_days and status != 'Done':
            upcoming.append(task)

    return upcoming, None

def get_overdue_tasks():
    """Fetches tasks that are past their due date and not marked as done."""
    today = datetime.today().date().isoformat()

    all_tasks = tasks_dao.get_all_tasks()

    overdue = []
    for task in all_tasks:
        due_date = task[3]  #due_date is index 3
        status = task[7]  #status is index 7
        if due_date and due_date < today and status != 'Done':
            overdue.append(task)

    return overdue, None

def get_daily_task_count():
    """Calculates the number of tasks due each day for the next 7 days."""
    today = datetime.today().date()
    workload = { (today + timedelta(days=i)).isoformat(): 0 for i in range(7) }

    all_tasks = tasks_dao.get_all_tasks()

    for task in all_tasks:
        due_date = task[3]  #due_date is index 4
        status = task[7]  #status is index 7
        if due_date and today.isoformat() <= due_date <= (today + timedelta(days=6)).isoformat() and status != 'Done':
            workload[due_date] += 1

    return workload, None

def get_progress_metrics():
    """Calculates the percentage of tasks completed."""

    all_tasks = tasks_dao.get_all_tasks()

    total_tasks = len(all_tasks)
    if total_tasks == 0:
        return {"completed": 0, "total": 0, "percentage": 0, "by_course": []}, None

    completed_tasks = sum(1 for task in all_tasks if task[7] == 'Done')  #status is index 7
    percentage = round((completed_tasks / total_tasks) * 100)

    # Get completion per course

    courses = courses_dao.get_all_courses()
    course_metrics = []
    for course in courses:
        course_id = course[0]  #course_id is index 0
        course_name = course[1]  #course_name is index 1
        course_tasks = [t for t in all_tasks if t[1] == course_id]  #course_id is index 1 in tasks
        total = len(course_tasks)
        completed = sum(1 for t in course_tasks if t[7] == 'Done')  #status is index 7
        course_percentage = round((completed / total) * 100) if total > 0 else 0
        course_metrics.append({
            "course_id": course_id, 
            "course_name": course_name, 
            "completed": completed, 
            "total": total, 
            "percentage": course_percentage
            })

    return {
        "completed": completed_tasks, 
        "total": total_tasks, 
        "percentage": percentage,
        "by_course": course_metrics 
        }, None