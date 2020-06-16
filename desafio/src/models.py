from __future__ import annotations
from desafio import Base
from sqlalchemy import Column, Integer, String


class User(Base):  # type: ignore
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

    def __eq__(self, other_user):
        if self.username == other_user.username and \
                self.email == other_user.email:
            return True
        else:
            return False
