import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from database.database_setup import initialise_database, get_connection
import seed_data

def is_database_empty():
    """Check if the database has any courses."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Courses")
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

def main():
    initialise_database()

    if is_database_empty():
        print("Seeding database with demo data...")
        seed_data.seed_data()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()