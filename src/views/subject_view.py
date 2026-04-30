# Môn học View
# UI for subject management

from PyQt6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox
from PyQt6.QtCore import Qt
from views.base_view import BaseTableView
from services.subject_service import SubjectService
from models.subject import Subject


class SubjectView(BaseTableView):
    """View for managing subjects"""

    def __init__(self):
        columns = ["Mã", "Tên", "Lớp học", "Ca học", "Ngày học"]
        super().__init__(title="Quản lý môn học", columns=columns)
        
        self.subject_service = SubjectService()
        self.add_search_bar("Nhập tên hoặc mã môn học...")
        self.on_refresh()

    def load_data(self):
        """Load subjects from service"""
        subjects = self.subject_service.get_all_subjects()
        
        def row_mapper(subject):
            return [
                subject.subject_id,
                subject.name,
                subject.class_name or "",
                subject.class_shift or "",
                subject.class_day or ""
            ]
        
        self.load_table_data(subjects, row_mapper)

    def on_add(self):
        """Add new subject"""
        dialog = SubjectDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()
                subject = Subject(**data)
                self.subject_service.create_subject(subject)
                self.on_refresh()
                QMessageBox.information(self, "Thành công", "Thêm môn học thành công!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Thêm môn học thất bại: {str(e)}")

    def on_edit(self):
        """Edit selected subject"""
        subject_id = self.get_selected_row_id()
        if subject_id is None:
            return
        
        try:
            subject = self.subject_service.get_subject(subject_id)
            dialog = SubjectDialog(self, subject)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                updated_subject = Subject(subject_id=subject_id, **data)
                self.subject_service.update_subject(subject_id, updated_subject)
                self.on_refresh()
                QMessageBox.information(self, "Thành công", "Cập nhật môn học thành công!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Cập nhật môn học thất bại: {str(e)}")

    def on_delete(self):
        """Delete selected subject"""
        subject_id = self.get_selected_row_id()
        if subject_id is None:
            return
        
        reply = QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa môn học này?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.subject_service.delete_subject(subject_id)
                self.on_refresh()
                QMessageBox.information(self, "Thành công", "Xóa môn học thành công!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Xóa môn học thất bại: {str(e)}")

    def on_refresh(self):
        """Refresh subject list"""
        try:
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Tải môn học thất bại: {str(e)}")


class SubjectDialog(QDialog):
    """Dialog for adding/editing subject"""

    def __init__(self, parent=None, subject=None):
        super().__init__(parent)
        self.subject = subject
        self.setWindowTitle("Thêm môn học" if subject is None else f"Sửa môn học - {subject.name}")
        self.setGeometry(200, 200, 400, 150)
        
        layout = QVBoxLayout()

        # Name
        layout.addWidget(QLabel("Tên:"))
        self.name_input = QLineEdit()
        if subject:
            self.name_input.setText(subject.name)
        layout.addWidget(self.name_input)

        # Lớp học
        layout.addWidget(QLabel("Lớp học:"))
        self.class_name_input = QLineEdit()
        if subject:
            self.class_name_input.setText(subject.class_name or "")
        layout.addWidget(self.class_name_input)

        # Ca học
        layout.addWidget(QLabel("Ca học:"))
        self.class_shift_input = QLineEdit()
        if subject:
            self.class_shift_input.setText(subject.class_shift or "")
        layout.addWidget(self.class_shift_input)

        # Ngày học
        layout.addWidget(QLabel("Ngày học:"))
        self.class_day_input = QLineEdit()
        if subject:
            self.class_day_input.setText(subject.class_day or "")
        layout.addWidget(self.class_day_input)

        # Mã
        layout.addWidget(QLabel("Mã:"))
        self.code_input = QLineEdit()
        if subject:
            self.code_input.setText(subject.code)
        layout.addWidget(self.code_input)

        # Số tín chỉ
        layout.addWidget(QLabel("Số tín chỉ:"))
        self.credit_input = QSpinBox()
        self.credit_input.setMinimum(0)
        self.credit_input.setMaximum(20)
        if subject:
            self.credit_input.setValue(subject.credit or 0)
        layout.addWidget(self.credit_input)

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
            "class_name": self.class_name_input.text(),
            "class_shift": self.class_shift_input.text(),
            "class_day": self.class_day_input.text(),
            "code": self.code_input.text(),
            "credit": self.credit_input.value()
        }
