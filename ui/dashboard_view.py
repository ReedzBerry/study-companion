from PySide6.QtWidgets import (
    QMessageBox, QPushButton, QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QScrollArea, QFrame
)
from PySide6.QtCore import Qt
from datetime import datetime, timedelta
from logic import dashboard_logic
from logic import planner_logic

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
    QWidget#dashboard_content {{
        background-color: {COLOURS['background']};
        color: {COLOURS['text_primary']};
    }}
    QWidget#dashboard_scroll {{
        background-color: transparent;
        border: none;
    }}
    QAbstractScrollArea#dashboard_scroll {{
        background-color: transparent;
    }}

    QWidget#central_widget{{
        background-color: {COLOURS['background']};
        color: {COLOURS['text_primary']};
    }}

    QWidget#content_area{{
        background-color: {COLOURS['background']};
        color: {COLOURS['text_primary']};
    }}

    QWidget#day_widget {{
        background-color: transparent;
        border: none;
    }}

    QScrollArea {{
        background-color: transparent;
        border: none;
    }}
    QScrollArea > QWidget > QWidget {{
        background-color: transparent;
    }}
    QLabel#view_title {{
        font-size: 22px;
        font-weight: bold;
        color: {COLOURS['text_primary']};
        padding: 10px 0px;
    }}
    QLabel#section_title {{
        font-size: 15px;
        font-weight: bold;
        color: {COLOURS['text_primary']};
        padding: 6px 0px;
    }}
    QFrame#card {{
        background-color: {COLOURS['card']};
        border-radius: 8px;
        border: 1px solid {COLOURS['sidebar']};
    }}
    QLabel#task_item {{
        color: {COLOURS['text_primary']};
        font-size: 12px;
        padding: 4px 0px;
    }}
    QLabel#task_date {{
        color: {COLOURS['text_secondary']};
        font-size: 11px;
        padding: 2px 0px;
    }}
    QLabel#overdue_item {{
        color: {COLOURS['danger']};
        font-size: 12px;
        padding: 4px 0px;
    }}
    QLabel#empty_label {{
        color: {COLOURS['text_secondary']};
        font-size: 12px;
        padding: 4px 0px;
    }}
    QLabel#progress_overall {{
        font-size: 20px;
        font-weight: bold;
        color: {COLOURS['success']};
        padding: 4px 0px;
    }}
    QLabel#progress_course {{
        font-size: 12px;
        color: {COLOURS['text_primary']};
        padding: 2px 0px;
    }}
    QLabel#workload_day {{
        font-size: 12px;
        font-weight: bold;
        color: {COLOURS['text_primary']};
        padding: 4px 6px;
    }}
    QLabel#workload_hours {{
        font-size: 11px;
        color: {COLOURS['text_secondary']};
        padding: 2px 6px;
    }}
    QLabel#workload_bar {{
        background-color: {COLOURS['accent']};
        border-radius: 3px;
        min-height: 8px;
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
"""

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(VIEW_STYLE)
        self._build_ui()

    def _build_ui(self):
        # Outer scroll area so content doesn't get cut off
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setObjectName("dashboard_scroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content = QWidget()
        content.setObjectName("dashboard_content")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title and refresh
        header_layout = QHBoxLayout()
        title = QLabel("Dashboard")
        title.setObjectName("view_title")
        header_layout.addWidget(title)
        header_layout.addStretch()

        refresh_btn = QPushButton("↻ Refresh")
        refresh_btn.setObjectName("nav_button")
        refresh_btn.clicked.connect(self._load_dashboard)
        header_layout.addWidget(refresh_btn)

        seed_btn = QPushButton("Reset Demo Data")
        seed_btn.setObjectName("nav_button")
        seed_btn.clicked.connect(self._load_demo_data)
        header_layout.addWidget(seed_btn)

        # Last updated label
        self.updated_label = QLabel()
        self.updated_label.setObjectName("empty_label")
        header_layout.addWidget(self.updated_label)
        layout.addLayout(header_layout)

        # Top row — three cards side by side
        top_row = QHBoxLayout()
        top_row.setSpacing(16)

        self.upcoming_card = self._make_card()
        self.upcoming_card.setMaximumHeight(300)
        self.overdue_card = self._make_card()
        self.overdue_card.setMaximumHeight(300)
        self.progress_card = self._make_card()
        self.progress_card.setMaximumHeight(300)

        top_row.addWidget(self.upcoming_card)
        top_row.addWidget(self.overdue_card)
        top_row.addWidget(self.progress_card)
        layout.addLayout(top_row)

        # Bottom — workload card
        self.workload_card = self._make_card()
        layout.addWidget(self.workload_card)

        layout.addStretch()
        scroll.setWidget(content)
        outer_layout.addWidget(scroll)

        # Load data
        self._load_dashboard()

    def _make_card(self):
        """Create an empty card frame."""
        card = QFrame()
        card.setObjectName("card")
        card.setLayout(QVBoxLayout())
        card.layout().setContentsMargins(16, 16, 16, 16)
        card.layout().setSpacing(8)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        return card

    def _clear_card(self, card):
        """Remove all widgets from a card."""
        while card.layout().count():
            item = card.layout().takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
            elif item.layout():
                # Clear nested layouts if any (like in workload bars)
                nested = item.layout()
                while nested.count():
                    nested_item = nested.takeAt(0)
                    nested_widget = nested_item.widget()
                    if nested_widget:
                        nested_widget.setParent(None)

    #TODO - Remove before submission
    def _load_demo_data(self):
        """Clear database and load demo data."""
        reply = QMessageBox.question(
            self, "Load Demo Data",
        "This will DELETE all existing data and replace it with demo data.\n\nAre you sure?",
        QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                import seed_data
                seed_data.clear_database()
                QMessageBox.information(self, "Success","Demo data loaded successfully!")    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load demo data: {str(e)}")

    def _load_dashboard(self):
        """Load all dashboard data."""
        self.updated_label.setText(f"Updated: {datetime.now().strftime('%H:%M')}")
        self._load_upcoming()
        self._load_overdue()
        self._load_progress()
        self._load_workload()

    def _load_upcoming(self):
        """Load upcoming tasks card."""
        self._clear_card(self.upcoming_card)
        layout = self.upcoming_card.layout()

        title = QLabel("Upcoming Tasks")
        title.setObjectName("section_title")
        layout.addWidget(title)

        subtitle = QLabel("Due in the next 7 days")
        subtitle.setObjectName("empty_label")
        layout.addWidget(subtitle)

        upcoming, _ = dashboard_logic.get_upcoming_tasks()

        # Scrollable area if too many tasks
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setMaximumHeight(180)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(4)

        if not upcoming:
            empty = QLabel("No upcoming tasks 🎉")
            empty.setObjectName("empty_label")
            scroll_layout.addWidget(empty)
        else:
            for task in upcoming:
                task_name = task[2]
                due_date = task[3][:10] if task[3] else "—"
                priority = task[5]

                task_label = QLabel(f"• {task_name}")
                task_label.setObjectName("task_item")
                task_label.setWordWrap(True)
                scroll_layout.addWidget(task_label)

                date_label = QLabel(f"  Due: {due_date} — {priority} priority")
                date_label.setObjectName("task_date")
                scroll_layout.addWidget(date_label)

            if len(upcoming) > 5:
                more = QLabel(f"  + {len(upcoming) - 5} more...")
                more.setObjectName("empty_label")
                scroll_layout.addWidget(more)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        layout.addStretch()

    def _load_overdue(self):
        """Load overdue tasks card."""
        self._clear_card(self.overdue_card)
        layout = self.overdue_card.layout()

        title = QLabel("Overdue Tasks")
        title.setObjectName("section_title")
        layout.addWidget(title)

        subtitle = QLabel("Past due date")
        subtitle.setObjectName("empty_label")
        layout.addWidget(subtitle)

        overdue, _ = dashboard_logic.get_overdue_tasks()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setMaximumHeight(180)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(4)

        if not overdue:
            empty = QLabel("No overdue tasks 🎉")
            empty.setObjectName("empty_label")
            scroll_layout.addWidget(empty)
        else:
            for task in overdue[:5]:  # Show max 5
                task_name = task[2]
                due_date = task[3][:10] if task[3] else "—"

                task_label = QLabel(f"• {task_name}")
                task_label.setObjectName("overdue_item")
                task_label.setWordWrap(True)
                scroll_layout.addWidget(task_label)

                date_label = QLabel(f"  Was due: {due_date}")
                date_label.setObjectName("task_date")
                scroll_layout.addWidget(date_label)

            if len(overdue) > 5:
                more = QLabel(f"  + {len(overdue) - 5} more...")
                more.setObjectName("empty_label")
                scroll_layout.addWidget(more)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        layout.addStretch()

    def _load_progress(self):
        """Load progress metrics card."""
        self._clear_card(self.progress_card)
        layout = self.progress_card.layout()

        title = QLabel("Progress")
        title.setObjectName("section_title")
        layout.addWidget(title)

        metrics, _ = dashboard_logic.get_progress_metrics()

        # Overall percentage
        overall = QLabel(f"{metrics['percentage']}% Complete")
        overall.setObjectName("progress_overall")
        overall.setAlignment(Qt.AlignCenter)
        layout.addWidget(overall)

        summary = QLabel(f"{metrics['completed']} of {metrics['total']} tasks done")
        summary.setObjectName("empty_label")
        summary.setAlignment(Qt.AlignCenter)
        layout.addWidget(summary)

        # Per course breakdown
        if metrics['by_course']:
            divider = QLabel("─" * 20)
            divider.setObjectName("empty_label")
            layout.addWidget(divider)

            for course in metrics['by_course']:
                course_label = QLabel(
                    f"• {course['course_name']}: {course['percentage']}% "
                    f"({course['completed']}/{course['total']})"
                )
                course_label.setObjectName("progress_course")
                course_label.setWordWrap(True)
                layout.addWidget(course_label)

        layout.addStretch()

    def _load_workload(self):
        """Load weekly workload card."""
        self._clear_card(self.workload_card)
        layout = self.workload_card.layout()
        layout.setContentsMargins(20,20,20,20)

        title = QLabel("This Week's Planned Workload")
        title.setObjectName("section_title")
        layout.addWidget(title)

        # Get current week plan
        today = datetime.today().date()
        week_start = today - timedelta(days=today.weekday())
        plan, error = planner_logic.get_or_create_plan(week_start.isoformat())

        if error or not plan:
            empty = QLabel("No plan found for this week.")
            empty.setObjectName("empty_label")
            layout.addWidget(empty)
            layout.addStretch()
            return

        plan_id = plan[0]
        workload, _ = planner_logic.get_weekly_workload(plan_id)

        # Day columns
        days_layout = QHBoxLayout()
        days_layout.setContentsMargins(10, 0, 10, 0)
        days_layout.setSpacing(10)

        max_hours = max(workload.values()) if workload else 1
        max_hours = max(max_hours, 1)  # Avoid division by zero

        for day in DAYS:
            hours = workload.get(day, 0)
            day_widget = QWidget()
            day_widget.setObjectName("day_widget")
            day_layout = QVBoxLayout(day_widget)
            day_layout.setContentsMargins(0, 0, 0, 0)
            day_layout.setSpacing(2)
            day_layout.setAlignment(Qt.AlignBottom)

            # Bar
            bar = QLabel()
            bar.setObjectName("workload_bar")
            bar_height = max(8, int((hours / max_hours) * 60))
            bar.setFixedHeight(bar_height)
            day_layout.addWidget(bar)

            # Day name
            day_label = QLabel(day[:3])
            day_label.setObjectName("workload_day")
            day_label.setAlignment(Qt.AlignCenter)
            day_layout.addWidget(day_label)

            # Hours
            hours_label = QLabel(f"{hours}h")
            hours_label.setObjectName("workload_hours")
            hours_label.setAlignment(Qt.AlignCenter)
            day_layout.addWidget(hours_label)

            days_layout.addWidget(day_widget, 1)

        layout.addLayout(days_layout)
        layout.addStretch()