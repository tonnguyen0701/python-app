# Teacher Class Permission View
# UI for managing teacher permissions by class and subject

from PyQt6.QtWidgets import (QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
                             QPushButton, QListWidget, QListWidgetItem, QGroupBox, QCheckBox, QScrollArea)
from PyQt6.QtCore import Qt
from views.base_view import BaseTableView
from services.teacher_class_permission_service import TeacherClassPermissionService
from services.teacher_service import TeacherService
from services.class_service import ClassService
from services.subject_service import SubjectService
from models.teacher_class_permission import TeacherClassPermission


class TeacherClassPermissionView(BaseTableView):
    """View for managing teacher permissions"""

    def __init__(self):
        columns = ["Mã", "Giáo viên", "Lớp học", "Môn học", "Có quyền nhập điểm"]
        super().__init__(title="Phân quyền giáo viên", columns=columns)
        
        self.permission_service = TeacherClassPermissionService()
        self.teacher_service = TeacherService()
        self.class_service = ClassService()
        self.subject_service = SubjectService()
        self.add_search_bar("Nhập tên giáo viên, lớp hoặc môn...")
        self.on_refresh()

    def load_data(self):
        """Load permissions from service"""
        permissions = self.permission_service.get_all_permissions()
        
        def row_mapper(permission):
            teacher_name = ""
            class_name = ""
            subject_name = ""
            
            try:
                teacher = self.teacher_service.get_teacher(permission.teacher_id)
                teacher_name = teacher.name if teacher else ""
            except:
                pass
            try:
                classroom = self.class_service.get_class(permission.class_id)
                class_name = classroom.name if classroom else ""
            except:
                pass
            try:
                subject = self.subject_service.get_subject(permission.subject_id)
                subject_name = subject.name if subject else ""
            except:
                pass
            
            return [
                permission.permission_id,
                teacher_name,
                class_name,
                subject_name,
                "Có" if permission.can_enter_score else "Không"
            ]
        
        self.load_table_data(permissions, row_mapper)

    def on_add(self):
        """Add new permission"""
        dialog = TeacherClassPermissionDialog(self, self.teacher_service, self.class_service, 
                                             self.subject_service, self.permission_service)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()
                permission = TeacherClassPermission(**data)
                self.permission_service.create_permission(permission)
                self.on_refresh()
                QMessageBox.information(self, "Thành công", "Thêm quyền thành công!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Thêm quyền thất bại: {str(e)}")

    def on_edit(self):
        """Edit selected permission"""
        permission_id = self.get_selected_row_id()
        if permission_id is None:
            return
        
        try:
            permission = self.permission_service.get_permission(permission_id)
            dialog = TeacherClassPermissionDialog(self, self.teacher_service, self.class_service,
                                                 self.subject_service, self.permission_service, permission)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                updated_permission = TeacherClassPermission(permission_id=permission_id, **data)
                self.permission_service.update_permission(permission_id, updated_permission)
                self.on_refresh()
                QMessageBox.information(self, "Thành công", "Cập nhật quyền thành công!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Cập nhật quyền thất bại: {str(e)}")

    def on_delete(self):
        """Delete selected permission"""
        permission_id = self.get_selected_row_id()
        if permission_id is None:
            return
        
        reply = QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa quyền này?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.permission_service.delete_permission(permission_id)
                self.on_refresh()
                QMessageBox.information(self, "Thành công", "Xóa quyền thành công!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Xóa quyền thất bại: {str(e)}")

    def on_refresh(self):
        """Refresh permission list"""
        try:
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Tải quyền thất bại: {str(e)}")


