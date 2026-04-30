# Teacher Model
# Data class for Teacher entity

from datetime import datetime


class Teacher:
    """Teacher entity class"""

    def __init__(self, teacher_id=None, name="", email="", phone="", department="", created_at=None):
        self.teacher_id = teacher_id
        self.name = name
        self.email = email
        self.phone = phone
        self.department = department
        self.created_at = created_at or datetime.now()

    def __repr__(self):
        return f"Teacher(id={self.teacher_id}, name={self.name})"

    def to_dict(self):
        return {
            'teacher_id': self.teacher_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'department': self.department,
            'created_at': self.created_at
        }
