# Subject Service
# Business logic for subject management

from database.subject_dao import SubjectDAO


class SubjectService:
    """Business logic for subject operations"""
    
    def __init__(self):
        self.subject_dao = SubjectDAO()
    
    def create_subject(self, subject_data):
        """Create new subject"""
        # TODO: Validate subject data
        return self.subject_dao.insert(subject_data)
    
    def get_subject(self, subject_id):
        """Get subject by ID"""
        return self.subject_dao.find_by_id(subject_id)
    
    def get_all_subjects(self):
        """Get all subjects"""
        return self.subject_dao.find_all()
    
    def update_subject(self, subject_id, subject_data):
        """Update subject information"""
        # TODO: Validate subject data
        return self.subject_dao.update(subject_id, subject_data)
    
    def delete_subject(self, subject_id):
        """Delete subject"""
        return self.subject_dao.delete(subject_id)
