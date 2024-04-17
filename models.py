from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from db_config import db


class APIKEYS(db.Model):
    __tablename__ = 'apikeys'
    id = db.Column(db.Integer, primary_key=True)
    
    def __init__(self) -> None:
        super().__init__()

    def to_dict(self):
        return {
            'id': self.id
        }
    

class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, date, location, price) -> None:
        self.name = name
        self.date = date
        self.type = type
        self.location = location
        self.price = price
        super().__init__()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date,
            'type': self.type,
            'location': self.location,
            'price': self.price
        }