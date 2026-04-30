# Helper Utility Functions
# Common helper functions

from datetime import datetime, date


class Helpers:
    """Helper utility class"""
    
    @staticmethod
    def format_date(date_obj, format_str="%d/%m/%Y"):
        """Format date to string"""
        if isinstance(date_obj, str):
            return date_obj
        if isinstance(date_obj, (datetime, date)):
            return date_obj.strftime(format_str)
        return str(date_obj)
    
    @staticmethod
    def parse_date(date_str, format_str="%d/%m/%Y"):
        """Parse string to date"""
        try:
            return datetime.strptime(date_str, format_str).date()
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def calculate_age(date_of_birth):
        """Calculate age from date of birth"""
        try:
            today = date.today()
            if isinstance(date_of_birth, str):
                dob = Helpers.parse_date(date_of_birth)
            else:
                dob = date_of_birth
            return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        except:
            return None
    
    @staticmethod
    def truncate_string(text, max_length=50):
        """Truncate string if too long"""
        if len(text) > max_length:
            return text[:max_length] + "..."
        return text
    
    @staticmethod
    def is_empty(value):
        """Check if value is empty"""
        return value is None or (isinstance(value, str) and len(value.strip()) == 0)
    
    @staticmethod
    def safe_divide(numerator, denominator, default=0):
        """Safe division to avoid division by zero"""
        try:
            return numerator / denominator if denominator != 0 else default
        except (TypeError, ValueError):
            return default
