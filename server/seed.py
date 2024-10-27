# Importing the choice function from the random module to randomly select elements from a list
from random import choice as rc

# Importing the Flask app instance, database instance, and model classes
from app import app
from models import db, Hero, Power, HeroPower

# Run this code only if the script is executed directly
if __name__ == '__main__':
    # Using the app's context to interact with the database
    with app.app_context():
        print("Clearing db...")  # Indicate start of database clearing

        # Clearing all records from the Power, Hero, and HeroPower tables to start fresh
        Power.query.delete()
        Hero.query.delete()
        HeroPower.query.delete()

        print("Seeding powers...")  # Indicate seeding of power data
        
        # Creating instances of Power with attributes name and description
        powers = [
            Power(name="super strength", description="gives the wielder super-human strengths"),
            Power(name="flight", description="gives the wielder the ability to fly through the skies at supersonic speed"),
            Power(name="super human senses", description="allows the wielder to use her senses at a super-human level"),
            Power(name="elasticity", description="can stretch the human body to extreme lengths"),
        ]

        # Adding all Power instances to the session, ready to be saved to the database
        db.session.add_all(powers)

        print("Seeding heroes...")  # Indicate seeding of hero data

        # Creating instances of Hero with attributes name and super_name
        heroes = [
            Hero(name="Kamala Khan", super_name="Ms. Marvel"),
            Hero(name="Doreen Green", super_name="Squirrel Girl"),
            Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
            Hero(name="Janet Van Dyne", super_name="The Wasp"),
            Hero(name="Wanda Maximoff", super_name="Scarlet Witch"),
            Hero(name="Carol Danvers", super_name="Captain Marvel"),
            Hero(name="Jean Grey", super_name="Dark Phoenix"),
            Hero(name="Ororo Munroe", super_name="Storm"),
            Hero(name="Kitty Pryde", super_name="Shadowcat"),
            Hero(name="Elektra Natchios", super_name="Elektra"),
        ]

        # Adding all Hero instances to the session
        db.session.add_all(heroes)

        print("Adding powers to heroes...")  # Indicate linking heroes to powers

        # Defining possible strength values for hero powers
        strengths = ["Strong", "Weak", "Average"]
        hero_powers = []  # List to collect HeroPower instances

        # Looping through each hero to randomly assign them a power and strength
        for hero in heroes:
            power = rc(powers)  # Randomly selecting a power from the powers list
            # Creating a HeroPower instance with selected hero, power, and a random strength
            hero_powers.append(
                HeroPower(hero=hero, power=power, strength=rc(strengths))
            )

        # Adding all HeroPower instances to the session
        db.session.add_all(hero_powers)
        
        # Committing all changes to the database
        db.session.commit()

        print("Done seeding!")  # Indicate completion of the seeding process
