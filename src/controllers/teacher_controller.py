# Teacher Controller
# Frontend logic for teacher management

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                             QDialog, QMessageBox, QHeaderView)
from PyQt6.QtCore import Qt
from services.teacher_service import TeacherService
from models.teacher import Teacher


class TeacherController(QMainWindow):
    """Controller for teacher management"""

    def __init__(self):
        super().__init__()
        self.teacher_service = TeacherService()
        self.init_ui()
        self.load_teachers()

    def init_ui(self):
        """Initialize teacher UI"""
        self.setWindowTitle("Quản lý giáo viên")
        self.setGeometry(100, 100, 800, 500)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Search bar
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Tìm kiếm:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nhập tên giáo viên...")
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Mã", "Name", "Email", "Phone", "Bộ môn"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # Buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Thêm giáo viên")
        add_btn.clicked.connect(self.add_teacher)
        edit_btn = QPushButton("Sửa")
        edit_btn.clicked.connect(self.edit_teacher)
        delete_btn = QPushButton("Xóa")
        delete_btn.clicked.connect(self.delete_teacher)
        refresh_btn = QPushButton("Làm mới")
        refresh_btn.clicked.connect(self.load_teachers)
        button_layout.addWidget(add_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(refresh_btn)
        layout.addLayout(button_layout)

        central_widget.setLayout(layout)

    def load_teachers(self):
        """Load teachers from database"""
        teachers = self.teacher_service.get_all_teachers()
        self.table.setRowCount(0)
        for teacher in teachers:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(teacher.teacher_id)))
            self.table.setItem(row, 1, QTableWidgetItem(teacher.name))
            self.table.setItem(row, 2, QTableWidgetItem(teacher.email or ""))
            self.table.setItem(row, 3, QTableWidgetItem(teacher.phone or ""))
            self.table.setItem(row, 4, QTableWidgetItem(teacher.department or ""))

    def add_teacher(self):
        """Show dialog to add new teacher"""
        dialog = TeacherDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            teacher_data = dialog.get_data()
            teacher = Teacher(**teacher_data)
            self.teacher_service.create_teacher(teacher)
            self.load_teachers()
            QMessageBox.information(self, "Thành công", "Thêm giáo viên thành công!")

    def edit_teacher(self):
        """Edit selected teacher"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn giáo viên!")
            return
        teacher_id = int(self.table.item(row, 0).text())
        teacher = self.teacher_service.get_teacher(teacher_id)
        dialog = TeacherDialog(self, teacher)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_data()
            updated_teacher = Teacher(teacher_id=teacher_id, **updated_data)
            self.teacher_service.update_teacher(teacher_id, updated_teacher)
            self.load_teachers()
            QMessageBox.information(self, "Thành công", "Cập nhật giáo viên thành công!")

    def delete_teacher(self):
        """Delete selected teacher"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn giáo viên!")
            return
        teacher_id = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(self, "Xác nhận", "Xóa giáo viên này?")
        if reply == QMessageBox.StandardButton.Yes:
            self.teacher_service.delete_teacher(teacher_id)
            self.load_teachers()
            QMessageBox.information(self, "Thành công", "Xóa giáo viên thành công!")


class TeacherDialog(QDialog):
    """Dialog for adding/editing teacher"""

    def __init__(self, parent=None, teacher=None):
        super().__init__(parent)
        self.teacher = teacher
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Name
        layout.addWidget(QLabel("Tên:"))
        self.name_input = QLineEdit()
        if self.teacher:
            self.name_input.setText(self.teacher.name)
        layout.addWidget(self.name_input)

        # Email
        layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        if self.teacher:
            self.email_input.setText(self.teacher.email)
        layout.addWidget(self.email_input)

        # Phone
        layout.addWidget(QLabel("Phone:"))
        self.phone_input = QLineEdit()
        if self.teacher:
            self.phone_input.setText(self.teacher.phone)
        layout.addWidget(self.phone_input)

        # Bộ môn
        layout.addWidget(QLabel("Bộ môn:"))
        self.department_input = QLineEdit()
        if self.teacher:
            self.department_input.setText(self.teacher.department)
        layout.addWidget(self.department_input)

        # Buttons
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("Xác nhận")
        cancel_btn = QPushButton("Hủy")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setWindowTitle("Thông tin giáo viên")

    def get_data(self):
        return {
            'name': self.name_input.text(),
            'email': self.email_input.text(),
            'phone': self.phone_input.text(),
            'department': self.department_input.text()
        }
