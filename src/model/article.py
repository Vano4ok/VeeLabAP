from src.main import db
from strenum import StrEnum
from sqlalchemy import func
from sqlalchemy import DateTime, Enum


class State(StrEnum):
    NEW = 'New'
    IN_REVIEW = 'In Review'
    CONFIRMED = 'Confirmed'


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    text = db.Column(db.String(700), nullable=False)
    date = db.Column(DateTime(timezone=True), server_default=func.now())
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    state = db.Column(Enum(State), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
