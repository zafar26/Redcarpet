from flask_sqlalchemy import SQLAlchemy
import enum
import uuid
from sqlalchemy_utils import UUIDType
from sqlalchemy import Enum

db = SQLAlchemy()


class Status(enum.Enum):
    'New'
    'Rejected'
    'Approved'


class Users(db.Model):
    __tablename__ = "users"
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


class Agents(db.Model):
    __tablename__ = "agents"
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


class Loan(db.Model):
    __tablename__ = "loan"
    id = db.Column(UUIDType(binary=False), primary_key=True,
                   default=uuid.uuid4(), unique=True, nullable=False)
    name = db.Column(db.String, nullable=True)
    aadhar = db.Column(db.String, nullable=True)
    purpose = db.Column(db.String, nullable=True)
    status = db.Column(Enum('New', 'Rejected', 'Approved'),
                       default='New', nullable=False)
    isUserApproved = db.Column(db.Boolean, default=False)
    isAdminApproved = db.Column(db.Boolean, default=False)
    ammount = db.Column(db.Integer, nullable=True)
    monthlyDeductAmmount = db.Column(db.Integer, nullable=True)
    createdAt = db.Column(db.DateTime, nullable=False)
    updatedAt = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(UUIDType(binary=False),
                        db.ForeignKey("users.id"), nullable=False)
    agent_id = db.Column(UUIDType(binary=False),
                         db.ForeignKey("agents.id"), nullable=False)
    emi_id = db.Column(UUIDType(binary=False),
                       db.ForeignKey("emi.id"), nullable=False)

    def __init__(self, name, aadhar, purpose, status, isUserApproved, isAdminApproved, ammount, monthlyDeductAmmount, createdAt, updatedAt):
        self.name = name
        self.aadhar = aadhar
        self.purpose = purpose
        self.status = status
        self.isUserApproved = isUserApproved
        self.isAdminApproved = isAdminApproved
        self.ammount = ammount
        self.monthlyDeductAmmount = monthlyDeductAmmount
        self.createdAt = createdAt
        self.updatedAt = updatedAt

    def __repr__(self):
        return '<User %r>' % self.name
