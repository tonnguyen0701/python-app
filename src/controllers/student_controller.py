# Student Controller
# Handle student management logic

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                             QDialog, QMessageBox, QHeaderView, QComboBox)
from PyQt6.QtCore import Qt
from services.student_service import StudentService
from models.student import Student


class StudentController(QMainWindow):
    """Controller for student management"""

    def __init__(self):
        super().__init__()
        self.student_service = StudentService()
        self.init_ui()
        self.load_students()

    def init_ui(self):
        """Initialize student UI"""
        self.setWindowTitle("Quản lý học sinh")
        self.setGeometry(100, 100, 900, 500)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Search bar
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Tìm kiếm:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nhập tên hoặc email học sinh...")
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Mã", "Name", "DOB", "Gender", "Email", "Phone", "Address"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # Buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Add Student")
        add_btn.clicked.connect(self.add_student)
        edit_btn = QPushButton("Sửa")
        edit_btn.clicked.connect(self.edit_student)
        delete_btn = QPushButton("Xóa")
        delete_btn.clicked.connect(self.delete_student)
        refresh_btn = QPushButton("Làm mới")
        refresh_btn.clicked.connect(self.load_students)
        button_layout.addWidget(add_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(refresh_btn)
        layout.addLayout(button_layout)

        central_widget.setLayout(layout)

    def load_students(self):
        """Load students from database"""
        students = self.student_service.get_all_students()
        self.table.setRowCount(0)
        for student in students:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(student.student_id)))
            self.table.setItem(row, 1, QTableWidgetItem(student.name))
            self.table.setItem(row, 2, QTableWidgetItem(str(student.date_of_birth or "")))
            self.table.setItem(row, 3, QTableWidgetItem(student.gender or ""))
            self.table.setItem(row, 4, QTableWidgetItem(student.email or ""))
            self.table.setItem(row, 5, QTableWidgetItem(student.phone or ""))
            self.table.setItem(row, 6, QTableWidgetItem(student.address or ""))

    def add_student(self):
        """Show dialog to add new student"""
        dialog = StudentDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            student = Student(**data)
            self.student_service.create_student(student)
            self.load_students()
            QMessageBox.information(self, "Thành công", "Thêm học sinh thành công!")

    def edit_student(self):
        """Edit selected student"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn học sinh!")
            return
        student_id = int(self.table.item(row, 0).text())
        student = self.student_service.get_student(student_id)
        dialog = StudentDialog(self, student)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            updated_student = Student(student_id=student_id, **data)
            self.student_service.update_student(student_id, updated_student)
            self.load_students()
            QMessageBox.information(self, "Thành công", "Cập nhật học sinh thành công!")

    def delete_student(self):
        """Delete selected student"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn học sinh!")
            return
        student_id = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(self, "Xác nhận", "Xóa học sinh này?")
        if reply == QMessageBox.StandardButton.Yes:
            self.student_service.delete_student(student_id)
            self.load_students()
            QMessageBox.information(self, "Thành công", "Xóa học sinh thành công!")


class StudentDialog(QDialog):
    """Dialog for adding/editing student"""

    def __init__(self, parent=None, student=None):
        super().__init__(parent)
        self.student = student
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Name
        layout.addWidget(QLabel("Tên:"))
        self.name_input = QLineEdit()
        if self.student:
            self.name_input.setText(self.student.name)
        layout.addWidget(self.name_input)

        # Date of Birth
        layout.addWidget(QLabel("Ngày sinh (YYYY-MM-DD):"))
        self.dob_input = QLineEdit()
        if self.student:
            self.dob_input.setText(str(self.student.date_of_birth or ""))
        layout.addWidget(self.dob_input)

        # Gender
        layout.addWidget(QLabel("Giới tính:"))
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["", "Nam", "Nữ", "Khác"])
        if self.student:
            self.gender_combo.setCurrentText(self.student.gender or "")
        layout.addWidget(self.gender_combo)

        # Email
        layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        if self.student:
            self.email_input.setText(self.student.email or "")
        layout.addWidget(self.email_input)

        # Phone
        layout.addWidget(QLabel("Phone:"))
        self.phone_input = QLineEdit()
        if self.student:
            self.phone_input.setText(self.student.phone or "")
        layout.addWidget(self.phone_input)

        # Address
        layout.addWidget(QLabel("Địa chỉ:"))
        self.address_input = QLineEdit()
        if self.student:
            self.address_input.setText(self.student.address or "")
        layout.addWidget(self.address_input)

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
        self.setWindowTitle("Thông tin học sinh")

    def get_data(self):
        return {
            'name': self.name_input.text(),
            'date_of_birth': self.dob_input.text() or None,
            'gender': self.gender_combo.currentText(),
            'email': self.email_input.text(),
            'phone': self.phone_input.text(),
            'address': self.address_input.text()
        }
