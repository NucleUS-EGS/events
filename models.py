import uuid
from db_config import db

class APIKEYS(db.Model):
        __tablename__ = 'APIKEYS'
        ID = db.Column(db.String(100), primary_key=True)
        
        def __init__(self, id):
            if id is None:
                id = str(uuid.uuid4())
            self.ID = id
        
        def to_dict(self):
            return {
                "ID": self.ID
            }

class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, description, date, location, price) -> None:
        self.name = name
        self.description = description
        self.date = date
        self.type = type
        self.location = location
        self.price = price
        super().__init__()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'date': self.date,
            'type': self.type,
            'location': self.location,
            'price': self.price
        }
    


    



