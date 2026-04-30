# Teacher Class Permission DAO
# Database operations for Teacher-Class-Subject Permission entity

from database.db_connect import DatabaseConnection
from models.teacher_class_permission import TeacherClassPermission


class TeacherClassPermissionDAO:
    """Data Access Object for Teacher Class Permission"""
    
    def __init__(self):
        self.conn = DatabaseConnection.get_connection()
    
    def insert(self, permission):
        """Insert new permission"""
        query = """
            INSERT INTO teacher_class_permissions (teacher_id, class_id, subject_id, can_enter_score, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (permission.teacher_id, permission.class_id, permission.subject_id, 
                  permission.can_enter_score, permission.created_at)
        cursor = DatabaseConnection.execute_query(query, params)
        return cursor.lastrowid
    
    def find_by_id(self, permission_id):
        """Find permission by ID"""
        query = """
            SELECT permission_id, teacher_id, class_id, subject_id, can_enter_score, created_at 
            FROM teacher_class_permissions WHERE permission_id = %s
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (permission_id,))
        row = cursor.fetchone()
        if row:
            return self._row_to_permission(row)
        return None
    
    def find_by_teacher(self, teacher_id):
        """Find all permissions for a teacher"""
        query = """
            SELECT permission_id, teacher_id, class_id, subject_id, can_enter_score, created_at 
            FROM teacher_class_permissions WHERE teacher_id = %s ORDER BY created_at
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (teacher_id,))
        rows = cursor.fetchall()
        return [self._row_to_permission(row) for row in rows]
    
    def find_by_teacher_and_class(self, teacher_id, class_id):
        """Find all permissions for a teacher in a specific class"""
        query = """
            SELECT permission_id, teacher_id, class_id, subject_id, can_enter_score, created_at 
            FROM teacher_class_permissions 
            WHERE teacher_id = %s AND class_id = %s ORDER BY created_at
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (teacher_id, class_id))
        rows = cursor.fetchall()
        return [self._row_to_permission(row) for row in rows]
    
    def find_by_teacher_subject_class(self, teacher_id, subject_id, class_id):
        """Check if teacher has permission for specific subject in class"""
        query = """
            SELECT permission_id, teacher_id, class_id, subject_id, can_enter_score, created_at 
            FROM teacher_class_permissions 
            WHERE teacher_id = %s AND subject_id = %s AND class_id = %s
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (teacher_id, subject_id, class_id))
        row = cursor.fetchone()
        if row:
            return self._row_to_permission(row)
        return None

    def find_all(self):
        """Find all permissions"""
        query = """
            SELECT permission_id, teacher_id, class_id, subject_id, can_enter_score, created_at 
            FROM teacher_class_permissions ORDER BY created_at
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return [self._row_to_permission(row) for row in rows]
    
    def update(self, permission_id, permission):
        """Update permission"""
        query = """
            UPDATE teacher_class_permissions 
            SET teacher_id = %s, class_id = %s, subject_id = %s, can_enter_score = %s
            WHERE permission_id = %s
        """
        params = (permission.teacher_id, permission.class_id, permission.subject_id,
                  permission.can_enter_score, permission_id)
        DatabaseConnection.execute_query(query, params)
    
    def delete(self, permission_id):
        """Delete permission"""
        query = "DELETE FROM teacher_class_permissions WHERE permission_id = %s"
        DatabaseConnection.execute_query(query, (permission_id,))
    
    def delete_by_teacher_and_class(self, teacher_id, class_id):
        """Delete all permissions for teacher in a class"""
        query = "DELETE FROM teacher_class_permissions WHERE teacher_id = %s AND class_id = %s"
        DatabaseConnection.execute_query(query, (teacher_id, class_id))
    
    @staticmethod
    def _row_to_permission(row):
        """Convert database row to TeacherClassPermission object"""
        return TeacherClassPermission(
            permission_id=row[0],
            teacher_id=row[1],
            class_id=row[2],
            subject_id=row[3],
            can_enter_score=row[4],
            created_at=row[5]
        )
