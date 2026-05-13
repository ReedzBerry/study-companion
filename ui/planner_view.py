from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QScrollArea,
    QFrame, QMessageBox, QDialog,
    QFormLayout, QComboBox, QDoubleSpinBox,
    QDialogButtonBox, QApplication
)
from PySide6.QtCore import Qt
from datetime import datetime, timedelta
from logic import planner_logic
from logic import task_logic
from logic import course_logic

COLOURS = {
    "background":     "#1e1e2e",
    "sidebar":        "#2a2a3d",
    "card":           "#2f2f45",
    "accent":         "#2A3C5B",
    "text_primary":   "#ffffff",
    "text_secondary": "#a0a0b0",
    "success":        "#4caf82",
    "warning":        "#f7a94f",
    "danger":         "#f75f5f",
}

VIEW_STYLE = f"""
    QWidget {{
        background-color: {COLOURS['background']};
        color: {COLOURS['text_primary']};
    }}
    QLabel#view_title {{
        font-size: 22px;
        font-weight: bold;
        color: {COLOURS['text_primary']};
        padding: 10px 0px;
    }}
    QLabel#week_label {{
        font-size: 14px;
        color: {COLOURS['text_secondary']};
        padding: 4px 10px;
    }}
    QPushButton#nav_button {{
        background-color: {COLOURS['card']};
        color: {COLOURS['text_primary']};
        border: none;
        padding: 6px 12px;
        font-size: 13px;
        border-radius: 4px;
    }}
    QPushButton#nav_button:hover {{
        background-color: {COLOURS['accent']};
    }}
    QPushButton#add_button {{
        background-color: {COLOURS['accent']};
        color: {COLOURS['text_primary']};
        border: none;
        padding: 4px 8px;
        font-size: 11px;
        border-radius: 4px;
    }}
    QPushButton#add_button:hover {{
        background-color: {COLOURS['card']};
    }}
    QPushButton#delete_button {{
        background-color: transparent;
        color: {COLOURS['danger']};
        border: none;
        font-size: 11px;
        padding: 2px 4px;
    }}
    QPushButton#delete_button:hover {{
        color: #ff0000;
    }}
    QFrame#day_column {{
        background-color: {COLOURS['card']};
        border-radius: 6px;
        border: 1px solid {COLOURS['sidebar']};
    }}
    QLabel#day_header {{
        font-size: 13px;
        font-weight: bold;
        color: {COLOURS['text_primary']};
        padding: 8px;
        background-color: {COLOURS['accent']};
        border-radius: 4px;
    }}
    QLabel#day_header_today {{
        font-size: 13px;
        font-weight: bold;
        color: {COLOURS['text_primary']};
        padding: 8px;
        background-color: {COLOURS['success']};
        border-radius: 4px;
    }}
    QLabel#day_total {{
        font-size: 11px;
        color: {COLOURS['text_secondary']};
        padding: 4px 8px;
    }}
    QLabel#task_card {{
        background-color: {COLOURS['sidebar']};
        color: {COLOURS['text_primary']};
        border-radius: 4px;
        padding: 6px;
        font-size: 11px;
    }}
    QComboBox {{
        background-color: {COLOURS['card']};
        color: {COLOURS['text_primary']};
        border: 1px solid {COLOURS['accent']};
        padding: 6px;
        border-radius: 4px;
    }}
    QDoubleSpinBox {{
        background-color: {COLOURS['card']};
        color: {COLOURS['text_primary']};
        border: 1px solid {COLOURS['accent']};
        padding: 6px;
        border-radius: 4px;
    }}
"""

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class PlannerView(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(VIEW_STYLE)
        self.current_week_start = self._get_current_monday()
        self._build_ui()
        self._load_planner()

    def _get_current_monday(self):
        """Get the Monday of the current week."""
        today = datetime.today().date()
        return today - timedelta(days=today.weekday())

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header row
        header_layout = QHBoxLayout()
        title = QLabel("Planner")
        title.setObjectName("view_title")
        header_layout.addWidget(title)
        header_layout.addStretch()

        # Week navigation
        prev_btn = QPushButton("< Prev")
        prev_btn.setObjectName("nav_button")
        prev_btn.clicked.connect(self._prev_week)
        header_layout.addWidget(prev_btn)

        today_btn = QPushButton("Today")
        today_btn.setObjectName("nav_button")
        today_btn.clicked.connect(self._go_to_today)
        header_layout.addWidget(today_btn)

        self.week_label = QLabel()
        self.week_label.setObjectName("week_label")
        self.week_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.week_label)

        next_btn = QPushButton("Next >")
        next_btn.setObjectName("nav_button")
        next_btn.clicked.connect(self._next_week)
        header_layout.addWidget(next_btn)

        layout.addLayout(header_layout)

        # Scroll area for the day columns
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        self.grid_widget = QWidget()
        self.grid_layout = QHBoxLayout(self.grid_widget)
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        scroll.setWidget(self.grid_widget)
        layout.addWidget(scroll)

    def _load_planner(self):
        """Load the planner for the current week."""
        # Update week label
        week_end = self.current_week_start + timedelta(days=6)
        self.week_label.setText(
            f"{self.current_week_start.strftime('%d %b')} — {week_end.strftime('%d %b %Y')}"
        )

        # Clear existing grid
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

        # Force Qt to process pending deletions before rebuilding
        QApplication.processEvents()

        # Get or create plan for this week
        plan, error = planner_logic.get_or_create_plan(
            self.current_week_start.isoformat()
        )
        if error:
            QMessageBox.warning(self, "Error", error)
            return

        # plan is a tuple: (plan_id, week_start, week_end, created_at)
        plan_id = plan[0]

        # Get workload per day
        workload, _ = planner_logic.get_weekly_workload(plan_id)

        # Get items for this plan
        items, _ = planner_logic.get_items_by_plan(plan_id)

        # Build day columns
        for day in DAYS:
            day_items = [i for i in (items or []) if i[3] == day]
            self.grid_layout.addWidget(
                self._build_day_column(plan_id, day, day_items, workload.get(day, 0))
            )

    def _build_day_column(self, plan_id, day, items, total_hours):
        """Build a single day column widget."""
        column = QFrame()
        column.setObjectName("day_column")
        column.setMinimumWidth(140)

        # Check if this column is today
        today = datetime.today().strftime("%A")
        is_today = day == today

        layout = QVBoxLayout(column)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        # Calculate date for this day
        day_index = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(day)
        day_date = self.current_week_start + timedelta(days=day_index)
        day_date_str = day_date.strftime("%d/%m")

        # Day header - highlight if today
        header = QLabel(f"{day[:3]}\n{day_date_str}")
        header.setObjectName("day_header_today" if is_today else "day_header")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Add button
        add_btn = QPushButton("+ Add")
        add_btn.setObjectName("add_button")
        add_btn.clicked.connect(lambda checked, d=day, pid=plan_id: self._open_add_dialog(pid, d))
        layout.addWidget(add_btn)

        # Task cards
        for item in items:
            plan_item_id = item[0]
            task_id = item[2]
            hours = item[4]

            # Get task name
            task, _ = task_logic.get_task_by_id(task_id)
            task_name = task[2] if task else "Unknown Task"

            # Get course name is task has one
            course_name = ""
            if task and task[1]:
                courses = course_logic.get_all_courses()
                course_map = {c[0]: c[1] for c in courses}
                course_name = course_map.get(task[1], "")

            # Task card
            card_widget = QWidget()
            card_layout = QVBoxLayout(card_widget)
            card_layout.setContentsMargins(4, 4, 4, 4)
            card_layout.setSpacing(2)

            # Build task label text
            task_text = f"{task_name}\n{hours or 0} hrs"
            if course_name:
                task_text = f"\n{course_name}"

            task_label = QLabel(task_text)
            task_label.setObjectName("task_card")
            task_label.setWordWrap(True)
            card_layout.addWidget(task_label)

            remove_btn = QPushButton("✕ Remove")
            remove_btn.setObjectName("delete_button")
            remove_btn.clicked.connect(
                lambda checked, piid=plan_item_id: self._remove_item(piid)
            )
            card_layout.addWidget(remove_btn)
            layout.addWidget(card_widget)

        # Push everything up
        layout.addStretch()

        # Daily total
        total_label = QLabel(f"Total: {total_hours} hrs")
        total_label.setObjectName("day_total")
        total_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(total_label)

        return column

    def _prev_week(self):
        """Navigate to the previous week."""
        self.current_week_start -= timedelta(weeks=1)
        self._load_planner()

    def _go_to_today(self):
        """Navigate to the current week."""
        self.current_week_start = self._get_current_monday()
        self._load_planner()

    def _next_week(self):
        """Navigate to the next week."""
        self.current_week_start += timedelta(weeks=1)
        self._load_planner()

    def _open_add_dialog(self, plan_id, day):
        """Open dialog to add a task to a specific day."""
        all_tasks = task_logic.get_all_tasks()
        incomplete_tasks = [t for t in all_tasks if t[7] != "Done"]

        if not incomplete_tasks:
            QMessageBox.information(self, "No Tasks", "No incomplete tasks available to schedule.")
            return

        dialog = PlanItemDialog(self, day, incomplete_tasks)
        if dialog.exec() == QDialog.Accepted:
            task_id, hours = dialog.get_values()
            result, error = planner_logic.add_plan_item(plan_id, task_id, day, hours)
            if error:
                QMessageBox.warning(self, "Error", error)
            else:
                QMessageBox.information(self, "Success", f"Task scheduled for {day}!")
                self._load_planner()

    def _remove_item(self, plan_item_id):
        """Remove a task from the planner."""
        reply = QMessageBox.question(
            self, "Remove Task",
            "Remove this task from the planner?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            result, error = planner_logic.delete_plan_item(plan_item_id)
            if error:
                QMessageBox.warning(self, "Error", error)
            else:
                self._load_planner()


class PlanItemDialog(QDialog):
    """Dialog for scheduling a task to a day."""
    def __init__(self, parent=None, day="Monday", tasks=None):
        super().__init__(parent)
        self.setWindowTitle(f"Schedule Task — {day}")
        self.setMinimumWidth(350)
        self.tasks = tasks or []
        self._build_ui()

    def _build_ui(self):
        layout = QFormLayout(self)
        layout.setSpacing(12)

        # Task dropdown
        self.task_combo = QComboBox()
        for task in self.tasks:
            self.task_combo.addItem(task[2], task[0])
        layout.addRow("Task", self.task_combo)

        # Hours planned
        self.hours_input = QDoubleSpinBox()
        self.hours_input.setRange(0, 24)
        self.hours_input.setSingleStep(0.5)
        self.hours_input.setSuffix(" hrs")
        self.hours_input.setValue(1.0)
        layout.addRow("Hours Planned", self.hours_input)

        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_values(self):
        return self.task_combo.currentData(), self.hours_input.value()