from src.models import User
from desafio import session_scope


class RepositoryUsers:
    def __init__(self, session):
        self.session = session
        pass

    def get_all_user(self):
        with session_scope() as session:
            return session.query(User).all()

    def insert(self, user):
        with session_scope() as session:
            session.add(user)

    def update(self, user):
        with session_scope() as session:
            session.query(User).filter(
                User.username == user.username).update({"email": user.email})

        return user
