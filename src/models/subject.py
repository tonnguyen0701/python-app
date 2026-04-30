# Subject Model
# Data class for Subject entity

from datetime import datetime


class Subject:
    """Subject entity class"""
    
    def __init__(self, subject_id=None, name="", code="", credit=0,
                 class_name="", class_shift="", class_day="", created_at=None):
        self.subject_id = subject_id
        self.name = name
        self.code = code
        self.credit = credit
        self.class_name = class_name
        self.class_shift = class_shift
        self.class_day = class_day
        self.created_at = created_at or datetime.now()
    
    def __repr__(self):
        return f"Subject(id={self.subject_id}, name={self.name})"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'subject_id': self.subject_id,
            'name': self.name,
            'code': self.code,
            'credit': self.credit,
            'class_name': self.class_name,
            'class_shift': self.class_shift,
            'class_day': self.class_day,
            'created_at': self.created_at
        }
