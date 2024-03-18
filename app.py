from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

# Define a sample resource
class HelloWorld(Resource):
    def get(self):
        return jsonify({'message': 'Hello, World!'})

# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

# Define a resource to return a list of users
class Users(Resource):
    def get(self):
        users = User.query.all()
        user_list = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
        return jsonify(user_list)

# Add the resources to the API
api.add_resource(HelloWorld, '/')
api.add_resource(Users, '/users')


#Create more endpoints
#POST /events: Create a new event
# DELETE /events?id=<event_id>: Delete an event by ID.
# PATCH /events?id=<event_id>: Update event information by ID.
# POST /events?id=<event_id>: Register for an event (Note: This endpoint has the same URL as the POST /events endpoint, so you may need to modify it if it should have a different URL).
# GET /events?entity=<entity_id>: Get event by the entity that creates groups.
# GET /events?date_from=<date>&date_to=<date>: Filter events by date range.
# GET /events?type=<type>: Get event by type.
# GET /events?location=<location>: Get event by location.
# GET /events?price=<price>: Get event by price.

class Events(Resource):
    def post(self):
        return jsonify({'message': 'Create a new event'})
    def delete(self):
        return jsonify({'message': 'Delete an event by ID'})
    def patch(self):
        return jsonify({'message': 'Update event information by ID'})
    def get(self):
        return jsonify({'message': 'Get event by the entity that creates groups'})
class EventsDate(Resource):
    def get(self):
        return jsonify({'message': 'Filter events by date range'})
class EventsType(Resource):
    def get(self):
        return jsonify({'message': 'Get event by type'})
class EventsLocation(Resource):
    def get(self):
        return jsonify({'message': 'Get event by location'})
class EventsPrice(Resource):
    def get(self):
        return jsonify({'message': 'Get event by price'})
class EventsRegister(Resource):
    def post(self):
        return jsonify({'message': 'Register for an event'})
    
api.add_resource(Events, '/events')
api.add_resource(EventsDate, '/events/date')
api.add_resource(EventsType, '/events/type')
api.add_resource(EventsLocation, '/events/location')
api.add_resource(EventsPrice, '/events/price')
api.add_resource(EventsRegister, '/events/register')

# Create the database tables
with app.app_context():
    db.create_all()

# Create a Swagger UI


# Configure Swagger UI
SWAGGER_URL = '/swagger1'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Events"
    }
)

# Register the Swagger UI blueprint
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


#Configure Swagger UI to work with the new endpoints
SWAGGER_URL = '/swagger1'
API_URL = '/swagger1.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Events"
    }
)



@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)