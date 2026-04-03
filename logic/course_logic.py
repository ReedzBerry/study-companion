from database import courses_dao

def create_course(course_name, course_code=None):
    """Validate and create a new course."""
    # Validate course name
    if not course_name or not course_name.strip():
        return None, "Course name cannot be empty."
    if len(course_name) > 100:
        return None, "Course name cannot exceed 100 characters."
    
    # Validate course code if provided
    if course_code and len(course_code.strip()) > 20:
        return None, "Course code cannot exceed 20 characters."
    
    # clean up whitespace
    course_name = course_name.strip()
    course_code = course_code.strip() if course_code else None

    course_id = courses_dao.create_course(course_name, course_code)
    return course_id, None

def get_all_courses():
    """Retrieve all courses."""
    return courses_dao.get_all_courses()

def get_course_by_id(course_id):
    """Retrieve a course by its ID."""
    if not course_id:
        return None, "Course ID is required."
    course = courses_dao.get_course_by_id(course_id)
    if not course:
        return None, "Course not found."
    return course, None

def update_course(course_id, course_name, course_code=None):
    """"Validate and update existing course."""
    if not course_id:
        return False, "Course ID is required."
    if not course_name or not course_name.strip():
        return False, "Course name cannot be empty."
    if len(course_name.strip()) > 100:
        return False, "Course name cannot exceed 100 characters."
    if course_code and len(course_code.strip()) > 20:
        return False, "Course code cannot exceed 20 characters."
    
    # clean up whitespace
    course_name = course_name.strip()
    course_code = course_code.strip() if course_code else None

    courses_dao.update_course(course_id, course_name, course_code)
    return True, None

def delete_course(course_id):
    """Delete a course by its ID."""
    if not course_id:
        return False, "Course ID is required."
    course = courses_dao.get_course_by_id(course_id)
    if not course:
        return False, "Course not found."
    courses_dao.delete_course(course_id)
    return True, None

