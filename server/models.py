# Import necessary modules for SQLAlchemy, serialization, and validation
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin  # For serializing model instances
from sqlalchemy.orm import validates  # Enables field validation for models

# Initialize the SQLAlchemy database instance
db = SQLAlchemy()

# HERO MODEL

class Hero(db.Model, SerializerMixin):  # Inherits from db.Model and SerializerMixin
    __tablename__ = 'heroes'  # Defines table name in the database

    # Serialization rules to avoid circular references or excess data
    serialize_rules = ('-hero_powers.hero',)  # Exclude hero details within hero_powers

    # Define table columns
    id = db.Column(db.Integer, primary_key=True)  # Primary key for hero ID
    name = db.Column(db.String(100), nullable=False)  # Hero name, cannot be null
    super_name = db.Column(db.String(100), nullable=False)  # Hero's super name, also cannot be null

    # Relationship to powers through HeroPower association table
    powers = db.relationship('HeroPower', back_populates='hero', cascade="all, delete-orphan")


# POWER MODEL

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'  # Defines table name in the database

    # Serialization rules to prevent circular references
    serialize_rules = ('-hero_powers.power',)  # Exclude power details within hero_powers

    # Define table columns
    id = db.Column(db.Integer, primary_key=True)  # Primary key for power ID
    name = db.Column(db.String(100), nullable=False)  # Power name, cannot be null
    description = db.Column(db.String(255), nullable=False)  # Description of the power

    # Relationship to HeroPower association table
    hero_powers = db.relationship('HeroPower', back_populates='power', cascade="all, delete-orphan")


# HERO-POWER ASSOCIATION MODEL

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'  # Defines table name in the database

    # Serialization rules to prevent circular references and excess data
    serialize_rules = ('-hero', '-power',)  # Exclude hero and power details in serialization

    # Define table columns
    id = db.Column(db.Integer, primary_key=True)  # Primary key for hero-power association ID
    strength = db.Column(db.String(20), nullable=False)  # Strength of the hero-power association

    # Foreign keys to link heroes and powers
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    # Relationships to link back to Hero and Power models
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    # Validate the strength attribute with specific allowed values
    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ['Strong', 'Weak', 'Average']  # Allowed values
        if strength not in valid_strengths:
            raise ValueError(f'Strength must be one of {valid_strengths}.')  # Raise error for invalid values
        return strength  # Return valid strength value