class TeacherClassPermissionDialog(QDialog):
    """Dialog for adding/editing teacher class permission"""

    def __init__(self, parent=None, teacher_service=None, class_service=None,
                 subject_service=None, permission_service=None, permission=None):
        super().__init__(parent)
        self.permission = permission
        self.teacher_service = teacher_service
        self.class_service = class_service
        self.subject_service = subject_service
        self.permission_service = permission_service
        self.setWindowTitle("Thêm quyền" if permission is None else "Sửa quyền")
        self.setGeometry(100, 100, 500, 400)
        
        self.init_ui()
        
        if permission:
            self.load_permission_data(permission)

    def init_ui(self):
        """Initialize the UI"""
        main_layout = QVBoxLayout()
        
        # Teacher selection
        teacher_layout = QVBoxLayout()
        teacher_layout.addWidget(QLabel("Giáo viên:"))
        self.teacher_combo = QComboBox()
        self.teacher_combo.addItem("-- Chọn giáo viên --", None)
        if self.teacher_service:
            teachers = self.teacher_service.get_all_teachers()
            for teacher in teachers:
                self.teacher_combo.addItem(teacher.name, teacher.teacher_id)
        self.teacher_combo.currentIndexChanged.connect(self.on_teacher_changed)
        teacher_layout.addWidget(self.teacher_combo)
        main_layout.addLayout(teacher_layout)
        
        # Class selection
        class_layout = QVBoxLayout()
        class_layout.addWidget(QLabel("Lớp học:"))
        self.class_combo = QComboBox()
        self.class_combo.addItem("-- Chọn lớp học --", None)
        if self.class_service:
            classes = self.class_service.get_all_classes()
            for classroom in classes:
                self.class_combo.addItem(classroom.name, classroom.class_id)
        self.class_combo.currentIndexChanged.connect(self.on_class_changed)
        class_layout.addWidget(self.class_combo)
        main_layout.addLayout(class_layout)
        
        # Subject selection
        subject_label = QLabel("Môn học:")
        main_layout.addWidget(subject_label)
        
        self.subject_scroll = QScrollArea()
        self.subject_scroll.setWidgetResizable(True)
        self.subject_container = QGroupBox()
        self.subject_layout = QVBoxLayout()
        self.subject_checkboxes = {}
        
        if self.subject_service:
            subjects = self.subject_service.get_all_subjects()
            for subject in subjects:
                checkbox = QCheckBox(subject.name)
                checkbox.setData(Qt.ItemDataRole.UserRole, subject.subject_id)
                self.subject_layout.addWidget(checkbox)
                self.subject_checkboxes[subject.subject_id] = checkbox
        
        self.subject_layout.addStretch()
        self.subject_container.setLayout(self.subject_layout)
        self.subject_scroll.setWidget(self.subject_container)
        main_layout.addWidget(self.subject_scroll)
        
        # Permission checkbox
        self.can_enter_score_check = QCheckBox("Có quyền nhập điểm")
        self.can_enter_score_check.setChecked(True)
        main_layout.addWidget(self.can_enter_score_check)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("Xác nhận")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

    def on_teacher_changed(self):
        """Handle teacher selection change"""
        pass

    def on_class_changed(self):
        """Handle class selection change"""
        pass

    def load_permission_data(self, permission):
        """Load existing permission data"""
        if permission.teacher_id:
            index = self.teacher_combo.findData(permission.teacher_id)
            if index >= 0:
                self.teacher_combo.setCurrentIndex(index)
        
        if permission.class_id:
            index = self.class_combo.findData(permission.class_id)
            if index >= 0:
                self.class_combo.setCurrentIndex(index)
        
        if permission.subject_id in self.subject_checkboxes:
            self.subject_checkboxes[permission.subject_id].setChecked(True)
        
        self.can_enter_score_check.setChecked(permission.can_enter_score)

    def get_data(self):
        """Return dialog data as dictionary"""
        # Get selected subject
        subject_id = None
        for subject_id_key, checkbox in self.subject_checkboxes.items():
            if checkbox.isChecked():
                subject_id = subject_id_key
                break
        
        if subject_id is None:
            raise ValueError("Vui lòng chọn môn học")
        
        return {
            "teacher_id": self.teacher_combo.currentData(),
            "class_id": self.class_combo.currentData(),
            "subject_id": subject_id,
            "can_enter_score": self.can_enter_score_check.isChecked()
        }
