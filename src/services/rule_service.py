# Rule Service
# Business logic for calculating grades and classifications

class RuleService:
    """Business logic for calculating grades and classifications"""
    
    def __init__(self):
        pass
    
    def calculate_gpa(self, scores):
        """Calculate GPA (Điểm Trung Bình)"""
        if not scores:
            return 0.0
        total = sum(scores)
        return total / len(scores)
    
    def classify_student(self, gpa):
        """Classify student based on GPA (Xếp loại học lực)"""
        if gpa >= 8.0:
            return "Giỏi"
        elif gpa >= 6.5:
            return "Khá"
        elif gpa >= 5.0:
            return "Trung bình"
        elif gpa >= 3.0:
            return "Yếu"
        else:
            return "Kém"
    
    def calculate_weighted_gpa(self, scores, weights):
        """Calculate weighted GPA (Điểm trung bình có trọng số)"""
        if not scores or not weights:
            return 0.0
        total_weighted = sum(score * weight for score, weight in zip(scores, weights))
        total_weight = sum(weights)
        return total_weighted / total_weight if total_weight > 0 else 0.0
    
    def determine_pass_fail(self, gpa, min_gpa=3.0):
        """Determine pass/fail status"""
        return gpa >= min_gpa
