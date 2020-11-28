from flask_sqlalchemy import SQLAlchemy
import enum
import uuid
from sqlalchemy_utils import UUIDType
from sqlalchemy import Enum

db = SQLAlchemy()


class Status(enum.Enum):
    new = 'New'
    rejected = 'Rejected'
    approved = 'Approved'


class Loan(db.Model):
    __tablename__ = "loan"
    id = db.Column(UUIDType(binary=False), primary_key=True,
                   default=uuid.uuid4(), unique=True, nullable=False)
    name = db.Column(db.String, nullable=True)
    aadhar = db.Column(db.String, nullable=True)
    purpose = db.Column(db.String, nullable=True)
    status = db.Column(Enum(Status), default='New', nullable=False)
    isUserApproved = db.Column(db.Boolean, default=False)
    isAdminApproved = db.Column(db.Boolean, default=False)
    ammount = db.Column(db.Integer, nullable=True)
    monthlyDeductAmmount = db.Column(db.Integer, nullable=True)
    createdAt = db.Column(db.DateTime, nullable=False)
    updatedAt = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(UUIDType(binary=False),
                        db.ForeignKey("users.id"), nullable=False)
    agent_id = db.Column(UUIDType(binary=False),
                         db.ForeignKey("users.id"), nullable=False)
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
