from src.ext import db
from src.models.base import BaseModel

class Plant(BaseModel, db.Model):
    __tablename__ = 'plant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=True)
    eng_name = db.Column(db.String(255), unique=True, nullable=True)
    family_name = db.Column(db.String(255), unique=True, nullable=True)
    family_name_geo = db.Column(db.String(255), unique=True, nullable=True)
    description = db.Column(db.Text(), nullable=True)
    image = db.Column(db.String(255), unique=True, nullable=True)

    def __str__(self):
        return self.family_name or f'Plant {self.id}'
