# Class Controller
# Frontend logic for class management

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                             QDialog, QMessageBox, QHeaderView, QComboBox)
from PyQt6.QtCore import Qt
from services.class_service import ClassService
from services.teacher_service import TeacherService
from models.classroom import ClassRoom


class ClassController(QMainWindow):
    """Controller for class management"""

    def __init__(self):
        super().__init__()
        self.class_service = ClassService()
        self.teacher_service = TeacherService()
        self.init_ui()
        self.load_classes()

    def init_ui(self):
        """Initialize class UI"""
        self.setWindowTitle("Quản lý lớp học")
        self.setGeometry(100, 100, 800, 500)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Search bar
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Tìm kiếm:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nhập tên lớp...")
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Mã", "Tên lớp", "Khối", "Giáo viên chủ nhiệm", "Ngày tạo"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # Buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Thêm lớp")
        add_btn.clicked.connect(self.add_class)
        edit_btn = QPushButton("Sửa")
        edit_btn.clicked.connect(self.edit_class)
        delete_btn = QPushButton("Xóa")
        delete_btn.clicked.connect(self.delete_class)
        refresh_btn = QPushButton("Làm mới")
        refresh_btn.clicked.connect(self.load_classes)
        button_layout.addWidget(add_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(refresh_btn)
        layout.addLayout(button_layout)

        central_widget.setLayout(layout)

    def load_classes(self):
        """Load classes from database"""
        classes = self.class_service.get_all_classes()
        self.table.setRowCount(0)
        for cls in classes:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(cls.class_id)))
            self.table.setItem(row, 1, QTableWidgetItem(cls.name))
            self.table.setItem(row, 2, QTableWidgetItem(str(cls.grade_level or "")))
            
            teacher_name = ""
            if cls.homeroom_teacher_id:
                teacher = self.teacher_service.get_teacher(cls.homeroom_teacher_id)
                if teacher:
                    teacher_name = teacher.name
            self.table.setItem(row, 3, QTableWidgetItem(teacher_name))
            self.table.setItem(row, 4, QTableWidgetItem(str(cls.created_at)[:10]))

    def add_class(self):
        """Show dialog to add new class"""
        dialog = ClassDialog(self, self.teacher_service)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            class_data = dialog.get_data()
            cls = ClassRoom(**class_data)
            self.class_service.create_class(cls)
            self.load_classes()
            QMessageBox.information(self, "Thành công", "Thêm lớp thành công!")

    def edit_class(self):
        """Edit selected class"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một lớp!")
            return
        class_id = int(self.table.item(row, 0).text())
        cls = self.class_service.get_class(class_id)
        dialog = ClassDialog(self, self.teacher_service, cls)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_data()
            updated_class = ClassRoom(class_id=class_id, **updated_data)
            self.class_service.update_class(class_id, updated_class)
            self.load_classes()
            QMessageBox.information(self, "Thành công", "Cập nhật lớp thành công!")

    def delete_class(self):
        """Delete selected class"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một lớp!")
            return
        class_id = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(self, "Xác nhận", "Xóa lớp học này?")
        if reply == QMessageBox.StandardButton.Yes:
            self.class_service.delete_class(class_id)
            self.load_classes()
            QMessageBox.information(self, "Thành công", "Xóa lớp thành công!")


class ClassDialog(QDialog):
    """Dialog for adding/editing class"""

    def __init__(self, parent=None, teacher_service=None, classroom=None):
        super().__init__(parent)
        self.classroom = classroom
        self.teacher_service = teacher_service
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Tên lớp
        layout.addWidget(QLabel("Tên lớp:"))
        self.name_input = QLineEdit()
        if self.classroom:
            self.name_input.setText(self.classroom.name)
        layout.addWidget(self.name_input)

        # Khối
        layout.addWidget(QLabel("Khối:"))
        self.grade_input = QLineEdit()
        if self.classroom:
            self.grade_input.setText(str(self.classroom.grade_level or ""))
        layout.addWidget(self.grade_input)

        # Giáo viên chủ nhiệm
        layout.addWidget(QLabel("Giáo viên chủ nhiệm:"))
        self.teacher_combo = QComboBox()
        teachers = self.teacher_service.get_all_teachers()
        self.teacher_combo.addItem("Chọn giáo viên", None)
        for teacher in teachers:
            self.teacher_combo.addItem(teacher.name, teacher.teacher_id)
        if self.classroom and self.classroom.homeroom_teacher_id:
            for i in range(self.teacher_combo.count()):
                if self.teacher_combo.itemData(i) == self.classroom.homeroom_teacher_id:
                    self.teacher_combo.setCurrentIndex(i)
                    break
        layout.addWidget(self.teacher_combo)

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
        self.setWindowTitle("Thông tin lớp học")

    def get_data(self):
        return {
            'name': self.name_input.text(),
            'grade_level': int(self.grade_input.text()) if self.grade_input.text() else None,
            'homeroom_teacher_id': self.teacher_combo.currentData()
        }
