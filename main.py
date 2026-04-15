import os
import sys
from pathlib import Path

from src.ui.qt_compat import QtWidgets
from src.ui import (
    Ui_MainWindow,
    Ui_StudentWindow,
    Ui_TeacherWindow,
    Ui_SubjectWindow,
    Ui_ClassWindow,
    Ui_ScoreWindow,
    Ui_ReportWindow,
)

BASE_DIR = Path(__file__).resolve().parent
STYLE_PATH = BASE_DIR / "src" / "resources" / "styles.qss"


def load_stylesheet(app: QtWidgets.QApplication) -> None:
    if STYLE_PATH.exists():
        with STYLE_PATH.open("r", encoding="utf-8") as stylesheet_file:
            app.setStyleSheet(stylesheet_file.read())


class WindowManager:
    def __init__(self):
        self.student_window = None
        self.teacher_window = None
        self.subject_window = None
        self.class_window = None
        self.score_window = None
        self.report_window = None

    def show_student(self):
        self.student_window = self._create_window(Ui_StudentWindow, self.student_window)
        self.student_window.show()

    def show_teacher(self):
        self.teacher_window = self._create_window(Ui_TeacherWindow, self.teacher_window)
        self.teacher_window.show()

    def show_subject(self):
        self.subject_window = self._create_window(Ui_SubjectWindow, self.subject_window)
        self.subject_window.show()

    def show_class(self):
        self.class_window = self._create_window(Ui_ClassWindow, self.class_window)
        self.class_window.show()

    def show_score(self):
        self.score_window = self._create_window(Ui_ScoreWindow, self.score_window)
        self.score_window.show()

    def show_report(self):
        self.report_window = self._create_window(Ui_ReportWindow, self.report_window)
        self.report_window.show()

    def _create_window(self, ui_class, existing_window):
        if existing_window is None:
            window = QtWidgets.QMainWindow()
            ui = ui_class()
            ui.setupUi(window)
            if hasattr(ui, "closeButton"):
                ui.closeButton.clicked.connect(window.close)
            return window
        return existing_window


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, manager: WindowManager):
        super().__init__()
        self.manager = manager
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._connect_signals()

    def _connect_signals(self):
        self.ui.studentButton.clicked.connect(self.manager.show_student)
        self.ui.teacherButton.clicked.connect(self.manager.show_teacher)
        self.ui.subjectButton.clicked.connect(self.manager.show_subject)
        self.ui.classButton.clicked.connect(self.manager.show_class)
        self.ui.scoreButton.clicked.connect(self.manager.show_score)
        self.ui.reportButton.clicked.connect(self.manager.show_report)
        self.ui.logoutButton.clicked.connect(self.close)


def main():
    app = QtWidgets.QApplication(sys.argv)
    load_stylesheet(app)
    manager = WindowManager()
    main_window = MainWindow(manager)
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
