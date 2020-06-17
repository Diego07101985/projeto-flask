from desafio.src.models import User
from desafio import session_scope

from desafio.src.models import User
from desafio import session_scope
from sqlalchemy import inspect


class RepositoryUsers:
    def __init__(self):
        pass

    def get_all_user(self):
        with session_scope() as session:
            return session.query(User).all()

    def get_user(self, user):
        with session_scope() as session:
            print(session)
            user = session.query(User).filter(
                User.username == user.username).first()
        return user

    def insert(self, user):
        with session_scope() as session:
            session.add(user)
            user = session.query(User).filter(
                User.username == user.username).first()
            return user.id

    def update(self, user):
        with session_scope() as session:
            print(user)
            print(f' Nome usuario: {user.username}')
            session.query(User).filter(
                User.username == user.username). \
                update({"email": user.email})

            update_user = session.query(User).filter(
                User.username == user.username).first()
        return update_user

    def delete(self, user):
        with session_scope() as session:
            user = session.query(User).filter(
                User.username == user.username).first()
            session.delete(user)
            update_user = session.query(User).filter(
                User.username == user.username).first()
        return update_user
