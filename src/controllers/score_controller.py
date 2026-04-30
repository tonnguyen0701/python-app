# Score Controller
# Handle score management logic

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                             QDialog, QMessageBox, QHeaderView, QComboBox)
from PyQt6.QtCore import Qt
from services.score_service import ScoreService
from services.student_service import StudentService
from services.subject_service import SubjectService
from services.rule_service import RuleService
from models.score import Score


class ScoreController(QMainWindow):
    """Controller for score management"""

    def __init__(self):
        super().__init__()
        self.score_service = ScoreService()
        self.student_service = StudentService()
        self.subject_service = SubjectService()
        self.rule_service = RuleService()
        self.init_ui()
        self.load_scores()

    def init_ui(self):
        """Initialize score UI"""
        self.setWindowTitle("Quản lý điểm")
        self.setGeometry(100, 100, 1000, 500)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Filter bar
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Học sinh:"))
        self.student_combo = QComboBox()
        self.student_combo.addItem("Tất cả học sinh", None)
        for student in self.student_service.get_all_students():
            self.student_combo.addItem(student.name, student.student_id)
        self.student_combo.currentIndexChanged.connect(self.load_scores)
        filter_layout.addWidget(self.student_combo)
        layout.addLayout(filter_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Mã", "Student", "Môn học", "Điểm giữa kỳ", "Điểm cuối kỳ", "Học kỳ", "Xếp loại"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # Buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Thêm điểm")
        add_btn.clicked.connect(self.add_score)
        edit_btn = QPushButton("Sửa")
        edit_btn.clicked.connect(self.edit_score)
        delete_btn = QPushButton("Xóa")
        delete_btn.clicked.connect(self.delete_score)
        calc_btn = QPushButton("Tính trung bình")
        calc_btn.clicked.connect(self.calculate_average)
        refresh_btn = QPushButton("Làm mới")
        refresh_btn.clicked.connect(self.load_scores)
        button_layout.addWidget(add_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(calc_btn)
        button_layout.addWidget(refresh_btn)
        layout.addLayout(button_layout)

        central_widget.setLayout(layout)

    def load_scores(self):
        """Load scores from database"""
        student_id = self.student_combo.currentData()
        if student_id:
            scores = self.score_service.get_scores_by_student(student_id)
        else:
            # Load all scores
            from database.db_connect import DatabaseConnection
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM scores ORDER BY created_at DESC")
            rows = cursor.fetchall()
            scores = [self.score_service._row_to_score(r) for r in rows] if rows else []

        self.table.setRowCount(0)
        for score in scores:
            row = self.table.rowCount()
            self.table.insertRow(row)

            student = self.student_service.get_student(score.student_id)
            subject = self.subject_service.get_subject(score.subject_id)
            rating = self.rule_service.classify_student(score.score_value)

            self.table.setItem(row, 0, QTableWidgetItem(str(score.score_id)))
            self.table.setItem(row, 1, QTableWidgetItem(student.name if student else ""))
            self.table.setItem(row, 2, QTableWidgetItem(subject.name if subject else ""))
            self.table.setItem(row, 3, QTableWidgetItem(f"{score.midterm_score:.1f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{score.final_score:.1f}"))
            self.table.setItem(row, 5, QTableWidgetItem(score.semester or ""))
            self.table.setItem(row, 6, QTableWidgetItem(rating))

    def add_score(self):
        """Show dialog to add new score"""
        dialog = ScoreDialog(self, self.student_service, self.subject_service)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            score = Score(**data)
            self.score_service.add_score(score)
            self.load_scores()
            QMessageBox.information(self, "Thành công", "Thêm điểm thành công!")

    def edit_score(self):
        """Edit selected score"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn điểm!")
            return
        score_id = int(self.table.item(row, 0).text())
        score = self.score_service.get_score(score_id)
        dialog = ScoreDialog(self, self.student_service, self.subject_service, score)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            updated_score = Score(score_id=score_id, **data)
            self.score_service.update_score(score_id, updated_score)
            self.load_scores()
            QMessageBox.information(self, "Thành công", "Cập nhật điểm thành công!")

    def delete_score(self):
        """Delete selected score"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn điểm!")
            return
        score_id = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa điểm này?")
        if reply == QMessageBox.StandardButton.Yes:
            self.score_service.delete_score(score_id)
            self.load_scores()
            QMessageBox.information(self, "Thành công", "Xóa điểm thành công!")

    def calculate_average(self):
        """Calculate average score for selected student"""
        student_id = self.student_combo.currentData()
        if not student_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn học sinh!")
            return
        scores = self.score_service.get_scores_by_student(student_id)
        if not scores:
            QMessageBox.information(self, "Thông tin", "Không tìm thấy điểm cho học sinh này!")
            return
        score_values = [s.score_value for s in scores]
        avg = self.rule_service.calculate_gpa(score_values)
        rating = self.rule_service.classify_student(avg)
        QMessageBox.information(self, "Kết quả", f"Điểm trung bình: {avg:.2f}\nXếp loại: {rating}")


class ScoreDialog(QDialog):
    """Dialog for adding/editing score"""

    def __init__(self, parent=None, student_service=None, subject_service=None, score=None):
        super().__init__(parent)
        self.score = score
        self.student_service = student_service
        self.subject_service = subject_service
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Student
        layout.addWidget(QLabel("Học sinh:"))
        self.student_combo = QComboBox()
        students = self.student_service.get_all_students()
        for student in students:
            self.student_combo.addItem(student.name, student.student_id)
        if self.score:
            for i in range(self.student_combo.count()):
                if self.student_combo.itemData(i) == self.score.student_id:
                    self.student_combo.setCurrentIndex(i)
                    break
        layout.addWidget(self.student_combo)

        # Môn học
        layout.addWidget(QLabel("Môn học:"))
        self.subject_combo = QComboBox()
        subjects = self.subject_service.get_all_subjects()
        for subject in subjects:
            self.subject_combo.addItem(subject.name, subject.subject_id)
        if self.score:
            for i in range(self.subject_combo.count()):
                if self.subject_combo.itemData(i) == self.score.subject_id:
                    self.subject_combo.setCurrentIndex(i)
                    break
        layout.addWidget(self.subject_combo)

        # Midterm score
        layout.addWidget(QLabel("Điểm giữa kỳ (0-10):"))
        self.midterm_input = QLineEdit()
        if self.score:
            self.midterm_input.setText(str(self.score.midterm_score))
        layout.addWidget(self.midterm_input)

        # Final score
        layout.addWidget(QLabel("Điểm cuối kỳ (0-10):"))
        self.final_input = QLineEdit()
        if self.score:
            self.final_input.setText(str(self.score.final_score))
        layout.addWidget(self.final_input)

        # Học kỳ
        layout.addWidget(QLabel("Học kỳ:"))
        self.semester_input = QLineEdit()
        if self.score:
            self.semester_input.setText(self.score.semester or "")
        layout.addWidget(self.semester_input)

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
        self.setWindowTitle("Thông tin điểm")

    def get_data(self):
        return {
            'student_id': self.student_combo.currentData(),
            'subject_id': self.subject_combo.currentData(),
            'midterm_score': float(self.midterm_input.text()),
            'final_score': float(self.final_input.text()),
            'semester': self.semester_input.text()
        }
