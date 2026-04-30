# Enrollment Service
# Business logic for enrollment management

from database.enrollment_dao import EnrollmentDAO


class EnrollmentService:
    """Business logic for enrollment operations"""
    
    def __init__(self):
        self.enrollment_dao = EnrollmentDAO()
    
    def get_class_by_student(self, student_id, semester=None):
        """Get class for a student"""
        return self.enrollment_dao.find_class_by_student(student_id, semester)
    
    def get_enrollments_by_student(self, student_id):
        """Get all enrollments for a student"""
        return self.enrollment_dao.find_by_student_id(student_id)
    
    def get_enrollment_by_student_and_semester(self, student_id, semester):
        """Get enrollment for a student in a specific semester"""
        return self.enrollment_dao.find_by_student_and_semester(student_id, semester)
    
    def create_enrollment(self, student_id, class_id, semester=None):
        """Create new enrollment"""
        return self.enrollment_dao.insert(student_id, class_id, semester)
    
    def delete_enrollment(self, enrollment_id):
        """Delete enrollment"""
        return self.enrollment_dao.delete(enrollment_id)
