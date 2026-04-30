# Student Service
# Business logic for student management

from database.student_dao import StudentDAO


class StudentService:
    """Business logic for student operations"""
    
    def __init__(self):
        self.student_dao = StudentDAO()
    
    def create_student(self, student_data):
        """Create new student"""
        # TODO: Validate student data
        return self.student_dao.insert(student_data)
    
    def get_student(self, student_id):
        """Get student by ID"""
        return self.student_dao.find_by_id(student_id)
    
    def get_all_students(self):
        """Get all students"""
        return self.student_dao.find_all()
    
    def update_student(self, student_id, student_data):
        """Update student information"""
        # TODO: Validate student data
        return self.student_dao.update(student_id, student_data)
    
    def delete_student(self, student_id):
        """Delete student"""
        return self.student_dao.delete(student_id)
    
    def search_students(self, keyword):
        """Search students by keyword"""
        return self.student_dao.search(keyword)
