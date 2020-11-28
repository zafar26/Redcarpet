
from flask_sqlalchemy import SQLAlchemy
import enum
import uuid
from sqlalchemy_utils import UUIDType
from sqlalchemy import Enum

db = SQLAlchemy()


class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(UUIDType(binary=False), primary_key=True,
                   default=uuid.uuid4(), unique=True, nullable=False)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=True)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username
