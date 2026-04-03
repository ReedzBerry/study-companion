from database import plans_dao
from datetime import datetime, timedelta

def create_weekly_plan(week_start):
    """Validate and create a new weekly plan."""
    if not week_start:
        return None, "Week start date is required."
    
    try:
        parsed_date = datetime.strptime(week_start, "%Y-%m-%d").date()
    except ValueError:
        return None, "Invalid date format. Use YYYY-MM-DD."
    
    # Ensure the week starts on a Monday
    if parsed_date.weekday() != 0:
        return None, "Week start date must be a Monday."
    
    week_end_date = parsed_date + timedelta(days=6)
    plan_id = plans_dao.create_weekly_plan(parsed_date.isoformat(), week_end_date.isoformat())
    return plan_id, None

def get_or_create_plan():
    """Get the current week's plan or create one if it doesn't exist."""
    today = datetime.today().date()
    week_start = today - timedelta(days=today.weekday())  # Get the Monday of the current week
    existing_plan = plans_dao.get_plan_by_week(week_start.isoformat())
    
    if existing_plan:
        return existing_plan, None
    
    return create_weekly_plan(week_start.isoformat())

def add_plan_items(plan_id, task_id, scheduled_day, hours_planned):
    """Validate and add a task to a weekly plan."""
    if not plan_id:
        return None, "Plan ID is required."
    if not task_id:
        return None, "Task ID is required."
    if not scheduled_day:
        return None, "Scheduled day is required."
    
    # Validate scheduled day is a valid day name
    valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if scheduled_day not in valid_days:
        return None, "Scheduled day must be one of: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday."
    
    # Validate hours planned
    if hours_planned is not None:
        if hours_planned < 0:
            return None, "Hours planned cannot be negative."
        if hours_planned > 24:
            return None, "Hours planned cannot exceed 24."
    
    plan_item_id = plans_dao.add_plan_item(plan_id, task_id, scheduled_day, hours_planned)
    return plan_item_id, None

def get_items_by_plan(plan_id):
    """Retrieve all items for a specific weekly plan."""
    if not plan_id:
        return None, "Plan ID is required."
    return plans_dao.get_items_by_plan(plan_id), None

def get_items_by_day(plan_id, scheduled_day):
    """Retrieve all items for a specific day in a weekly plan."""
    if not plan_id:
        return None, "Plan ID is required."
    if not scheduled_day:
        return None, "Scheduled day is required."
    
    # Validate scheduled day is a valid day name
    valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if scheduled_day not in valid_days:
        return None, "Scheduled day must be one of: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday."
    
    return plans_dao.get_items_by_day(plan_id, scheduled_day), None

def update_plan_item(plan_item_id, scheduled_day=None, hours_planned=None):
    """Validate and update a plan item."""
    if not plan_item_id:
        return False, "Plan item ID is required."
    
    # Validate hours planned
    if hours_planned is not None and hours_planned < 0:
        return False, "Hours planned cannot be negative."
    
    # Validate scheduled day
    valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if scheduled_day is not None and scheduled_day not in valid_days:
        return False, "Scheduled day must be one of: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday."
    
    plans_dao.update_plan_item(plan_item_id, scheduled_day, hours_planned)
    return True, None

def delete_plan_item(plan_item_id):
    """Delete a plan item by its ID."""
    if not plan_item_id:
        return False, "Plan item ID is required."
    
    plans_dao.delete_plan_item(plan_item_id)
    return True, None

def delete_weekly_plan(plan_id):
    """Delete a weekly plan and all its associated items."""
    if not plan_id:
        return False, "Plan ID is required."
 
    plans_dao.delete_weekly_plan(plan_id)
    return True, None

def get_weekly_workload(plan_id):
    """Calculate the total planned hours for a weekly plan."""
    if not plan_id:
        return None, "Plan ID is required."
    
    items = plans_dao.get_items_by_plan(plan_id)
    
    # Build a dictionary of hours per day
    workload = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}

    for item in items:
        day = item[3] # scheduled_day is index 3
        hours = item[4] # hours_planned is index 4
        if hours is not None:
            workload[day] += hours

    return workload, None