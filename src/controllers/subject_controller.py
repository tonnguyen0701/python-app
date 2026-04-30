# Môn học Controller
# Handle subject management logic

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                             QDialog, QMessageBox, QHeaderView)
from PyQt6.QtCore import Qt
from services.subject_service import SubjectService
from models.subject import Subject


class SubjectController(QMainWindow):
    """Controller for subject management"""

    def __init__(self):
        super().__init__()
        self.subject_service = SubjectService()
        self.init_ui()
        self.load_subjects()

    def init_ui(self):
        """Initialize subject UI"""
        self.setWindowTitle("Quản lý môn học")
        self.setGeometry(100, 100, 700, 400)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Search bar
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Tìm kiếm:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nhập tên môn học...")
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Mã", "Tên môn học", "Mã", "Số tín chỉ"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # Buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Thêm môn học")
        add_btn.clicked.connect(self.add_subject)
        edit_btn = QPushButton("Sửa")
        edit_btn.clicked.connect(self.edit_subject)
        delete_btn = QPushButton("Xóa")
        delete_btn.clicked.connect(self.delete_subject)
        refresh_btn = QPushButton("Làm mới")
        refresh_btn.clicked.connect(self.load_subjects)
        button_layout.addWidget(add_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(refresh_btn)
        layout.addLayout(button_layout)

        central_widget.setLayout(layout)

    def load_subjects(self):
        """Load subjects from database"""
        subjects = self.subject_service.get_all_subjects()
        self.table.setRowCount(0)
        for subject in subjects:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(subject.subject_id)))
            self.table.setItem(row, 1, QTableWidgetItem(subject.name))
            self.table.setItem(row, 2, QTableWidgetItem(subject.code))
            self.table.setItem(row, 3, QTableWidgetItem(str(subject.credit or "")))

    def add_subject(self):
        """Show dialog to add new subject"""
        dialog = SubjectDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            subject = Subject(**data)
            self.subject_service.create_subject(subject)
            self.load_subjects()
            QMessageBox.information(self, "Thành công", "Thêm môn học thành công!")

    def edit_subject(self):
        """Edit selected subject"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn môn học!")
            return
        subject_id = int(self.table.item(row, 0).text())
        subject = self.subject_service.get_subject(subject_id)
        dialog = SubjectDialog(self, subject)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            updated_subject = Subject(subject_id=subject_id, **data)
            self.subject_service.update_subject(subject_id, updated_subject)
            self.load_subjects()
            QMessageBox.information(self, "Thành công", "Cập nhật môn học thành công!")

    def delete_subject(self):
        """Delete selected subject"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn môn học!")
            return
        subject_id = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(self, "Xác nhận", "Xóa môn học này?")
        if reply == QMessageBox.StandardButton.Yes:
            self.subject_service.delete_subject(subject_id)
            self.load_subjects()
            QMessageBox.information(self, "Thành công", "Xóa môn học thành công!")


class SubjectDialog(QDialog):
    """Dialog for adding/editing subject"""

    def __init__(self, parent=None, subject=None):
        super().__init__(parent)
        self.subject = subject
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Name
        layout.addWidget(QLabel("Tên môn học:"))
        self.name_input = QLineEdit()
        if self.subject:
            self.name_input.setText(self.subject.name)
        layout.addWidget(self.name_input)

        # Mã
        layout.addWidget(QLabel("Mã:"))
        self.code_input = QLineEdit()
        if self.subject:
            self.code_input.setText(self.subject.code)
        layout.addWidget(self.code_input)

        # Số tín chỉ
        layout.addWidget(QLabel("Số tín chỉ:"))
        self.credit_input = QLineEdit()
        if self.subject:
            self.credit_input.setText(str(self.subject.credit or ""))
        layout.addWidget(self.credit_input)

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
        self.setWindowTitle("Thông tin môn học")

    def get_data(self):
        return {
            'name': self.name_input.text(),
            'code': self.code_input.text(),
            'credit': int(self.credit_input.text()) if self.credit_input.text() else None
        }
