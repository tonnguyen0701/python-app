# Semester Model
# Data class for Semester entity

from datetime import datetime


class Semester:
    """Semester entity class"""
    
    def __init__(self, semester_id=None, name="", start_date=None, end_date=None, created_at=None):
        self.semester_id = semester_id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.created_at = created_at or datetime.now()
    
    def __repr__(self):
        return f"Semester(id={self.semester_id}, name={self.name})"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'semester_id': self.semester_id,
            'name': self.name,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'created_at': self.created_at
        }
