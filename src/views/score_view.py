# Score View
# UI for score management

from PyQt6.QtWidgets import (QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QDoubleSpinBox, QComboBox, QGroupBox, QSpinBox)
from PyQt6.QtCore import Qt, pyqtSignal
from views.base_view import BaseTableView
from services.score_service import ScoreService
from services.student_service import StudentService
from services.subject_service import SubjectService
from services.teacher_service import TeacherService
from services.class_service import ClassService
from services.teacher_class_permission_service import TeacherClassPermissionService
from services.enrollment_service import EnrollmentService
from models.score import Score


class ScoreView(BaseTableView):
    """View for managing scores"""

    def __init__(self):
        columns = ["Mã", "Học sinh", "Lớp học", "Môn học", "Điểm giữa kỳ", "Điểm cuối kỳ", "Học kỳ", "GV"]
        super().__init__(title="Quản lý điểm", columns=columns)
        
        self.score_service = ScoreService()
        self.student_service = StudentService()
        self.subject_service = SubjectService()
        self.teacher_service = TeacherService()
        self.class_service = ClassService()
        self.enrollment_service = EnrollmentService()
        self.permission_service = TeacherClassPermissionService()
        self.add_search_bar("Nhập tên học sinh hoặc môn học...")
        self.on_refresh()

    def load_data(self):
        """Load scores from service"""
        scores = self.score_service.get_all_scores()
        
        def row_mapper(score):
            student_name = ""
            class_name = ""
            subject_name = ""
            teacher_name = ""
            try:
                student = self.student_service.get_student(score.student_id)
                student_name = student.name if student else ""
            except:
                pass
            try:
                classroom = self.enrollment_service.get_class_by_student(score.student_id, score.semester)
                class_name = classroom.name if classroom else ""
            except:
                pass
            try:
                subject = self.subject_service.get_subject(score.subject_id)
                subject_name = subject.name if subject else ""
            except:
                pass
            # Try to get teacher info from score if available
            if hasattr(score, 'teacher_id') and score.teacher_id:
                try:
                    teacher = self.teacher_service.get_teacher(score.teacher_id)
                    teacher_name = teacher.name if teacher else ""
                except:
                    pass
            return [
                score.score_id,
                student_name,
                class_name,
                subject_name,
                f"{score.midterm_score:.2f}",
                f"{score.final_score:.2f}",
                score.semester or "",
                teacher_name
            ]
        
        self.load_table_data(scores, row_mapper)

    def on_add(self):
        """Add new score"""
        dialog = ScoreDialog(self, self.student_service, self.subject_service, 
                           self.teacher_service, self.class_service, self.permission_service,
                           enrollment_service=self.enrollment_service)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()
                
                # Validate required fields
                if not data.get("student_id"):
                    QMessageBox.warning(self, "Lỗi", "Vui lòng chọn học sinh!")
                    return
                if not data.get("subject_id"):
                    QMessageBox.warning(self, "Lỗi", "Vui lòng chọn môn học!")
                    return
                
                # Ensure enrollment exists for selected class/semester
                class_id = data.get("class_id")
                semester = data.get("semester")
                student_id = data.get("student_id")
                if class_id and student_id and self.enrollment_service:
                    try:
                        existing = self.enrollment_service.get_enrollment_by_student_and_semester(student_id, semester)
                        if not existing:
                            self.enrollment_service.create_enrollment(student_id, class_id, semester)
                        else:
                            try:
                                # existing is a DB row: (enrollment_id, student_id, class_id, semester, created_at)
                                existing_class_id = existing[2]
                                if existing_class_id != class_id:
                                    self.enrollment_service.delete_enrollment(existing[0])
                                    self.enrollment_service.create_enrollment(student_id, class_id, semester)
                            except Exception:
                                pass
                    except Exception:
                        pass

                # Remove class_id from data before creating Score object (Score model doesn't have class_id)
                data.pop("class_id", None)
                score = Score(**data)
                self.score_service.create_score(score)
                self.on_refresh()
                QMessageBox.information(self, "Thành công", "Thêm điểm thành công!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Thêm điểm thất bại: {str(e)}")

    def on_edit(self):
        """Edit selected score"""
        score_id = self.get_selected_row_id()
        if score_id is None:
            return
        
        try:
            score = self.score_service.get_score(score_id)
            dialog = ScoreDialog(self, self.student_service, self.subject_service,
                               self.teacher_service, self.class_service, self.permission_service, score,
                               enrollment_service=self.enrollment_service)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                
                # Validate required fields
                if not data.get("student_id"):
                    QMessageBox.warning(self, "Lỗi", "Vui lòng chọn học sinh!")
                    return
                if not data.get("subject_id"):
                    QMessageBox.warning(self, "Lỗi", "Vui lòng chọn môn học!")
                    return
                
                # Ensure enrollment exists/updated for selected class when editing
                class_id = data.get("class_id")
                semester = data.get("semester")
                student_id = data.get("student_id")
                if class_id and student_id and self.enrollment_service:
                    try:
                        existing = self.enrollment_service.get_enrollment_by_student_and_semester(student_id, semester)
                        if not existing:
                            self.enrollment_service.create_enrollment(student_id, class_id, semester)
                        else:
                            try:
                                existing_class_id = existing[2]
                                if existing_class_id != class_id:
                                    self.enrollment_service.delete_enrollment(existing[0])
                                    self.enrollment_service.create_enrollment(student_id, class_id, semester)
                            except Exception:
                                pass
                    except Exception:
                        pass

                # Remove class_id from data before creating Score object (Score model doesn't have class_id)
                data.pop("class_id", None)
                updated_score = Score(score_id=score_id, **data)
                self.score_service.update_score(score_id, updated_score)
                self.on_refresh()
                QMessageBox.information(self, "Thành công", "Cập nhật điểm thành công!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Cập nhật điểm thất bại: {str(e)}")

    def on_delete(self):
        """Delete selected score"""
        score_id = self.get_selected_row_id()
        if score_id is None:
            return
        
        reply = QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa điểm này?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.score_service.delete_score(score_id)
                self.on_refresh()
                QMessageBox.information(self, "Thành công", "Xóa điểm thành công!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Xóa điểm thất bại: {str(e)}")

    def on_refresh(self):
        """Refresh score list"""
        try:
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Tải điểm thất bại: {str(e)}")


