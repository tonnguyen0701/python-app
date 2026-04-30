# Teacher Class Permission Service
# Business logic for teacher class permission management

from database.teacher_class_permission_dao import TeacherClassPermissionDAO


class TeacherClassPermissionService:
    """Business logic for teacher class permission operations"""
    
    def __init__(self):
        self.dao = TeacherClassPermissionDAO()
    
    def create_permission(self, permission):
        """Create a new permission"""
        return self.dao.insert(permission)
    
    def get_permission(self, permission_id):
        """Get permission by ID"""
        return self.dao.find_by_id(permission_id)
    
    def get_all_permissions(self):
        """Get all permissions"""
        return self.dao.find_all()
    
    def get_permissions_by_teacher(self, teacher_id):
        """Get all permissions for a teacher"""
        return self.dao.find_by_teacher(teacher_id)
    
    def get_permissions_by_teacher_class(self, teacher_id, class_id):
        """Get permissions for teacher in a specific class"""
        return self.dao.find_by_teacher_and_class(teacher_id, class_id)
    
    def check_permission(self, teacher_id, subject_id, class_id):
        """Check if teacher has permission for subject in class"""
        return self.dao.find_by_teacher_subject_class(teacher_id, subject_id, class_id) is not None
    
    def update_permission(self, permission_id, permission):
        """Update permission"""
        return self.dao.update(permission_id, permission)
    
    def delete_permission(self, permission_id):
        """Delete permission"""
        return self.dao.delete(permission_id)
    
    def delete_permissions_by_teacher_class(self, teacher_id, class_id):
        """Delete all permissions for teacher in a class"""
        return self.dao.delete_by_teacher_and_class(teacher_id, class_id)
    
    def get_teacher_subjects(self, teacher_id):
        """Get all subjects assigned to a teacher"""
        permissions = self.dao.find_by_teacher(teacher_id)
        subjects = {}
        for perm in permissions:
            if perm.subject_id not in subjects:
                subjects[perm.subject_id] = []
            subjects[perm.subject_id].append(perm.class_id)
        return subjects
