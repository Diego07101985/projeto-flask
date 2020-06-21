from desafio import db


class User(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def __init__(self, id=0, email=""):
        self.id = id
        self.email = email
        self.username = ""

    def __repr__(self):
        return '<User %r>' % self.username

    def __eq__(self, other_user):
        if self.username == other_user.username and \
                self.email == other_user.email:
            return True
        else:
            return False
