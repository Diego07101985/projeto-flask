from src.models import User


class RepositoryUsers:
    def __init__(self, dal):
        self.dal = dal
        self.dal.session = dal.Session()

    def get_user(self):
        return self.dal.session.query(User).all()

    def insert(self, user) -> int:
        self.dal.Session.add(user)
        id = self.dal.session.commit()
        return id
