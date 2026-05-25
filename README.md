# Digital Study Companion

## Overview

**Digital Study Companion** is a desktop application designed to help tertiary students manage study workload through structured scheduling, task tracking, and progress monitoring. The application provides a central dashboard for viewing upcoming deadlines, a weekly planner for distributing tasks across the week, and progress metrics to support motivation and reflective study habits.

**Target Platform:** Windows 10/11  
**Framework:** Python 3.11 + PySide6  
**Database:** SQLite (local, no cloud sync)

---

## Project Artefacts Included

### Source Code
```
Study_companion_app/
├── database/
│   ├── __init__.py
│   ├── database_setup.py          # Database initialization and schema
│   ├── course_dao.py              # Course data access operations
│   ├── task_dao.py                # Task data access operations
│   └── weekly_plan_dao.py         # Weekly planning data access
│
├── logic/
│   ├── __init__.py
│   ├── course_logic.py            # Course validation and business logic
│   ├── task_logic.py              # Task validation and business logic
│   ├── plans_logic.py             # Planner logic and workload calculations
│   └── dashboard_logic.py         # Dashboard metrics and aggregations
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py             # Main application window and navigation
│   ├── course_view.py             # Course management UI
│   ├── task_view.py               # Task management UI with filtering
│   ├── planner_view.py            # Weekly planner UI
│   └── dashboard_view.py          # Dashboard and metrics UI
│
├── assets/                        # Empty directory for future use
│
├── main.py                        # Application entry point
├── seed_data.py                   # Demo data seeding utility
└── seed_stress_test.py            # Stress test data generator (120+ tasks)
```

### Documentation
- **README.md** — This file; setup and running instructions
- **TEST_PLAN.md** — Comprehensive test plan with 39 test cases and results
- **TECHNICAL_DOCUMENTATION.md** — System architecture, database schema, and API reference

### Testing & Data
- **test_plan.txt** — Detailed test cases, results, and defect log
- **seed_data.py** — Generates demo data (3 courses, 10 tasks, 1 weekly plan)
- **seed_stress_test.py** — Generates 120+ tasks for stability testing

### Additional Files
- **requirements.txt** — Python dependencies (PySide6, PyInstaller)

---

## System Requirements

### Hardware
- **OS:** Windows 10 or Windows 11
- **RAM:** 4GB minimum (8GB recommended)
- **Storage:** 200MB available disk space
- **Display:** Minimum 1280x720 resolution
- **Input:** Standard keyboard and mouse

### Software
- **Python:** Version 3.11 or later
- **PySide6:** 6.7.0 (Qt for Python)
- **SQLite:** 3.x (included with Python)

---

## Installation & Setup

### Step 1: Install Python

