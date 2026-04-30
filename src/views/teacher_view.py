# Teacher View
# UI for teacher management

from PyQt6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from views.base_view import BaseTableView
from services.teacher_service import TeacherService
from models.teacher import Teacher


class TeacherView(BaseTableView):
    """View for managing teachers"""

    def __init__(self):
        columns = ["Mã", "Tên", "Email", "Số điện thoại", "Bộ môn"]
        super().__init__(title="Quản lý giáo viên", columns=columns)
        
        self.teacher_service = TeacherService()
        self.add_search_bar("Nhập tên hoặc email giáo viên...")
        self.on_refresh()

    def load_data(self):
        """Load teachers from service"""
        teachers = self.teacher_service.get_all_teachers()
        
        def row_mapper(teacher):
            return [
                teacher.teacher_id,
                teacher.name,
                teacher.email or "",
                teacher.phone or "",
                teacher.department or ""
            ]
        
        self.load_table_data(teachers, row_mapper)

    def on_add(self):
        """Add new teacher"""
        dialog = TeacherDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()
                teacher = Teacher(**data)
                self.teacher_service.create_teacher(teacher)
                self.on_refresh()
                QMessageBox.information(self, "Thành công", "Thêm giáo viên thành công!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Thêm giáo viên thất bại: {str(e)}")

    def on_edit(self):
        """Edit selected teacher"""
        teacher_id = self.get_selected_row_id()
        if teacher_id is None:
            return
        
        try:
            teacher = self.teacher_service.get_teacher(teacher_id)
            dialog = TeacherDialog(self, teacher)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                updated_teacher = Teacher(teacher_id=teacher_id, **data)
                self.teacher_service.update_teacher(teacher_id, updated_teacher)
                self.on_refresh()
                QMessageBox.information(self, "Thành công", "Cập nhật giáo viên thành công!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Cập nhật giáo viên thất bại: {str(e)}")

    def on_delete(self):
        """Delete selected teacher"""
        teacher_id = self.get_selected_row_id()
        if teacher_id is None:
            return
        
        reply = QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa giáo viên này?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.teacher_service.delete_teacher(teacher_id)
                self.on_refresh()
                QMessageBox.information(self, "Thành công", "Xóa giáo viên thành công!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Xóa giáo viên thất bại: {str(e)}")

    def on_refresh(self):
        """Refresh teacher list"""
        try:
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Tải giáo viên thất bại: {str(e)}")


class TeacherDialog(QDialog):
    """Dialog for adding/editing teacher"""

    def __init__(self, parent=None, teacher=None):
        super().__init__(parent)
        self.teacher = teacher
        self.setWindowTitle("Thêm giáo viên" if teacher is None else f"Sửa giáo viên - {teacher.name}")
        self.setGeometry(200, 200, 400, 200)
        
        layout = QVBoxLayout()

        # Name
        layout.addWidget(QLabel("Tên:"))
        self.name_input = QLineEdit()
        if teacher:
            self.name_input.setText(teacher.name)
        layout.addWidget(self.name_input)

        # Email
        layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        if teacher:
            self.email_input.setText(teacher.email or "")
        layout.addWidget(self.email_input)

        # Phone
        layout.addWidget(QLabel("Điện thoại:"))
        self.phone_input = QLineEdit()
        if teacher:
            self.phone_input.setText(teacher.phone or "")
        layout.addWidget(self.phone_input)

        # Bộ môn
        layout.addWidget(QLabel("Bộ môn:"))
        self.department_input = QLineEdit()
        if teacher:
            self.department_input.setText(teacher.department or "")
        layout.addWidget(self.department_input)

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
            "email": self.email_input.text() or None,
            "phone": self.phone_input.text() or None,
            "department": self.department_input.text() or None
        }
