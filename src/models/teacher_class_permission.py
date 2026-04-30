# Teacher Class Permission Model
# Data class for Teacher-Class-Subject Permission entity

from datetime import datetime


class TeacherClassPermission:
    """Teacher Class Permission entity class"""

    def __init__(self, permission_id=None, teacher_id=None, class_id=None, 
                 subject_id=None, can_enter_score=True, created_at=None):
        self.permission_id = permission_id
        self.teacher_id = teacher_id
        self.class_id = class_id
        self.subject_id = subject_id
        self.can_enter_score = can_enter_score
        self.created_at = created_at or datetime.now()

    def __repr__(self):
        return f"TeacherClassPermission(id={self.permission_id}, teacher={self.teacher_id}, class={self.class_id}, subject={self.subject_id})"

    def to_dict(self):
        return {
            'permission_id': self.permission_id,
            'teacher_id': self.teacher_id,
            'class_id': self.class_id,
            'subject_id': self.subject_id,
            'can_enter_score': self.can_enter_score,
            'created_at': self.created_at
        }
