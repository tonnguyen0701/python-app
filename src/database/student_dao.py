# Student DAO (Data Access Object)
# Database operations for Student entity

from database.db_connect import DatabaseConnection
from models.student import Student


class StudentDAO:
    """Data Access Object for Student"""
    
    def __init__(self):
        self.conn = DatabaseConnection.get_connection()
    
    def insert(self, student):
        """Insert new student"""
        query = """
            INSERT INTO students (name, date_of_birth, gender, email, phone, address, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (student.name, student.date_of_birth, student.gender, 
                  student.email, student.phone, student.address, student.created_at)
        cursor = DatabaseConnection.execute_query(query, params)
        return cursor.lastrowid
    
    def find_by_id(self, student_id):
        """Find student by ID"""
        query = "SELECT * FROM students WHERE student_id = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (student_id,))
        row = cursor.fetchone()
        if row:
            return self._row_to_student(row)
        return None
    
    def find_all(self):
        """Find all students"""
        query = "SELECT * FROM students ORDER BY name"
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return [self._row_to_student(row) for row in rows]
    
    def update(self, student_id, student):
        """Update student"""
        query = """
            UPDATE students 
            SET name = %s, date_of_birth = %s, gender = %s, email = %s, phone = %s, address = %s
            WHERE student_id = %s
        """
        params = (student.name, student.date_of_birth, student.gender, 
                  student.email, student.phone, student.address, student_id)
        DatabaseConnection.execute_query(query, params)
    
    def delete(self, student_id):
        """Delete student"""
        query = "DELETE FROM students WHERE student_id = %s"
        DatabaseConnection.execute_query(query, (student_id,))
    
    def search(self, keyword):
        """Search students"""
        query = "SELECT * FROM students WHERE name LIKE %s OR email LIKE %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
        rows = cursor.fetchall()
        return [self._row_to_student(row) for row in rows]
    
    @staticmethod
    def _row_to_student(row):
        """Convert database row to Student object"""
        return Student(
            student_id=row[0],
            name=row[1],
            date_of_birth=row[2],
            gender=row[3],
            email=row[4],
            phone=row[5],
            address=row[6],
            created_at=row[7]
        )
