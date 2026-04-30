# Score Model
# Data class for Score entity

from datetime import datetime


class Score:
    """Score entity class"""
    
    def __init__(self, score_id=None, student_id=None, subject_id=None, 
                 score_value=None, midterm_score=0.0, final_score=0.0,
                 semester=None, teacher_id=None, created_at=None):
        self.score_id = score_id
        self.student_id = student_id
        self.subject_id = subject_id
        self.midterm_score = midterm_score if midterm_score is not None else 0.0
        self.final_score = final_score if final_score is not None else 0.0
        self.semester = semester
        self.teacher_id = teacher_id
        self.created_at = created_at or datetime.now()
        self._score_value = self._compute_score_value(score_value)

    def _compute_score_value(self, score_value):
        if score_value is not None:
            return score_value
        return (self.midterm_score + self.final_score) / 2 if self.midterm_score is not None and self.final_score is not None else 0.0

    @property
    def score_value(self):
        return self._score_value

    def __repr__(self):
        return (f"Score(id={self.score_id}, student={self.student_id}, "
                f"midterm={self.midterm_score}, final={self.final_score})")
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'score_id': self.score_id,
            'student_id': self.student_id,
            'subject_id': self.subject_id,
            'score_value': self.score_value,
            'midterm_score': self.midterm_score,
            'final_score': self.final_score,
            'semester': self.semester,
            'teacher_id': self.teacher_id,
            'created_at': self.created_at
        }
