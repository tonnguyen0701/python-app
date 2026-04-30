# Score Service
# Business logic for score management

from database.score_dao import ScoreDAO


class ScoreService:
    """Business logic for score operations"""
    
    def __init__(self):
        self.score_dao = ScoreDAO()
    
    def create_score(self, score_data):
        """Create a new score"""
        # TODO: Validate score data
        return self.score_dao.insert(score_data)
    
    def add_score(self, score_data):
        """Alias for create_score"""
        return self.create_score(score_data)
    
    def get_all_scores(self):
        """Get all scores"""
        return self.score_dao.find_all()
    
    def get_score(self, score_id):
        """Get score by ID"""
        return self.score_dao.find_by_id(score_id)
    
    def get_scores_by_student(self, student_id):
        """Get all scores for a student"""
        return self.score_dao.find_by_student(student_id)
    
    def update_score(self, score_id, score_data):
        """Update score"""
        # TODO: Validate score data
        return self.score_dao.update(score_id, score_data)
    
    def delete_score(self, score_id):
        """Delete score"""
        return self.score_dao.delete(score_id)
    
    def _row_to_score(self, row):
        """Convert database row to Score object"""
        from models.score import Score
        return Score(
            score_id=row[0],
            student_id=row[1],
            subject_id=row[2],
            score_value=row[3],
            midterm_score=row[4],
            final_score=row[5],
            semester=row[6],
            created_at=row[7]
        )