Download and install Python 3.11 from [python.org](https://www.python.org/downloads/).

**During installation:**
-  Check "Add Python to PATH"
-  Check "Install pip"

Verify installation:
```bash
python --version
pip --version
```

### Step 2: Extract Project Files

Extract the provided `.zip` file to a location on your computer:
```
C:\Users\YourUsername\Documents\Study_companion_app\
```

### Step 3: Install Dependencies

Open Command Prompt (or PowerShell) and navigate to the project directory:

```bash
cd C:\Users\YourUsername\Documents\Study_companion_app
```

Install required packages:
```bash
pip install -r requirements.txt
```

This will install:
- **PySide6** — Qt framework for the user interface
- **PyInstaller** — For packaging the app as a standalone executable (optional)

---

## Running the Application

### Method 1: Run from Source (Recommended for Development)

From the project directory in Command Prompt:

```bash
python main.py
```

The application will:
1. Initialize the SQLite database if it doesn't exist
2. Load demo data on first run (if the database is empty)
3. Launch the main application window

### Method 2: Run from Packaged Executable (Optional)

To create a standalone `.exe` file that doesn't require Python:

```bash
pyinstaller --onefile --windowed --name "Study Companion" main.py
```

This creates:
- `dist/Study Companion.exe` — Standalone executable
- Run this `.exe` directly without needing Python installed

**Note:** The packaged version may take longer to start on first run.

---

## Using the Application

### First Launch

On first launch, the application will automatically:
1. Create the SQLite database (`study_companion.db`)
2. Load demo data with:
   - 3 sample courses (Web Development, IT Project, Database Management)
   - 10 sample tasks with varied statuses (overdue, upcoming, completed)
   - 1 weekly plan with 6 scheduled tasks

### Main Features

#### Dashboard
- **Upcoming Tasks:** Tasks due within the next 7 days
- **Overdue Tasks:** Tasks past their due date (not completed)
- **Progress Metrics:** Overall completion % and per-course breakdown
- **Weekly Workload:** Bar chart showing planned hours per day

#### Tasks
- Create, edit, and delete tasks
- Assign tasks to courses
- Set priority (Low/Medium/High), due date, estimated hours
- Update status (Not Started → In Progress → Done)
- Filter by status or view all tasks

#### Courses
- Manage courses for organizational purposes
- Associate tasks with courses
- View progress metrics per course
- Delete courses (associated tasks remain)

#### Planner
- View weekly schedule (Monday–Sunday)
- Assign tasks to specific days
- Track daily workload (sum of estimated hours)
- Navigate between weeks (Previous/Today/Next)
- Today's column highlighted in green

---

## Resetting Demo Data

To reset the application to original demo data:

1. Navigate to the Dashboard
2. Click **"Reset Demo Data"** button
3. Confirm the action

Alternatively, from Command Prompt in the project directory:

```bash
python seed_data.py
```

---

## Stress Testing

To test the application with a large data set (120+ tasks):

From Command Prompt in the project directory:

```bash
python seed_stress_test.py
```

This:
- Creates 120 random tasks across multiple courses
- Distributes them across ±60 days from today
- Tests dashboard responsiveness and stability
- Should load without crashes or significant lag

After stress testing, reset to demo data using the Dashboard button.

---

## Testing

### Manual Testing

The test plan includes 39 test cases covering:
-  Course management (create, edit, delete)
-  Task creation and status updates
-  Dashboard display and refresh
-  Weekly planner functionality
-  Task filtering and progress metrics
-  Data persistence after restart
-  Stress testing with 100+ tasks

Run test cases by manually using the application and verifying expected outcomes.

### Automated Testing

Currently, the application uses manual testing. For future development, consider:
- Unit tests using `pytest`
- Integration tests for database operations
- UI tests using `pytest-qt`

---

## Project Structure & Architecture

### Layered Architecture

```
User Interface (PySide6)
        ↓
Business Logic (Validation, Calculations)
        ↓
Data Access Layer (DAO Pattern)
        ↓
SQLite Database
```

### Key Design Patterns

- **Data Access Object (DAO):** Each entity (Course, Task, Plan) has a dedicated DAO module for database operations
- **Separation of Concerns:** UI, logic, and data access are strictly separated
- **Validation:** All inputs validated at the logic layer before database operations
- **(value, error) Tuple Returns:** Consistent error handling throughout the application

### Database Schema

#### Courses Table
```sql
course_id (INTEGER PRIMARY KEY)
course_name (TEXT NOT NULL)
course_code (TEXT UNIQUE)
created_at (TEXT NOT NULL)
```

#### Tasks Table
```sql
task_id (INTEGER PRIMARY KEY)
course_id (INTEGER, FOREIGN KEY)
task_name (TEXT NOT NULL)
due_date (TEXT NOT NULL)
priority (TEXT: Low/Medium/High)
estimated_hours (REAL)
status (TEXT: Not Started/In Progress/Done)
completion_date (TEXT)
created_at (TEXT NOT NULL)
updated_at (TEXT)
```

#### Weekly_Plans Table
```sql
plan_id (INTEGER PRIMARY KEY)
week_start (TEXT NOT NULL)
week_end (TEXT NOT NULL)
created_at (TEXT NOT NULL)
```

#### Plan_Items Table
```sql
plan_item_id (INTEGER PRIMARY KEY)
plan_id (INTEGER FOREIGN KEY)
task_id (INTEGER FOREIGN KEY)
scheduled_day (TEXT: Monday–Sunday)
hours_planned (REAL)
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'PySide6'"

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Database file not found

**Solution:** The app creates the database automatically on first run. If issues persist:
1. Delete `study_companion.db` (if it exists)
2. Run `main.py` again

### Issue: Application won't start

**Solution:** Check Python version:
```bash
python --version
```

Must be Python 3.11 or later. If needed, install a compatible version and update your PATH.

### Issue: UI elements overlapping or cut off

**Solution:** Ensure display resolution is at least 1280x720. The application is designed for this minimum resolution.

### Issue: Slow performance with many tasks

**Solution:** This is expected with 100+ tasks. For typical usage (under 100 tasks), the dashboard should load in under 2 seconds. The stress test confirms stability even with large datasets.

---

## Known Limitations & Future Enhancements

### Current Limitations (MVP)
- **Desktop only:** No mobile app or web version
- **Local storage only:** No cloud synchronization
- **Single user:** No multi-user support or collaboration
- **No external integrations:** Calendar, email, or LMS integration not supported
- **Windows primary:** Cross-platform support not tested

### Future Enhancement Ideas
1. **CSV Export:** Backup and export tasks to CSV
2. **Google Calendar Integration:** Sync scheduled tasks with Google Calendar
3. **Email Notifications:** Reminders for upcoming deadlines
4. **Mobile App:** Companion app for iOS/Android
5. **Dark/Light Theme Toggle:** User preference for UI theme
6. **Task Templates:** Reusable task templates for recurring assessments
7. **Collaborative Planning:** Share plans with study group members
8. **Advanced Analytics:** Predictive workload analysis and recommendations

---

## Support & Contact

For issues, questions, or feature requests:
- Review the TEST_PLAN.md for known issues and resolutions
- Check the TECHNICAL_DOCUMENTATION.md for architecture details
- Verify you're running Python 3.11+ and have installed all dependencies from requirements.txt

---

## License & Academic Use

This project is developed as part of BIT701 Assessment 3 at The Open Polytechnic of New Zealand.

**Academic Use Only:** This application is provided for educational purposes. Commercial use is not permitted without explicit authorization.

---

## Version Information

- **Application Version:** 1.0 (MVP)
- **Python Version:** 3.11+
- **PySide6 Version:** 6.7.0
- **Database:** SQLite 3.x
- **Last Updated:** May 2026

---

## Document Information

- **File:** README.md
- **Purpose:** Installation, setup, and usage guide for Digital Study Companion
- **Audience:** End users, markers, and developers
- **Maintenance:** Update as new features are added or dependencies change


