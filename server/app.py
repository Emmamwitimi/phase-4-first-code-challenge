# Import necessary modules from Flask and SQLAlchemy
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db  # Import db instance from models
from models import *  # Import all models (Hero, Power, HeroPower)
from flask_migrate import Migrate  # Import Flask-Migrate for database migrations

# Create an instance of the Flask app
app = Flask(__name__)

# Configure the database URI and disable SQLAlchemy's modification tracking
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'  # Database connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disables modification tracking for efficiency

# Initialize the database with our app instance
db.init_app(app)

# Set up Flask-Migrate to handle database migrations
migrate = Migrate(app, db)

# ROUTES & VIEWS: Define API endpoints for handling different requests

# Route to get all heroes from the database
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()  # Query all Hero records
    return jsonify([hero.to_dict() for hero in heroes])  # Return serialized hero data as JSON

# Route to get details for a specific hero by ID
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)  # Query a Hero by ID
    return jsonify(hero.to_dict(include=['hero_powers']))  # Include hero powers in response

# Route to get all powers from the database
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()  # Query all Power records
    return jsonify([power.to_dict() for power in powers])  # Return serialized power data as JSON

# Route to get details for a specific power by ID
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)  # Query a Power by ID
    return jsonify(power.to_dict())  # Return serialized power data as JSON

# Route to update the description of a specific power by ID
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)  # Query a Power by ID
    data = request.json  # Get JSON data from the request
    power.description = data['description']  # Update the description field
    db.session.commit()  # Commit the change to the database
    return jsonify(power.to_dict())  # Return updated power data as JSON

# Route to create a new hero power association with strength, hero, and power IDs
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json  # Get JSON data from the request
    new_hero_power = HeroPower(
        strength=data['strength'],
        hero_id=data['hero_id'],
        power_id=data['power_id']
    )
    db.session.add(new_hero_power)  # Add the new HeroPower to the session
    db.session.commit()  # Commit the new record to the database
    return jsonify(new_hero_power.to_dict()), 201  # Return the new hero power data with 201 status code


