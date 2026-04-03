from database import tasks_dao
from database import courses_dao

def create_task(course_id, task_name, due_date=None, task_description=None, priority='Medium', estimated_hours=None, status='Not Started'):
    """Validate and create a new task."""
    # Validate task name
    if not task_name or not task_name.strip():
        return None, "Task name cannot be empty."
    if len(task_name.strip()) > 250:
        return None, "Task name cannot exceed 250 characters."
    
    # Validate due date
    if not due_date:
        return None, "Due date is required."
    
    # Validate priority
    valid_priorities = ["Low", "Medium", "High"]
    if priority not in valid_priorities:
        return None, "Priority must be one of: Low, Medium, High."
    
    # Validate estimated hours
    if estimated_hours is not None and estimated_hours < 0:
        return None, "Estimated hours cannot be negative."
    
    # Validate status
    valid_statuses = ["Not Started", "In Progress", "Done"]
    if status not in valid_statuses:
        return None, "Status must be one of: Not Started, In Progress, Done."
    
    # Validate course ID if provided
    if course_id is not None:
        existing_course = courses_dao.get_course_by_id(course_id)
        if not existing_course:
            return None, "Course ID does not exist."
        
    # clean up whitespace
    task_name = task_name.strip()
    task_description = task_description.strip() if task_description else None

    task_id = tasks_dao.create_task(course_id, task_name, due_date, task_description, priority, estimated_hours, status)
    return task_id, None

def get_all_tasks():
    """Retrieve all tasks."""
    return tasks_dao.get_all_tasks()

def get_task_by_id(task_id):
    """Retrieve a task by its ID."""
    if not task_id:
        return None, "Task ID is required."
    task = tasks_dao.get_task_by_id(task_id)
    if not task:
        return None, "Task not found."
    return task, None

def get_tasks_by_course(course_id):
    """Retrieve all tasks associated with a specific course."""
    if not course_id:
        return None, "Course ID is required."
    existing_course = courses_dao.get_course_by_id(course_id)
    if not existing_course:
        return None, "Course ID does not exist."
    return tasks_dao.get_tasks_by_course(course_id), None

def get_overdue_tasks():
    """Retrieve all overdue tasks."""
    return tasks_dao.get_overdue_tasks()

def update_task(task_id, task_name=None, due_date=None, task_description=None, priority=None, estimated_hours=None,  status=None):
    """Validate and update an existing task."""
    if not task_id:
        return False, "Task ID is required."
    
    existing_task = tasks_dao.get_task_by_id(task_id)
    if not existing_task:
        return False, "Task not found."
    
    # Validate task name
    if task_name is not None:
        if not task_name.strip():
            return False, "Task name cannot be empty."
        if len(task_name.strip()) > 250:
            return False, "Task name cannot exceed 250 characters."
    
    # Validate due date
    if due_date is not None and not due_date:
        return False, "Due date is required."
    
    # Validate priority
    valid_priorities = ["Low", "Medium", "High"]
    if priority is not None and priority not in valid_priorities:
        return False, "Priority must be one of: Low, Medium, High."
    
    # Validate estimated hours
    if estimated_hours is not None and estimated_hours < 0:
        return False, "Estimated hours cannot be negative."
    
    # Validate status
    valid_statuses = ["Not Started", "In Progress", "Done"]
    if status is not None and status not in valid_statuses:
        return False, "Status must be one of: Not Started, In Progress, Done."
        
    # clean up whitespace
    task_name = task_name.strip() if task_name else None
    task_description = task_description.strip() if task_description else None

    tasks_dao.update_task(task_id, task_name, due_date, task_description, priority, estimated_hours,  status)
    return True, None

def delete_task(task_id):
    """Delete a task by its ID."""
    if not task_id:
        return False, "Task ID is required."
    existing_task = tasks_dao.get_task_by_id(task_id)
    if not existing_task:
        return False, "Task not found."
    tasks_dao.delete_task(task_id)
    return True, None

def mark_task_completed(task_id):
    """Mark a task as completed."""
    if not task_id:
        return False, "Task ID is required."
    existing_task = tasks_dao.get_task_by_id(task_id)
    if not existing_task:
        return False, "Task not found."
    tasks_dao.mark_task_completed(task_id)
    return True, None