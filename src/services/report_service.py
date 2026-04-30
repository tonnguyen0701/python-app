# Report Service
# Generate statistical reports and visualizations

import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from database.db_connect import DatabaseConnection


class ReportService:
    def __init__(self):
        self.conn = DatabaseConnection.get_connection()

    def scores_dataframe(self):
        query = ("SELECT s.score_id, s.student_id, st.name as student_name, s.subject_id, sub.name as subject_name, "
                 "s.score_value, s.midterm_score, s.final_score, s.semester, s.created_at "
                 "FROM scores s JOIN students st ON s.student_id = st.student_id "
                 "JOIN subjects sub ON s.subject_id = sub.subject_id")
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        if not rows:
            return pd.DataFrame(columns=columns)
        df = pd.DataFrame(rows, columns=columns)
        if 'midterm_score' in df.columns and 'final_score' in df.columns:
            df['score_value'] = (df['midterm_score'] + df['final_score']) / 2
        return df

    def average_by_student(self):
        df = self.scores_dataframe()
        if df.empty:
            return pd.DataFrame()
        return df.groupby(['student_id', 'student_name'])['score_value'].mean().reset_index(name='avg_score')

    def get_average_scores(self):
        """Return a list of average score records"""
        df = self.average_by_student()
        if df.empty:
            return []
        return df.rename(columns={'avg_score': 'average'}).to_dict(orient='records')

    def plot_average_distribution(self, save_path=None):
        df = self.average_by_student()
        if df.empty:
            return None
        plt.figure(figsize=(8,6))
        plt.hist(df['avg_score'], bins=10, color='#2c7fb8')
        plt.title('Phân phối điểm trung bình học sinh')
        plt.xlabel('Điểm trung bình')
        plt.ylabel('Số học sinh')
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
            plt.close()
            return save_path
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        return buf
