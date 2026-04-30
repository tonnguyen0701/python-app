# ClassRoom Service
# Business logic related to classes

from database.class_dao import ClassDAO


class ClassService:
    def __init__(self):
        self.dao = ClassDAO()

    def create_class(self, data):
        return self.dao.insert(data)

    def get_class(self, class_id):
        return self.dao.find_by_id(class_id)

    def get_all_classes(self):
        return self.dao.find_all()

    def update_class(self, class_id, data):
        return self.dao.update(class_id, data)

    def delete_class(self, class_id):
        return self.dao.delete(class_id)
