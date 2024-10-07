from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates  # This line is essential


db = SQLAlchemy()


#hero model
class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    #serialization rules
    serialize_rules = ('-hero_powers.hero',)  # Prevent including hero details in hero_powers

    #attributes
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(100), nullable=False)

    #relationship with the power through the association table
    powers = db.relationship('HeroPower', back_populates='hero', cascade="all, delete-orphan")

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

     # Serialization rules to prevent recursion
    serialize_rules = ('-hero_powers.power',)  # Prevent including power details in hero_powers

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    #rtn
    hero_powers = db.relationship('HeroPower', back_populates='power', cascade="all, delete-orphan")


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

      # Serialization rules to prevent recursion
    serialize_rules = ('-hero', '-power',)  # Prevent including hero and power details in the association

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(20), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    # Relationships
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

     # Validation for strength
    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if strength not in valid_strengths:
            raise ValueError(f'Strength must be one of {valid_strengths}.')
        return strength