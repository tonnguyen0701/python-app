# Score DAO (Data Access Object)
# Database operations for Score entity

from database.db_connect import DatabaseConnection
from models.score import Score


class ScoreDAO:
    """Data Access Object for Score"""
    
    def __init__(self):
        self.conn = DatabaseConnection.get_connection()
    
    def insert(self, score):
        """Insert new score"""
        query = """
            INSERT INTO scores (student_id, subject_id, score_value, midterm_score, final_score, semester, teacher_id, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (score.student_id, score.subject_id, score.score_value,
                  score.midterm_score, score.final_score, score.semester, score.teacher_id, score.created_at)
        cursor = DatabaseConnection.execute_query(query, params)
        return cursor.lastrowid
    
    def find_by_id(self, score_id):
        """Find score by ID"""
        query = "SELECT score_id, student_id, subject_id, score_value, midterm_score, final_score, semester, teacher_id, created_at FROM scores WHERE score_id = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (score_id,))
        row = cursor.fetchone()
        if row:
            return self._row_to_score(row)
        return None
    
    def find_by_student(self, student_id):
        """Find all scores for a student"""
        query = "SELECT score_id, student_id, subject_id, score_value, midterm_score, final_score, semester, teacher_id, created_at FROM scores WHERE student_id = %s ORDER BY created_at"
        cursor = self.conn.cursor()
        cursor.execute(query, (student_id,))
        rows = cursor.fetchall()
        return [self._row_to_score(row) for row in rows]

    def find_all(self):
        """Find all scores"""
        query = "SELECT score_id, student_id, subject_id, score_value, midterm_score, final_score, semester, teacher_id, created_at FROM scores ORDER BY created_at"
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return [self._row_to_score(row) for row in rows]
    
    def update(self, score_id, score):
        """Update score"""
        query = """
            UPDATE scores 
            SET student_id = %s, subject_id = %s, score_value = %s, midterm_score = %s, final_score = %s, semester = %s, teacher_id = %s
            WHERE score_id = %s
        """
        params = (score.student_id, score.subject_id, score.score_value,
                  score.midterm_score, score.final_score, score.semester, score.teacher_id, score_id)
        DatabaseConnection.execute_query(query, params)
    
    def delete(self, score_id):
        """Delete score"""
        query = "DELETE FROM scores WHERE score_id = %s"
        DatabaseConnection.execute_query(query, (score_id,))
    
    @staticmethod
    def _row_to_score(row):
        """Convert database row to Score object"""
        return Score(
            score_id=row[0],
            student_id=row[1],
            subject_id=row[2],
            score_value=row[3],
            midterm_score=row[4],
            final_score=row[5],
            semester=row[6],
            teacher_id=row[7],
            created_at=row[8]
        )
