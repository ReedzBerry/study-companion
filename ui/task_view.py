from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox,
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox,
    QComboBox, QTextEdit, QDoubleSpinBox, QDateEdit
)
from PySide6.QtCore import Qt, QDate
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
    QPushButton#add_button {{
        background-color: {COLOURS['accent']};
        color: {COLOURS['text_primary']};
        border: none;
        padding: 8px 16px;
        font-size: 13px;
        border-radius: 4px;
    }}
    QPushButton#add_button:hover {{
        background-color: {COLOURS['card']};
    }}
    QPushButton#filter_button {{
        background-color: {COLOURS['card']};
        color: {COLOURS['text_secondary']};
        border: none;
        padding: 6px 14px;
        font-size: 12px;
        border-radius: 4px;
    }}
    QPushButton#filter_button:checked {{
        background-color: {COLOURS['accent']};
        color: {COLOURS['text_primary']};
    }}
    QPushButton#edit_button {{
        background-color: {COLOURS['card']};
        color: {COLOURS['text_primary']};
        border: none;
        padding: 8px 8px;
        font-size: 10px;
        border-radius: 4px;
        min-height: 35px;
    }}
    QPushButton#edit_button:hover {{
        background-color: {COLOURS['accent']};
    }}
    QPushButton#start_button {{
        background-color: {COLOURS['warning']};
        color: {COLOURS['text_primary']};
        border: none;
        padding: 8px 8px;
        font-size: 10px;
        border-radius: 4px;
        min-height: 35px;
    }}
    QPushButton#start_button:hover {{
        background-color: #d4922a;
    }}

    QPushButton#complete_button {{
        background-color: {COLOURS['success']};
        color: {COLOURS['text_primary']};
        border: none;
        padding: 8px 8px;
        font-size: 10px;
        border-radius: 4px;
        min-height: 35px;
    }}
    QPushButton#complete_button:hover {{
        background-color: #3d9e6e;
    }}
    QPushButton#delete_button {{
        background-color: {COLOURS['danger']};
        color: {COLOURS['text_primary']};
        border: none;
        padding: 8px 8px;
        font-size: 10px;
        border-radius: 4px;
        min-height: 35px;
    }}
    QPushButton#delete_button:hover {{
        background-color: #c0392b;
    }}
    QTableWidget {{
        background-color: {COLOURS['card']};
        color: {COLOURS['text_primary']};
        border: none;
        gridline-color: {COLOURS['sidebar']};
        font-size: 13px;
    }}
    QTableWidget::item {{
        padding: 8px;
    }}
    QTableWidget::item:selected {{
        background-color: {COLOURS['accent']};
    }}
    QHeaderView::section {{
        background-color: {COLOURS['sidebar']};
        color: {COLOURS['text_secondary']};
        padding: 8px;
        border: none;
        font-size: 13px;
    }}
    QComboBox {{
        background-color: {COLOURS['card']};
        color: {COLOURS['text_primary']};
        border: 1px solid {COLOURS['accent']};
        padding: 6px;
        border-radius: 4px;
    }}
    QLineEdit {{
        background-color: {COLOURS['card']};
        color: {COLOURS['text_primary']};
        border: 1px solid {COLOURS['accent']};
        padding: 6px;
        border-radius: 4px;
    }}
    QTextEdit {{
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
    QDateEdit {{
        background-color: {COLOURS['card']};
        color: {COLOURS['text_primary']};
        border: 1px solid {COLOURS['accent']};
        padding: 6px;
        border-radius: 4px;
    }}
"""

class TaskView(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(VIEW_STYLE)
        self.current_filter = "All"
        self._build_ui()
        self._load_tasks("All")

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30,30,30,30)
        layout.setSpacing(20)

        # Header row - title and add button
        header_layout = QHBoxLayout()
        title = QLabel("Tasks")
        title.setObjectName("view_title")
        header_layout.addWidget(title)
        header_layout.addStretch()

        add_btn = QPushButton("+ Add Task")
        add_btn.setObjectName("add_button")
        add_btn.clicked.connect(self._open_add_dialog)
        header_layout.addWidget(add_btn)
        layout.addLayout(header_layout)

        # Filter Buttons
        filter_layout = QHBoxLayout()
        self.filter_buttons = []
        for label in ["All", "Not Started", "In Progress", "Done"]:
            btn = QPushButton(label)
            btn.setObjectName("filter_button")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, l=label: self._apply_filter(l))
            filter_layout.addWidget(btn)
            self.filter_buttons.append(btn)
        filter_layout.addStretch()
        self.filter_buttons[0].setChecked(True)
        layout.addLayout(filter_layout)

        # Task Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Task Name", "Course", "Due Date", "Priority", "Status", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

    def _load_tasks(self, filter_status="All"):
        """Load tasks from the database and populate the table."""
        all_tasks = task_logic.get_all_tasks()
        courses = course_logic.get_all_courses()

        # Build a course id to name lookup
        course_map = {c[0]: c[1] for c in courses}

        self.table.setRowCount(0)

        for task in all_tasks:
            task_id =       task[0]
            course_id =     task[1]
            task_name =     task[2]
            due_date =      task[3][:10] if task[3] else "—"
            priority =      task[5]
            status =        task[7]

            # Apply filter
            if filter_status and filter_status != "All" and status != filter_status:
                continue

            course_name = course_map.get(course_id, "—") if course_id else "—"

            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setRowHeight(row, 60)
            self.table.setItem(row, 0, QTableWidgetItem(task_name))
            self.table.setItem(row, 1, QTableWidgetItem(course_name))
            self.table.setItem(row, 2, QTableWidgetItem(due_date))
            self.table.setItem(row, 3, QTableWidgetItem(priority))
            self.table.setItem(row, 4, QTableWidgetItem(status))

            # Action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 4, 4, 4)
            actions_layout.setSpacing(6)

            edit_btn = QPushButton("Edit")
            edit_btn.setObjectName("edit_button")
            edit_btn.clicked.connect(lambda checked, tid=task_id: self._open_edit_dialog(tid))

            start_btn = QPushButton("Start")
            start_btn.setObjectName("start_button")
            start_btn.clicked.connect(lambda checked, tid=task_id, tname=task_name: self._apply_filter("In Progress") if task_logic.update_task(tid, status="In Progress")[0] else QMessageBox.warning(self, "Error", "Failed to update task status."))
            start_btn.setEnabled(status == "Not Started")

            complete_btn = QPushButton("Complete")
            complete_btn.setObjectName("complete_button")
            complete_btn.clicked.connect(lambda checked, tid=task_id, tname=task_name: self._mark_complete(tid, tname))
            complete_btn.setEnabled(status != "Done")

            delete_btn = QPushButton("Delete")
            delete_btn.setObjectName("delete_button")
            delete_btn.clicked.connect(lambda checked, tid=task_id, tname=task_name: self._delete_task(tid, tname))

            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(start_btn)
            actions_layout.addWidget(complete_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch()
            self.table.setCellWidget(row, 5, actions_widget)

    def _apply_filter(self, status):
        """Apply a filter to the task list."""
        self.current_filter = status
        for btn in self.filter_buttons:
            btn.setChecked(btn.text() == status)
        self._load_tasks(filter_status=status)

    def _mark_in_progress(self, task_id, task_name):
        """Mark a task as in progress."""
        reply = QMessageBox.question(
            self, "Start TasK",
            f"Mark '{task_name}' as in progress?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            result, error = task_logic.update_task(task_id, status="In Progress")
            if error:
                QMessageBox.warning(self, "Error", error)
            else:
                QMessageBox.information(self, "Success", f"'{task_name}' is now in progress!")
                self._load_tasks(filter_status=self.current_filter)

    def _mark_complete(self, task_id, task_name):
        """Mark a task as complete."""
        reply = QMessageBox.question(
            self, "Mark Complete",
            f"Mark '{task_name}' as complete?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            result, error = task_logic.mark_task_completed(task_id)
            if error:
                QMessageBox.warning(self, "Error", error)
            else:
                QMessageBox.information(self, "Success", f"'{task_name}' marked as complete!")
                self._load_tasks(filter_status=self.current_filter)

    def _delete_task(self, task_id, task_name):
        """Confirm and delete a task."""
        reply = QMessageBox.question(
            self, "Delete Task",
            f"Are you sure you want to delete '{task_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            result, error = task_logic.delete_task(task_id)
            if error:
                QMessageBox.warning(self, "Error", error)
            else:
                QMessageBox.information(self, "Success", f"'{task_name}' has been deleted.")
                self._load_tasks(filter_status=self.current_filter)

    def _open_add_dialog(self):
        """Open dialog to add a new task."""
        courses = course_logic.get_all_courses()
        dialog = TaskDialog(self, courses=courses)
        if dialog.exec() == QDialog.Accepted:
            values = dialog.get_values()
            result, error = task_logic.create_task(**values)
            if error:
                QMessageBox.warning(self, "Error", error)
            else:
                QMessageBox.information(self, "Success", "Task added successfully!")
                self._load_tasks(filter_status=self.current_filter)

    def _open_edit_dialog(self, task_id):
        """Open dialog to edit an existing task."""
        task, error = task_logic.get_task_by_id(task_id)
        if error:
            QMessageBox.warning(self, "Error", error)
            return
        courses = course_logic.get_all_courses()
        dialog = TaskDialog(self, task=task, courses=courses)
        if dialog.exec() == QDialog.Accepted:
            values = dialog.get_values()
            result, error = task_logic.update_task(task_id, **values)
            if error:
                QMessageBox.warning(self, "Error", error)
            else:
                QMessageBox.information(self, "Success", "Task updated successfully!")
                self._load_tasks(filter_status=self.current_filter)


class TaskDialog(QDialog):
    """Dialog for adding or editing a task."""
    def __init__(self, parent=None, task=None, courses=None):
        super().__init__(parent)
        self.setWindowTitle("Add Task" if not task else "Edit Task")
        self.setMinimumWidth(450)
        self.courses = courses or []
        self._build_ui(task)

    def _build_ui(self, task):
        layout = QFormLayout(self)
        layout.setSpacing(12)

        # Task name
        self.name_input = QLineEdit(task[2] if task else "")
        self.name_input.setPlaceholderText("e.g. Assignment 1")
        layout.addRow("Task Name *", self.name_input)

        # Course dropdown
        self.course_combo = QComboBox()
        self.course_combo.addItem("— No Course —", None)
        for course in self.courses:
            self.course_combo.addItem(course[1], course[0])
        if task and task[1]:
            for i in range(self.course_combo.count()):
                if self.course_combo.itemData(i) == task[1]:
                    self.course_combo.setCurrentIndex(i)
                    break
        layout.addRow("Course", self.course_combo)

        # Due date
        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDisplayFormat("yyyy-MM-dd")
        if task and task[3]:
            self.due_date_input.setDate(QDate.fromString(task[3][:10], "yyyy-MM-dd"))
        else:
            self.due_date_input.setDate(QDate.currentDate())
        layout.addRow("Due Date *", self.due_date_input)

        # Priority dropdown
        self.priority_combo = QComboBox()
        for p in ["Low", "Medium", "High"]:
            self.priority_combo.addItem(p)
        if task:
            self.priority_combo.setCurrentText(task[5])
        else:
            self.priority_combo.setCurrentText("Medium")
        layout.addRow("Priority", self.priority_combo)

        # Estimated hours
        self.hours_input = QDoubleSpinBox()
        self.hours_input.setRange(0, 100)
        self.hours_input.setSingleStep(0.5)
        self.hours_input.setSuffix(" hrs")
        if task and task[6]:
            self.hours_input.setValue(task[6])
        layout.addRow("Estimated Hours", self.hours_input)

        # Status dropdown
        self.status_combo = QComboBox()
        for s in ["Not Started", "In Progress", "Done"]:
            self.status_combo.addItem(s)
        if task:
            self.status_combo.setCurrentText(task[7])
        layout.addRow("Status", self.status_combo)

        # Description
        self.description_input = QTextEdit(task[4] if task and task[4] else "")
        self.description_input.setPlaceholderText("Optional notes or details...")
        self.description_input.setMaximumHeight(80)
        layout.addRow("Description", self.description_input)

        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_values(self):
        return {
            "course_id": self.course_combo.currentData(),
            "task_name": self.name_input.text().strip(),
            "due_date": self.due_date_input.date().toString("yyyy-MM-dd"),
            "priority": self.priority_combo.currentText(),
            "estimated_hours": self.hours_input.value() or None,
            "task_description": self.description_input.toPlainText().strip() or None,
            "status": self.status_combo.currentText(),
        }