from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
from sqlalchemy.orm import declarative_base
from db_config import db, get_db

engine = create_engine(get_db())

Base = declarative_base()

class APIKEYS(Base):
    __tablename__ = 'apikeys'
    id = db.Column(db.Integer, primary_key=True)
    
    def __init__(self) -> None:
        super().__init__()

    def to_dict(self):
        return {
            'id': self.id
        }
    

class Events(Base):
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
    
insp = reflection.Inspector.from_engine(engine)
    
# if table does not exist, create it
if not insp.has_table(APIKEYS.__tablename__):
    print(" * Creating database tables")
    Base.metadata.create_all(engine)