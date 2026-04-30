# Teacher Service
# Business logic related to teachers

from database.teacher_dao import TeacherDAO


class TeacherService:
    def __init__(self):
        self.dao = TeacherDAO()

    def create_teacher(self, data):
        return self.dao.insert(data)

    def get_teacher(self, teacher_id):
        return self.dao.find_by_id(teacher_id)

    def get_all_teachers(self):
        return self.dao.find_all()

    def update_teacher(self, teacher_id, data):
        return self.dao.update(teacher_id, data)

    def delete_teacher(self, teacher_id):
        return self.dao.delete(teacher_id)
