# Enrollment DAO (Data Access Object)
# Database operations for Enrollment entity

from database.db_connect import DatabaseConnection
from models.classroom import ClassRoom


class EnrollmentDAO:
    """Data Access Object for Enrollment"""
    
    def __init__(self):
        self.conn = DatabaseConnection.get_connection()
    
    def find_class_by_student(self, student_id, semester=None):
        """Find class for a student"""
        if semester:
            query = """
                SELECT c.class_id, c.name, c.grade_level, c.homeroom_teacher_id, c.created_at
                FROM enrollments e
                JOIN classes c ON e.class_id = c.class_id
                WHERE e.student_id = %s AND e.semester = %s
                LIMIT 1
            """
            cursor = self.conn.cursor()
            cursor.execute(query, (student_id, semester))
        else:
            query = """
                SELECT c.class_id, c.name, c.grade_level, c.homeroom_teacher_id, c.created_at
                FROM enrollments e
                JOIN classes c ON e.class_id = c.class_id
                WHERE e.student_id = %s
                ORDER BY e.created_at DESC
                LIMIT 1
            """
            cursor = self.conn.cursor()
            cursor.execute(query, (student_id,))
        
        row = cursor.fetchone()
        if row:
            return self._row_to_classroom(row)
        return None
    
    def find_by_student_id(self, student_id):
        """Find all enrollments for a student"""
        query = """
            SELECT enrollment_id, student_id, class_id, semester, created_at
            FROM enrollments
            WHERE student_id = %s
            ORDER BY created_at DESC
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (student_id,))
        rows = cursor.fetchall()
        return rows
    
    def find_by_student_and_semester(self, student_id, semester):
        """Find enrollment for a student in a specific semester"""
        query = """
            SELECT enrollment_id, student_id, class_id, semester, created_at
            FROM enrollments
            WHERE student_id = %s AND semester = %s
            LIMIT 1
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (student_id, semester))
        return cursor.fetchone()
    
    def insert(self, student_id, class_id, semester=None):
        """Insert new enrollment"""
        query = """
            INSERT INTO enrollments (student_id, class_id, semester, created_at)
            VALUES (%s, %s, %s, NOW())
        """
        cursor = DatabaseConnection.execute_query(query, (student_id, class_id, semester))
        return cursor.lastrowid
    
    def delete(self, enrollment_id):
        """Delete enrollment"""
        query = "DELETE FROM enrollments WHERE enrollment_id = %s"
        DatabaseConnection.execute_query(query, (enrollment_id,))
    
    @staticmethod
    def _row_to_classroom(row):
        """Convert database row to ClassRoom object"""
        return ClassRoom(
            class_id=row[0],
            name=row[1],
            grade_level=row[2],
            homeroom_teacher_id=row[3],
            created_at=row[4]
        )
