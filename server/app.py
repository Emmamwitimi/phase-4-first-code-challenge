from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import *
from flask_migrate import Migrate

##flask app instance
app = Flask(__name__)

#configurations for our db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initialize the db
db.init_app(app)

migrate=Migrate(app,db)

#ROUTES & VIEWS

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes])

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    return jsonify(hero.to_dict(include=['hero_powers']))

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers])

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    return jsonify(power.to_dict())

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    data = request.json
    power.description = data['description']
    db.session.commit()
    return jsonify(power.to_dict())

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json
    new_hero_power = HeroPower(
            strength=data['strength'],
            hero_id=data['hero_id'],
            power_id=data['power_id']
        )
    db.session.add(new_hero_power)
    db.session.commit()
    return jsonify(new_hero_power.to_dict()), 201


#if __name__ == "__main__":
    #app.run(debug=True)



