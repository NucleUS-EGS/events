from flask import Flask, jsonify, Response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask import request
from dotenv import load_dotenv
import random
from datetime import date, timedelta
#from flaskext.mysql import MySQL
import mysql.connector
import json
import os
from sqlalchemy import create_engine


app = Flask(__name__)
api = Api(app)

load_dotenv()

db_config = {
    'host': os.environ.get("HOST"),
    'port': os.environ.get("PORT"),
    'user': os.environ.get("USER_NAME"),
    'password': os.environ.get("PASSWORD"),
    'database': os.environ.get('DATABASE')
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn


# Define a sample resource
class HelloWorld(Resource):
    def get(self):
        return jsonify({'message': 'Hello, World!'})
    

class Events(Resource):
    def get(self, event_id=None):
        if event_id:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM events WHERE id = %s"
            values = (event_id,)
            try:
                cursor.execute(query, values)
                result = cursor.fetchall()
                return jsonify({'event': result})
            except mysql.connector.Error as e:
                print(e)
                return Response("Failed to get standings", status=500, mimetype='application/json')
            finally:
                cursor.close()
                conn.close()
        else:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = "SELECT * FROM events"

            try:
                cursor.execute(query)
                result = cursor.fetchall()
                return jsonify({'event': result})
            except mysql.connector.Error as e:
                print(e)
                return Response(status=500)
            finally:
                cursor.close()
                conn.close()

    def post(self,event_id=None):
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO events (name, type, location, date, price) VALUES (%s, %s, %s, %s, %s)"
            values = (request.json['name'], request.json['type'], request.json['location'], request.json['date'], request.json['price'])
            try:
                cursor.execute(query, values)
                conn.commit()
                return Response(status=201)
            except mysql.connector.Error as e:
                print(e)
                return Response(status=500)
            finally:
                cursor.close()
                conn.close()

    def delete(self, event_id=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM events WHERE id = %s"
        values = (event_id,)
        try:
            cursor.execute(query, values)
            conn.commit()
            return Response(status=204)
        except mysql.connector.Error as e:
            print(e)
            return Response(status=500)
        finally:
            cursor.close()
            conn.close()
    
    def patch(self, event_id=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "UPDATE events SET name = %s, type = %s, location = %s, date = %s, price = %s WHERE id = %s"
        values = (request.json['name'], request.json['type'], request.json['location'], request.json['date'], request.json['price'], event_id)
        try:
            cursor.execute(query, values)
            conn.commit()
            return Response(status=204)
        except mysql.connector.Error as e:
            print(e)
            return Response(status=500)
        finally:
            cursor.close()
            conn.close()

class Date(Resource):
    def get(self, date=None):
        if date:
            conn = get_db_connection()
            cursor = conn.cursor()
        
            query = "SELECT * FROM events WHERE date BETWEEN %s AND %s"
            values = (date,)
            try:
                cursor.execute(query, values)
                result = cursor.fetchall()
                return jsonify({'event': result})
            except mysql.connector.Error as e:
                print(e)
                return Response(status=500)
            finally:
                cursor.close()
                conn.close()
        else:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = "SELECT * FROM events"

            try:
                cursor.execute(query)
                result = cursor.fetchall()
                return jsonify({'event': result})
            except mysql.connector.Error as e:
                print(e)
                return Response(status=500)
            finally:
                cursor.close()
                conn.close()

class Type(Resource):
    def get(self, type=None):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM events WHERE type = %s"
        values = (type,)
        try:
            cursor.execute(query, values)
            result = cursor.fetchall()
            return jsonify({'event': result})
        except mysql.connector.Error as e:
            print(e)
            return Response(status=500)
        finally:
            cursor.close()
            conn.close()

class Location(Resource):
    def get(self, location=None):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM events WHERE location = %s"
        values = (location,)
        try:
            cursor.execute(query, values)
            result = cursor.fetchall()
            return jsonify({'event': result})
        except mysql.connector.Error as e:
            print(e)
            return Response(status=500)
        finally:
            cursor.close()
            conn.close()


class Price(Resource):
    def get(self, price=None):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM events WHERE price = %s"
        values = (price,)
        try:
            cursor.execute(query, values)
            result = cursor.fetchall()
            return jsonify({'event': result})
        except mysql.connector.Error as e:
            print(e)
            return Response(status=500)
        finally:
            cursor.close()
            conn.close()


class Price(Resource):
    def get(self, price=None):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM events WHERE price = %s"
        values = (price,)
        try:
            cursor.execute(query, values)
            result = cursor.fetchall()
            return jsonify({'event': result})
        except mysql.connector.Error as e:
            print(e)
            return Response(status=500)
        finally:
            cursor.close()
            conn.close()

       
# Add the resources to the API
api.add_resource(HelloWorld, '/')

api.add_resource(Events, '/events', '/events?<int:event_id>')
api.add_resource(Date, '/date', '/date?<string:date>')
api.add_resource(Type, '/type', '/type?<string:type>')
api.add_resource(Location, '/location', '/location?<string:location>')
api.add_resource(Price, '/price', '/price?<float:price>')



SWAGGER_URL = '/swagger1/v1'
API_URL = 'http://127.0.0.1:5000/swagger.json'
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
    app.run(debug=True)
