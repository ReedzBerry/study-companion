from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout,
    QVBoxLayout, QPushButton, QStackedWidget, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# Colour Palette
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

STYLESHEET = f"""
     QMainWindow {{
        background-color: {COLOURS['background']};
    }}
    QWidget#central_widget {{
        background-color: {COLOURS['background']};
    }}
    QWidget#sidebar {{
        background-color: {COLOURS['sidebar']};
        border-right: 1px solid {COLOURS['accent']};
    }}
    QLabel#app_title {{
        color: {COLOURS['text_primary']};
        font-size: 16px;
        font-weight: bold;
        padding: 20px 10px;
    }}
    QPushButton#nav_button {{
        background-color: transparent;
        color: {COLOURS['text_secondary']};
        border: none;
        text-align: left;
        padding: 12px 20px;
        font-size: 14px;
    }}
    QPushButton#nav_button:hover {{
        background-color: {COLOURS['accent']};
        color: {COLOURS['text_primary']};
    }}
    QPushButton#nav_button:checked {{
        background-color: {COLOURS['accent']};
        color: {COLOURS['text_primary']};
        border-left: 3px solid {COLOURS['text_primary']};
    }}
    QWidget#content_area {{
        background-color: {COLOURS['background']};
    }}
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Companion")
        self.setMinimumSize(1000, 650)
        self.setStyleSheet(STYLESHEET)
        self._build_ui()

    def _build_ui(self):
        # Central Widget
        central_widget = QWidget()
        central_widget.setObjectName("central_widget")
        self.setCentralWidget(central_widget)

        # Main horizontal layout - sidebar on left, content on right
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        # Build sidebar and content area
        main_layout.addWidget(self._build_sidebar())
        main_layout.addWidget(self._build_content_area())

    def _build_sidebar(self):
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(200)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        # App Title 
        title = QLabel("Study Companion")
        title.setObjectName("app_title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Navigation Buttons
        self.nav_buttons = []
        nav_items = [
            ("Dashboard", 0),
            ("Tasks", 1),
            ("Courses", 2),
            ("Planner", 3),
        ]

        for label, index in nav_items:
            btn = QPushButton(label)
            btn.setObjectName("nav_button")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, i=index: self._navigate(i))
            layout.addWidget(btn)
            self.nav_buttons.append(btn)

        # Push everything to the top
        layout.addStretch()

        return sidebar
    
    def _build_content_area(self):
        content_area = QWidget()
        content_area.setObjectName("content_area")

        layout = QVBoxLayout(content_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Stacked widget holds all views
        self.stack = QStackedWidget()
        self.stack.addWidget(QLabel("Dashboard — coming soon"))
        self.stack.addWidget(QLabel("Tasks — coming soon"))
        self.stack.addWidget(QLabel("Courses — coming soon"))
        self.stack.addWidget(QLabel("Planner — coming soon"))

        layout.addWidget(self.stack)
        return content_area

    def _navigate(self, index):
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)