from flask import Flask, jsonify, request, Response
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
from flask_swagger_ui import get_swaggerui_blueprint
from models import *
from datetime import datetime
from db_config import * 
import mysql.connector
from mysql.connector import Error
import json
from sqlalchemy.orm import sessionmaker
from waitress import serve

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = get_db()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = get_sqlalchemy_track_modifications()

db.init_app(app)

APIKEY = os.environ.get('APIKEY')

with app.app_context():
    engine = create_engine(get_db())
    insp = reflection.Inspector.from_engine(engine)
    if not insp.has_table(APIKEYS.__tablename__):
        print(' * Creating all tables')
        db.create_all()

        # insert APIKEY if doesn't exist
        key = APIKEYS.query.filter(APIKEYS.apikey == APIKEY).first()
        if not key:
            print(' * Adding API Key')
            key = APIKEYS(apikey=APIKEY)
            db.session.add(key)
            db.session.commit()

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/') 
def home():
    return jsonify({"message": "Welcome to the Event API"})    

class APIkey(Resource):

    def get(self):
        try:
            apikeys = APIKEYS.query.all()  
            if not apikeys:  
                return jsonify([])  

            return jsonify([{'ID': apikey.ID} for apikey in apikeys])

        except Exception as e:
            return {"error": str(e)}, 500


class Events(Resource):

    #GET /events/<int:event_id>
    def get(self, event_id):
        parser = reqparse.RequestParser()
        parser.add_argument('event_id', type=int)
        args = parser.parse_args()
        event_id = args['event_id']

        try:
            if event_id is None:
                events = Events.query.all()
                if not events:
                    return jsonify([])

                return jsonify([event.to_dict() for event in events])
            else:
                events = Events.query.filter_by(id=event_id).first()
                if events is None:
                    return jsonify({"error": "Event not found"}), 404
                
            return jsonify([events.to_dict()])
        except Exception as e:
            return {"error": str(e)}, 500
        
    #GET /events/name?<string:name>
    def get(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        args = parser.parse_args()
        name = args['name']

        try:
            if name is None:
                events = Events.query.all()
                if not events:
                    return jsonify([])

                return jsonify([event.to_dict() for event in events])
            else:
                events = Events.query.filter_by(name=name).first()
                if events is None:
                    return jsonify({"error": "Event not found"}), 404
                
            return jsonify([events.to_dict()])
        except Exception as e:
            return {"error": str(e)}, 500

    #GET /events/date?<string:date>
    def get(self, date):    
        parser = reqparse.RequestParser()
        parser.add_argument('date', type=str)
        args = parser.parse_args()
        date = args['date']

        try:
            if date is None:
                events = Events.query.all()
                if not events:
                    return jsonify([])

                return jsonify([event.to_dict() for event in events])
            else:
                events = Events.query.filter_by(date=date).first()
                if events is None:
                    return jsonify({"error": "Event not found"}), 404
                
            return jsonify([events.to_dict()])
        except Exception as e:
            return {"error": str(e)}, 500

    #GET /events/type?<string:type>
    def get(self, type):
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str)
        args = parser.parse_args()
        type = args['type']

        try:
            if type is None:
                events = Events.query.all()
                if not events:
                    return jsonify([])

                return jsonify([event.to_dict() for event in events])
            else:
                events = Events.query.filter_by(type=type).first()
                if events is None:
                    return jsonify({"error": "Event not found"}), 404
                
            return jsonify([events.to_dict()])
        except Exception as e:
            return {"error": str(e)}, 500

    #GET /events/location?<string:location>
    def get(self, location):
        parser = reqparse.RequestParser()
        parser.add_argument('location', type=str)
        args = parser.parse_args()
        location = args['location']

        try:
            if location is None:
                events = Events.query.all()
                if not events:
                    return jsonify([])

                return jsonify([event.to_dict() for event in events])
            else:
                events = Events.query.filter_by(location=location).first()
                if events is None:
                    return jsonify({"error": "Event not found"}), 404
                
            return jsonify([events.to_dict()])
        except Exception as e:
            return {"error": str(e)}, 500

    #GET /events/price?<float:price>
    def get(self, price):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float)
        args = parser.parse_args()
        price = args['price']

        try:
            if price is None:
                events = Events.query.all()
                if not events:
                    return jsonify([])

                return jsonify([event.to_dict() for event in events])
            else:
                events = Events.query.filter_by(price=price).first()
                if events is None:
                    return jsonify({"error": "Event not found"}), 404
                
            return jsonify([events.to_dict()])
        except Exception as e:
            return {"error": str(e)}, 500

    #POST /events
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('date', type=str, required=True)
        parser.add_argument('type', type=str, required=True)
        parser.add_argument('location', type=str, required=True)
        parser.add_argument('price', type=float, required=True)
        args = parser.parse_args()

        try:
            event = Events(
                name=args['name'],
                date=args['date'],
                type=args['type'],
                location=args['location'],
                price=args['price']
            )
            db.session.add(event)
            db.session.commit()
            return jsonify(event.to_dict()), 201
        except Exception as e:
            return {"error": str(e)}, 500

    #PUT /events/<int:event_id>
    def put(self, event_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('date', type=str, required=True)
        parser.add_argument('type', type=str, required=True)
        parser.add_argument('location', type=str, required=True)
        parser.add_argument('price', type=float, required=True)
        args = parser.parse_args()

        try:
            event = Events.query.filter_by(id=event_id).first()
        
            event.name = args['name']
            event.date = args['date']
            event.type = args['type']
            event.location = args['location']
            event.price = args['price']

            db.session.commit()
            return jsonify(event.to_dict()), 200
        except Exception as e:
            return {"error": str(e)}, 500

    #DELETE /events/<int:event_id>
    def delete(self, event_id):
        try:
            event = Events.query.filter_by(id=event_id).first()
            if event is None:
                return jsonify({"error": "Event not found"}), 404

            db.session.delete(event)
            db.session.commit()
            return '', 204
        except Exception as e:
            return {"error": str(e)}, 500    
        
   

       
# Add the resources to the API
api.add_resource(Events, '/v1/events?<int:event_id>', endpoint='event')
api.add_resource(Events, '/v1/events/name?<string:name>', endpoint='name')
api.add_resource(Events, '/v1/events/date?<string:date>', endpoint='date')
api.add_resource(Events, '/v1/events/type?<string:type>', endpoint='type')
api.add_resource(Events, '/v1/events/location?<string:location>', endpoint='location')
api.add_resource(Events, '/v1/events/price?<float:price>', endpoint='price')

HOST = os.environ.get('APP_HOST')
PORT = os.environ.get('APP_PORT')

SWAGGER_URL = '/swagger/v1/'
API_URL = 'http://' + HOST + ':' + PORT + '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Event API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))


if __name__ == '__main__':
    serve(app, host=HOST, port=PORT)