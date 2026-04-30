# Subject DAO (Data Access Object)
# Database operations for Subject entity

from database.db_connect import DatabaseConnection
from models.subject import Subject


class SubjectDAO:
    """Data Access Object for Subject"""
    
    def __init__(self):
        self.conn = DatabaseConnection.get_connection()
    
    def insert(self, subject):
        """Insert new subject"""
        query = """
            INSERT INTO subjects (name, code, credit, class_name, class_shift, class_day, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (subject.name, subject.code, subject.credit,
                  subject.class_name, subject.class_shift, subject.class_day,
                  subject.created_at)
        cursor = DatabaseConnection.execute_query(query, params)
        return cursor.lastrowid
    
    def find_by_id(self, subject_id):
        """Find subject by ID"""
        query = "SELECT subject_id, name, code, credit, class_name, class_shift, class_day, created_at FROM subjects WHERE subject_id = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (subject_id,))
        row = cursor.fetchone()
        if row:
            return self._row_to_subject(row)
        return None
    
    def find_all(self):
        """Find all subjects"""
        query = "SELECT subject_id, name, code, credit, class_name, class_shift, class_day, created_at FROM subjects ORDER BY name"
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return [self._row_to_subject(row) for row in rows]
    
    def update(self, subject_id, subject):
        """Update subject"""
        query = """
            UPDATE subjects 
            SET name = %s, code = %s, credit = %s,
                class_name = %s, class_shift = %s, class_day = %s
            WHERE subject_id = %s
        """
        params = (subject.name, subject.code, subject.credit,
                  subject.class_name, subject.class_shift, subject.class_day,
                  subject_id)
        DatabaseConnection.execute_query(query, params)
    
    def delete(self, subject_id):
        """Delete subject"""
        query = "DELETE FROM subjects WHERE subject_id = %s"
        DatabaseConnection.execute_query(query, (subject_id,))
    
    @staticmethod
    def _row_to_subject(row):
        """Convert database row to Subject object"""
        return Subject(
            subject_id=row[0],
            name=row[1],
            code=row[2],
            credit=row[3],
            class_name=row[4],
            class_shift=row[5],
            class_day=row[6],
            created_at=row[7]
        )
