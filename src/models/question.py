from src.ext import db
from src.models.base import BaseModel

class Question(BaseModel, db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    pair_number = db.Column(db.Integer, unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), nullable=True)