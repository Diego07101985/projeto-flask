from src.models import User
from src import Session


class RepositoryUsers:
    def __init__(self):
        self.session = Session()

    def get_user(self):
        return self.session.query(User).all()

    def insert(self, user) -> int:
        self.session.add(user)
        id = self.session.commit()
        return id
