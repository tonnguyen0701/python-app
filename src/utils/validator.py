# Validator Utility
# Validation functions for data validation

import re


class Validator:
    """Validation utility class"""
    
    @staticmethod
    def is_valid_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_phone(phone):
        """Validate phone number"""
        pattern = r'^\+?[\d\s\-\(\)]{10,}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def is_valid_score(score):
        """Validate score value"""
        try:
            score_float = float(score)
            return 0 <= score_float <= 10
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_valid_name(name):
        """Validate student/subject name"""
        return isinstance(name, str) and len(name.strip()) > 0
    
    @staticmethod
    def is_valid_student_data(student_data):
        """Validate complete student data"""
        if not Validator.is_valid_name(student_data.get('name', '')):
            return False
        if student_data.get('email') and not Validator.is_valid_email(student_data['email']):
            return False
        if student_data.get('phone') and not Validator.is_valid_phone(student_data['phone']):
            return False
        return True
    
    @staticmethod
    def is_valid_score_data(score_data):
        """Validate complete score data"""
        if not Validator.is_valid_score(score_data.get('score_value')):
            return False
        if not isinstance(score_data.get('student_id'), int):
            return False
        if not isinstance(score_data.get('subject_id'), int):
            return False
        return True
