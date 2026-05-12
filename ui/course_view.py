from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QTableWidget, 
    QTableWidgetItem, QHeaderView, QMessageBox,
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox
)
from PySide6.QtCore import Qt
from logic import course_logic

# Reuse colours from main window
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
    QPushButton#edit_button {{
        background-color: {COLOURS['card']};
        color: {COLOURS['text_primary']};
        min-width: 95px;
        max-width: 95px;
        min-height: 32px;
        max-height: 32px;
        font-size: 11px;
        border-radius: 4px;
        border: none;
        padding: 0px;
    }}
    QPushButton#edit_button:hover {{
        background-color: {COLOURS['accent']};
    }}
    QPushButton#delete_button {{
        background-color: {COLOURS['danger']};
        color: {COLOURS['text_primary']};
        min-width: 95px;
        max-width: 95px;
        min-height: 32px;
        max-height: 32px;
        font-size: 11px;
        border-radius: 4px;
        border: none;
        padding: 0px;
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
"""

class CourseView(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(VIEW_STYLE)
        self._build_ui()
        self._load_courses()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header row — title and add button
        header_layout = QHBoxLayout()
        title = QLabel("Courses")
        title.setObjectName("view_title")
        header_layout.addWidget(title)
        header_layout.addStretch()

        add_btn = QPushButton("+ Add Course")
        add_btn.setObjectName("add_button")
        add_btn.clicked.connect(self._open_add_dialog)
        header_layout.addWidget(add_btn)
        layout.addLayout(header_layout)

        # Course table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Course Name", "Code", "Created", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.table.horizontalHeader().resizeSection(3, 220)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

    def _load_courses(self):
        """Load all courses from the database and populate table"""
        courses = course_logic.get_all_courses()
        self.table.setRowCount(0)

        for course in courses:
            course_id = course[0]
            course_name = course[1]
            course_code = course[2] if course[2] else "-"
            created_at = course[3][:10] if course[3] else "-"

            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setRowHeight(row, 50)
            self.table.setItem(row, 0, QTableWidgetItem(course_name))
            self.table.setItem(row, 1, QTableWidgetItem(course_code))
            self.table.setItem(row, 2, QTableWidgetItem(created_at))

            # Action Buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4,4,4,4)
            actions_layout.setSpacing(6)

            edit_btn = QPushButton("Edit Course")
            edit_btn.setObjectName("edit_button")
            edit_btn.clicked.connect(lambda checked, cid=course_id, name=course_name, code=course[2]: self._open_edit_dialog(cid, name, code))

            delete_btn = QPushButton("Delete Course")
            delete_btn.setObjectName("delete_button")
            delete_btn.clicked.connect(lambda checked, cid=course_id, name=course_name: self._delete_course(cid, name))

            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch()
            self.table.setCellWidget(row, 3, actions_widget)

    def _open_add_dialog(self):
        """Open dialog to add a new course"""
        dialog = CourseDialog(self)
        if dialog.exec() == QDialog.Accepted:
            name, code = dialog.get_values()
            result, error = course_logic.create_course(name, code)
            if error:
                QMessageBox.warning(self, "Error", error)
            else:
                QMessageBox.information(self, "Success", f"Course Added Successfully!")
                self._load_courses()

    def _open_edit_dialog(self, course_id, course_name, course_code):
        """Open dialog to edit and existing course"""
        dialog = CourseDialog(self, course_name, course_code)
        if dialog.exec() == QDialog.Accepted:
            name, code = dialog.get_values()
            result, error = course_logic.update_course(course_id, name, code)
            if error:
                QMessageBox.warning(self, "Error", error)
            else:
                QMessageBox.information(self, "Success", f"Course Updated Successfully")
                self._load_courses()
    
    def _delete_course(self, course_id, course_name):
        """Confirm and delete a course."""
        reply = QMessageBox.question(
            self, "Delete Course",
            f"Are you sure you want to delete '{course_name}'?\nTasks linked to this course will not be deleted.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            result, error = course_logic.delete_course(course_id)
            if error:
                QMessageBox.warning(self, "Error", error)
            else:
                QMessageBox.information(self, "Success", f"'{course_name}' has been deleted.")
                self._load_courses()

class CourseDialog(QDialog):
    """Dialog for adding or editing a course"""
    def __init__(self, parent=None, course_name="", course_code=""):
        super().__init__(parent)
        self.setWindowTitle("Add Course" if not course_name else "Edit Course")
        self.setMinimumWidth(350)
        self._build_ui(course_name, course_code)

    def _build_ui(self, course_name, course_code):
        layout = QFormLayout(self)
        layout.setSpacing(12)

        self.name_input = QLineEdit(course_name)
        self.name_input.setPlaceholderText("e.g. Introduction Programming")
        layout.addRow("Course Name *", self.name_input)

        self.code_input = QLineEdit(course_code or '')
        self.code_input.setPlaceholderText("e.g. BIT601 (optional)")
        layout.addRow("Course Code", self.code_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_values(self):
        return self.name_input.text().strip(), self.code_input.text().strip() or None
 