class ScoreDialog(QDialog):
    """Dialog for adding/editing score with teacher permissions"""

    def __init__(self, parent=None, student_service=None, subject_service=None, 
                 teacher_service=None, class_service=None, permission_service=None, score=None,
                 enrollment_service=None):
        super().__init__(parent)
        self.score = score
        self.student_service = student_service
        self.subject_service = subject_service
        self.teacher_service = teacher_service
        self.class_service = class_service
        self.permission_service = permission_service
        if enrollment_service is None:
            from services.enrollment_service import EnrollmentService
            self.enrollment_service = EnrollmentService()
        else:
            self.enrollment_service = enrollment_service
        self.setWindowTitle("Thêm điểm" if score is None else "Sửa điểm")
        self.setGeometry(100, 100, 600, 500)
        
        self.init_ui()
        
        # If adding new score, select first student and first subject if available
        if not score:
            if self.student_combo.count() > 1:  # More than just "-- Chọn học sinh --"
                self.student_combo.setCurrentIndex(1)
            if self.subject_combo.count() > 1:  # More than just "-- Chọn môn học --"
                self.subject_combo.setCurrentIndex(1)
        elif score:
            # If editing existing score, load its data
            self.load_score_data(score)

    def init_ui(self):
        """Initialize the UI"""
        main_layout = QVBoxLayout()
        
        # Score information group
        score_group = QGroupBox("Thông tin điểm")
        score_layout = QVBoxLayout()
        
        # Student
        score_layout.addWidget(QLabel("Học sinh:"))
        self.student_combo = QComboBox()
        self.student_combo.addItem("-- Chọn học sinh --", None)
        if self.student_service:
            students = self.student_service.get_all_students()
            for student in students:
                self.student_combo.addItem(student.name, student.student_id)
        # Connect after populating
        self.student_combo.currentIndexChanged.connect(self.on_student_changed)
        score_layout.addWidget(self.student_combo)

        # Class (auto-filled based on student)
        score_layout.addWidget(QLabel("Lớp học:"))
        self.class_combo = QComboBox()
        self.class_combo.addItem("-- Chọn lớp học --", None)
        # Populate all available classes as fallback options
        if self.class_service:
            try:
                all_classes = self.class_service.get_all_classes()
                for classroom in all_classes:
                    self.class_combo.addItem(classroom.name, classroom.class_id)
            except:
                pass
        score_layout.addWidget(self.class_combo)

        # Subject
        score_layout.addWidget(QLabel("Môn học:"))
        self.subject_combo = QComboBox()
        # Populate all subjects BEFORE connecting signal
        self.subject_combo.blockSignals(True)
        self.subject_combo.addItem("-- Chọn môn học --", None)
        if self.subject_service:
            try:
                all_subjects = self.subject_service.get_all_subjects()
                for subject in all_subjects:
                    self.subject_combo.addItem(subject.name, subject.subject_id)
            except:
                pass
        self.subject_combo.blockSignals(False)
        # Connect after populating and blocking signals
        self.subject_combo.currentIndexChanged.connect(self.on_subject_changed)
        score_layout.addWidget(self.subject_combo)
        
        # Midterm score
        midterm_layout = QHBoxLayout()
        midterm_layout.addWidget(QLabel("Điểm giữa kỳ:"))
        self.midterm_input = QDoubleSpinBox()
        self.midterm_input.setMinimum(0.0)
        self.midterm_input.setMaximum(10.0)
        self.midterm_input.setDecimals(2)
        self.midterm_input.setSingleStep(0.5)
        midterm_layout.addWidget(self.midterm_input)
        score_layout.addLayout(midterm_layout)

        # Final score
        final_layout = QHBoxLayout()
        final_layout.addWidget(QLabel("Điểm cuối kỳ:"))
        self.final_input = QDoubleSpinBox()
        self.final_input.setMinimum(0.0)
        self.final_input.setMaximum(10.0)
        self.final_input.setDecimals(2)
        self.final_input.setSingleStep(0.5)
        final_layout.addWidget(self.final_input)
        score_layout.addLayout(final_layout)

        # Semester
        semester_layout = QHBoxLayout()
        semester_layout.addWidget(QLabel("Học kỳ:"))
        self.semester_input = QSpinBox()
        self.semester_input.setMinimum(1)
        self.semester_input.setMaximum(2)
        self.semester_input.setValue(1)
        self.semester_input.valueChanged.connect(self.on_semester_changed)
        semester_layout.addWidget(self.semester_input)
        score_layout.addLayout(semester_layout)
        
        score_group.setLayout(score_layout)
        main_layout.addWidget(score_group)
        
        # Teacher selection group
        teacher_group = QGroupBox("Thông tin giáo viên (tùy chọn)")
        teacher_layout = QVBoxLayout()
        
        teacher_layout.addWidget(QLabel("Giáo viên:"))
        self.teacher_combo = QComboBox()
        self.teacher_combo.addItem("-- Không chọn --", None)
        if self.teacher_service:
            teachers = self.teacher_service.get_all_teachers()
            for teacher in teachers:
                self.teacher_combo.addItem(teacher.name, teacher.teacher_id)
        teacher_layout.addWidget(self.teacher_combo)
        
        teacher_group.setLayout(teacher_layout)
        main_layout.addWidget(teacher_group)

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

    def on_subject_changed(self):
        """Handle subject selection change"""
        pass

    def on_student_changed(self):
        """Handle student selection change - populate class"""
        student_id = self.student_combo.currentData()
        semester = self.semester_input.value()
        
        if student_id and self.enrollment_service:
            try:
                # Get class of student
                classroom = self.enrollment_service.get_class_by_student(student_id, semester)
                if classroom:
                    # Set the class combo to the student's class but keep it enabled for manual override
                    index = self.class_combo.findData(classroom.class_id)
                    if index >= 0:
                        self.class_combo.setCurrentIndex(index)
            except:
                pass

    def on_semester_changed(self):
        """Handle semester change - refresh class info"""
        student_id = self.student_combo.currentData()
        semester = self.semester_input.value()
        
        # Update class based on new semester
        if student_id and self.enrollment_service:
            try:
                classroom = self.enrollment_service.get_class_by_student(student_id, semester)
                if classroom:
                    index = self.class_combo.findData(classroom.class_id)
                    if index >= 0:
                        self.class_combo.setCurrentIndex(index)
            except:
                pass

    def load_score_data(self, score):
        """Load existing score data"""
        if score.midterm_score:
            self.midterm_input.setValue(score.midterm_score)
        if score.final_score:
            self.final_input.setValue(score.final_score)
        if score.semester:
            try:
                self.semester_input.setValue(int(score.semester))
            except:
                pass
        
        # Set student first
        if score.student_id:
            index = self.student_combo.findData(score.student_id)
            if index >= 0:
                self.student_combo.setCurrentIndex(index)
                # This will trigger on_student_changed to populate class
        
        # Set subject (after subjects are populated)
        if score.subject_id:
            # Try to find subject in combo
            index = self.subject_combo.findData(score.subject_id)
            if index >= 0:
                self.subject_combo.setCurrentIndex(index)
            else:
                # If not found, add it
                subject = self.subject_service.get_subject(score.subject_id)
                if subject:
                    self.subject_combo.addItem(subject.name, subject.subject_id)
                    index = self.subject_combo.findData(score.subject_id)
                    if index >= 0:
                        self.subject_combo.setCurrentIndex(index)
        
        # Set teacher
        if score.teacher_id:
            index = self.teacher_combo.findData(score.teacher_id)
            if index >= 0:
                self.teacher_combo.setCurrentIndex(index)

    def get_data(self):
        """Return dialog data as dictionary"""
        return {
            "student_id": self.student_combo.currentData(),
            "subject_id": self.subject_combo.currentData(),
            "class_id": self.class_combo.currentData(),
            "midterm_score": self.midterm_input.value(),
            "final_score": self.final_input.value(),
            "semester": self.semester_input.value(),
            "teacher_id": self.teacher_combo.currentData()
        }

