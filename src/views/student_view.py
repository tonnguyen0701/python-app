# Student View
# UI for student management

from PyQt6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from PyQt6.QtCore import Qt
from views.base_view import BaseTableView
from services.student_service import StudentService
from models.student import Student


class StudentView(BaseTableView):
    """View for managing students"""

    def __init__(self):
        columns = ["Mã", "Tên", "Ngày sinh", "Giới tính", "Email", "Số điện thoại", "Địa chỉ"]
        super().__init__(title="Quản lý học sinh", columns=columns)
        
        self.student_service = StudentService()
        self.add_search_bar("Nhập tên hoặc email học sinh...")
        self.on_refresh()

    def load_data(self):
        """Load students from service"""
        students = self.student_service.get_all_students()
        
        def row_mapper(student):
            return [
                student.student_id,
                student.name,
                student.date_of_birth or "",
                student.gender or "",
                student.email or "",
                student.phone or "",
                student.address or ""
            ]
        
        self.load_table_data(students, row_mapper)

    def on_add(self):
        """Add new student"""
        dialog = StudentDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()
                student = Student(**data)
                self.student_service.create_student(student)
                self.on_refresh()
                QMessageBox.information(self, "Thành công", "Thêm học sinh thành công!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Thêm học sinh thất bại: {str(e)}")

    def on_edit(self):
        """Edit selected student"""
        student_id = self.get_selected_row_id()
        if student_id is None:
            return
        
        try:
            student = self.student_service.get_student(student_id)
            dialog = StudentDialog(self, student)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                updated_student = Student(student_id=student_id, **data)
                self.student_service.update_student(student_id, updated_student)
                self.on_refresh()
                QMessageBox.information(self, "Thành công", "Cập nhật học sinh thành công!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Cập nhật học sinh thất bại: {str(e)}")

    def on_delete(self):
        """Delete selected student"""
        student_id = self.get_selected_row_id()
        if student_id is None:
            return
        
        reply = QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa học sinh này?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.student_service.delete_student(student_id)
                self.on_refresh()
                QMessageBox.information(self, "Thành công", "Xóa học sinh thành công!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Xóa học sinh thất bại: {str(e)}")

    def on_refresh(self):
        """Refresh student list"""
        try:
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Tải học sinh thất bại: {str(e)}")


class StudentDialog(QDialog):
    """Dialog for adding/editing student"""

    def __init__(self, parent=None, student=None):
        super().__init__(parent)
        self.student = student
        self.setWindowTitle("Học sinh" if student is None else f"Sửa học sinh - {student.name}")
        self.setGeometry(200, 200, 400, 300)
        
        layout = QVBoxLayout()

        # Name
        layout.addWidget(QLabel("Tên:"))
        self.name_input = QLineEdit()
        if student:
            self.name_input.setText(student.name)
        layout.addWidget(self.name_input)

        # DOB
        layout.addWidget(QLabel("Ngày sinh:"))
        self.dob_input = QLineEdit()
        if student:
            self.dob_input.setText(str(student.date_of_birth or ""))
        layout.addWidget(self.dob_input)

        # Gender
        layout.addWidget(QLabel("Giới tính:"))
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Nam", "Nữ", "Khác"])
        if student and student.gender:
            self.gender_combo.setCurrentText(student.gender)
        layout.addWidget(self.gender_combo)

        # Email
        layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        if student:
            self.email_input.setText(student.email or "")
        layout.addWidget(self.email_input)

        # Phone
        layout.addWidget(QLabel("Điện thoại:"))
        self.phone_input = QLineEdit()
        if student:
            self.phone_input.setText(student.phone or "")
        layout.addWidget(self.phone_input)

        # Address
        layout.addWidget(QLabel("Địa chỉ:"))
        self.address_input = QLineEdit()
        if student:
            self.address_input.setText(student.address or "")
        layout.addWidget(self.address_input)

        # Buttons
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("Xác nhận")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_data(self):
        """Return dialog data as dictionary"""
        return {
            "name": self.name_input.text(),
            "date_of_birth": self.dob_input.text() if self.dob_input.text() else None,
            "gender": self.gender_combo.currentText(),
            "email": self.email_input.text() or None,
            "phone": self.phone_input.text() or None,
            "address": self.address_input.text() or None
        }
