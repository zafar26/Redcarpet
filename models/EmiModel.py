
from flask_sqlalchemy import SQLAlchemy
import enum
import uuid
from sqlalchemy_utils import UUIDType
from sqlalchemy import Enum

db = SQLAlchemy()


class Emi(db.Model):
    __tablename__ = "emi"
    id = db.Column(UUIDType(binary=False), primary_key=True,
                   default=uuid.uuid4(), unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    interest = db.Column(db.Integer, nullable=False)
    no_of_months = db.Column(db.Integer, nullable=False)

    def __init__(self, name, intrest):
        self.name = name
        self.intrest = intrest
        self.no_of_months = no_of_months

    def __repr__(self):
        return '<User %r>' % self.name
