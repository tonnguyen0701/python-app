# ClassRoom DAO
# Database operations for ClassRoom entity

from database.db_connect import DatabaseConnection
from models.classroom import ClassRoom


class ClassDAO:
    def __init__(self):
        self.conn = DatabaseConnection.get_connection()

    def insert(self, classroom: ClassRoom):
        query = """
            INSERT INTO classes (name, grade_level, homeroom_teacher_id, created_at)
            VALUES (%s, %s, %s, %s)
        """
        params = (classroom.name, classroom.grade_level, classroom.homeroom_teacher_id, classroom.created_at)
        cursor = DatabaseConnection.execute_query(query, params)
        return cursor.lastrowid

    def find_by_id(self, class_id):
        query = "SELECT * FROM classes WHERE class_id = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (class_id,))
        row = cursor.fetchone()
        if row:
            return self._row_to_class(row)
        return None

    def find_all(self):
        query = "SELECT * FROM classes ORDER BY name"
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return [self._row_to_class(r) for r in rows]

    def update(self, class_id, classroom: ClassRoom):
        query = """
            UPDATE classes
            SET name = %s, grade_level = %s, homeroom_teacher_id = %s
            WHERE class_id = %s
        """
        params = (classroom.name, classroom.grade_level, classroom.homeroom_teacher_id, class_id)
        DatabaseConnection.execute_query(query, params)

    def delete(self, class_id):
        query = "DELETE FROM classes WHERE class_id = %s"
        DatabaseConnection.execute_query(query, (class_id,))

    @staticmethod
    def _row_to_class(row):
        return ClassRoom(
            class_id=row[0],
            name=row[1],
            grade_level=row[2],
            homeroom_teacher_id=row[3],
            created_at=row[4]
        )
