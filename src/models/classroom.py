# ClassRoom Model
# Data class for Class/Grade entity

from datetime import datetime


class ClassRoom:
    """Classroom entity class"""

    def __init__(self, class_id=None, name="", grade_level=None, homeroom_teacher_id=None, created_at=None):
        self.class_id = class_id
        self.name = name
        self.grade_level = grade_level
        self.homeroom_teacher_id = homeroom_teacher_id
        self.created_at = created_at or datetime.now()

    def __repr__(self):
        return f"ClassRoom(id={self.class_id}, name={self.name})"

    def to_dict(self):
        return {
            'class_id': self.class_id,
            'name': self.name,
            'grade_level': self.grade_level,
            'homeroom_teacher_id': self.homeroom_teacher_id,
            'created_at': self.created_at
        }
