import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication, QDialog
from main_window import MainWindow
from views.login_view import LoginDialog
from database.init_db import clear_database, init_database
from database.seed_data import seed_database


def main():
    if os.getenv("CLEAR_DB_ON_START") == "1":
        clear_database()
    init_database()
    
    # Auto-seed database with sample data if SEED_DB is set
    if os.getenv("SEED_DB_ON_START") == "1":
        try:
            seed_database()
        except Exception as e:
            print(f"⚠ Warning: Could not seed database: {e}")
    
    app = QApplication(sys.argv)
    
    # Show login dialog first
    login_dialog = LoginDialog()
    if login_dialog.exec() == QDialog.DialogCode.Accepted and login_dialog.authenticated:
        # Login successful - show main window
        w = MainWindow()
        w.show()
        sys.exit(app.exec())
    else:
        # Login failed or cancelled - exit app
        print("❌ Login failed or cancelled. Exiting...")
        sys.exit(0)


if __name__ == '__main__':
    main()
