# Teacher DAO
# Database operations for Teacher entity

from database.db_connect import DatabaseConnection
from models.teacher import Teacher


class TeacherDAO:
    def __init__(self):
        self.conn = DatabaseConnection.get_connection()

    def insert(self, teacher: Teacher):
        query = """
            INSERT INTO teachers (name, email, phone, department, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (teacher.name, teacher.email, teacher.phone, teacher.department, teacher.created_at)
        cursor = DatabaseConnection.execute_query(query, params)
        return cursor.lastrowid

    def find_by_id(self, teacher_id):
        query = "SELECT * FROM teachers WHERE teacher_id = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (teacher_id,))
        row = cursor.fetchone()
        if row:
            return self._row_to_teacher(row)
        return None

    def find_all(self):
        query = "SELECT * FROM teachers ORDER BY name"
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return [self._row_to_teacher(r) for r in rows]

    def update(self, teacher_id, teacher: Teacher):
        query = """
            UPDATE teachers
            SET name = %s, email = %s, phone = %s, department = %s
            WHERE teacher_id = %s
        """
        params = (teacher.name, teacher.email, teacher.phone, teacher.department, teacher_id)
        DatabaseConnection.execute_query(query, params)

    def delete(self, teacher_id):
        query = "DELETE FROM teachers WHERE teacher_id = %s"
        DatabaseConnection.execute_query(query, (teacher_id,))

    @staticmethod
    def _row_to_teacher(row):
        return Teacher(
            teacher_id=row[0],
            name=row[1],
            email=row[2],
            phone=row[3],
            department=row[4],
            created_at=row[5]
        )
