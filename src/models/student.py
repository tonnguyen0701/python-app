# Student Model
# Data class for Student entity

from datetime import datetime


class Student:
    """Student entity class"""
    
    def __init__(self, student_id=None, name="", date_of_birth=None, gender="", 
                 email="", phone="", address="", created_at=None):
        self.student_id = student_id
        self.name = name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.email = email
        self.phone = phone
        self.address = address
        self.created_at = created_at or datetime.now()
    
    def __repr__(self):
        return f"Student(id={self.student_id}, name={self.name})"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'date_of_birth': self.date_of_birth,
            'gender': self.gender,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at
        }
