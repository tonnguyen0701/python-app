import os

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from views.student_view import StudentView
from views.teacher_view import TeacherView
from views.subject_view import SubjectView
from views.class_view import ClassView
from views.score_view import ScoreView
from views.report_view import ReportView
from views.teacher_class_permission_view import TeacherClassPermissionView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "ui", "main_window.ui")
        uic.loadUi(ui_path, self)

        self.student_view = None
        self.teacher_view = None
        self.subject_view = None
        self.class_view = None
        self.score_view = None
        self.report_view = None
        self.permission_view = None

        # Connect buttons
        self.connect_buttons()

    def connect_buttons(self):
        """Connect UI buttons to their handlers"""
        if hasattr(self, "studentButton"):
            self.studentButton.clicked.connect(self.open_student_view)
        if hasattr(self, "teacherButton"):
            self.teacherButton.clicked.connect(self.open_teacher_view)
        if hasattr(self, "subjectButton"):
            self.subjectButton.clicked.connect(self.open_subject_view)
        if hasattr(self, "classButton"):
            self.classButton.clicked.connect(self.open_class_view)
        if hasattr(self, "scoreButton"):
            self.scoreButton.clicked.connect(self.open_score_view)
        if hasattr(self, "reportButton"):
            self.reportButton.clicked.connect(self.open_report_view)
        if hasattr(self, "permissionButton"):
            self.permissionButton.clicked.connect(self.open_permission_view)
        if hasattr(self, "logoutButton"):
            self.logoutButton.clicked.connect(self.handle_logout)

    def open_student_view(self):
        """Open student management view"""
        try:
            if self.student_view is None or not self.student_view.isVisible():
                self.student_view = StudentView()
            self.student_view.show()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể mở giao diện quản lý học sinh: {str(e)}")

    def open_teacher_view(self):
        """Open teacher management view"""
        try:
            if self.teacher_view is None or not self.teacher_view.isVisible():
                self.teacher_view = TeacherView()
            self.teacher_view.show()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể mở giao diện quản lý giáo viên: {str(e)}")

    def open_subject_view(self):
        """Open subject management view"""
        try:
            if self.subject_view is None or not self.subject_view.isVisible():
                self.subject_view = SubjectView()
            self.subject_view.show()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể mở giao diện quản lý môn học: {str(e)}")

    def open_class_view(self):
        """Open class management view"""
        try:
            if self.class_view is None or not self.class_view.isVisible():
                self.class_view = ClassView()
            self.class_view.show()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể mở giao diện quản lý lớp học: {str(e)}")

    def open_score_view(self):
        """Open score management view"""
        try:
            if self.score_view is None or not self.score_view.isVisible():
                self.score_view = ScoreView()
            self.score_view.show()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể mở giao diện quản lý điểm: {str(e)}")

    def open_report_view(self):
        """Open report and statistics view"""
        try:
            if self.report_view is None or not self.report_view.isVisible():
                self.report_view = ReportView()
            self.report_view.show()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể mở giao diện báo cáo: {str(e)}")

    def open_permission_view(self):
        """Open teacher class permission management view"""
        try:
            if self.permission_view is None or not self.permission_view.isVisible():
                self.permission_view = TeacherClassPermissionView()
            self.permission_view.show()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể mở giao diện phân quyền giáo viên: {str(e)}")

    def handle_logout(self):
        """Handle logout - confirm and close to return to login"""
        reply = QMessageBox.question(self, "Đăng Xuất", 
                                    "Bạn có chắc chắn muốn đăng xuất?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            # Close all child windows
            if self.student_view and self.student_view.isVisible():
                self.student_view.close()
            if self.teacher_view and self.teacher_view.isVisible():
                self.teacher_view.close()
            if self.subject_view and self.subject_view.isVisible():
                self.subject_view.close()
            if self.class_view and self.class_view.isVisible():
                self.class_view.close()
            if self.score_view and self.score_view.isVisible():
                self.score_view.close()
            if self.report_view and self.report_view.isVisible():
                self.report_view.close()
            if self.permission_view and self.permission_view.isVisible():
                self.permission_view.close()
            
            print("✓ Đăng xuất thành công")
            self.close()
