# Class View
# UI for class management

from PyQt6.QtWidgets import (QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QSpinBox, QComboBox)
from PyQt6.QtCore import Qt
from views.base_view import BaseTableView
from services.class_service import ClassService
from services.teacher_service import TeacherService
from models.classroom import ClassRoom


class ClassView(BaseTableView):
    """View for managing classes"""

    def __init__(self):
        columns = ["Mã", "Tên", "Khối", "Giáo viên chủ nhiệm"]
        super().__init__(title="Quản lý lớp học", columns=columns)
        
        self.class_service = ClassService()
        self.teacher_service = TeacherService()
        self.add_search_bar("Nhập tên lớp...")
        self.on_refresh()

    def load_data(self):
        """Load classes from service"""
        classes = self.class_service.get_all_classes()
        
        def row_mapper(cls):
            teacher_name = ""
            if cls.homeroom_teacher_id:
                try:
                    teacher = self.teacher_service.get_teacher(cls.homeroom_teacher_id)
                    teacher_name = teacher.name if teacher else ""
                except:
                    pass
            return [
                cls.class_id,
                cls.name,
                cls.grade_level or "",
                teacher_name
            ]
        
        self.load_table_data(classes, row_mapper)

    def on_add(self):
        """Add new class"""
        dialog = ClassDialog(self, self.teacher_service)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()
                cls = ClassRoom(**data)
                self.class_service.create_class(cls)
                self.on_refresh()
                QMessageBox.information(self, "Thành công", "Thêm lớp thành công!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Thêm lớp thất bại: {str(e)}")

    def on_edit(self):
        """Edit selected class"""
        class_id = self.get_selected_row_id()
        if class_id is None:
            return
        
        try:
            cls = self.class_service.get_class(class_id)
            dialog = ClassDialog(self, self.teacher_service, cls)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                updated_class = ClassRoom(class_id=class_id, **data)
                self.class_service.update_class(class_id, updated_class)
                self.on_refresh()
                QMessageBox.information(self, "Thành công", "Cập nhật lớp thành công!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Cập nhật lớp thất bại: {str(e)}")

    def on_delete(self):
        """Delete selected class"""
        class_id = self.get_selected_row_id()
        if class_id is None:
            return
        
        reply = QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa lớp học này?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.class_service.delete_class(class_id)
                self.on_refresh()
                QMessageBox.information(self, "Thành công", "Xóa lớp thành công!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Xóa lớp thất bại: {str(e)}")

    def on_refresh(self):
        """Refresh class list"""
        try:
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Tải lớp thất bại: {str(e)}")


class ClassDialog(QDialog):
    """Dialog for adding/editing class"""

    def __init__(self, parent=None, teacher_service=None, classroom=None):
        super().__init__(parent)
        self.classroom = classroom
        self.teacher_service = teacher_service
        self.setWindowTitle("Thêm lớp" if classroom is None else f"Sửa lớp - {classroom.name}")
        self.setGeometry(200, 200, 400, 150)
        
        layout = QVBoxLayout()

        # Name
        layout.addWidget(QLabel("Tên:"))
        self.name_input = QLineEdit()
        if classroom:
            self.name_input.setText(classroom.name)
        layout.addWidget(self.name_input)

        # Khối
        layout.addWidget(QLabel("Khối:"))
        self.grade_input = QSpinBox()
        self.grade_input.setMinimum(1)
        self.grade_input.setMaximum(12)
        if classroom:
            self.grade_input.setValue(classroom.grade_level or 10)
        layout.addWidget(self.grade_input)

        # Giáo viên chủ nhiệm
        layout.addWidget(QLabel("Giáo viên chủ nhiệm:"))
        self.teacher_combo = QComboBox()
        self.teacher_combo.addItem("Không chọn", None)
        if teacher_service:
            teachers = teacher_service.get_all_teachers()
            for teacher in teachers:
                self.teacher_combo.addItem(teacher.name, teacher.teacher_id)
        if classroom and classroom.homeroom_teacher_id:
            index = self.teacher_combo.findData(classroom.homeroom_teacher_id)
            if index >= 0:
                self.teacher_combo.setCurrentIndex(index)
        layout.addWidget(self.teacher_combo)

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
            "grade_level": self.grade_input.value(),
            "homeroom_teacher_id": self.teacher_combo.currentData()
        }
