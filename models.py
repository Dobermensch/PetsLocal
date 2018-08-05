from app import db
from sqlalchemy.dialects.postgresql import JSON

class Pet(db.Model):
    __tablename__ = 'Pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    available_from = db.Column(db.TIMESTAMP(False))
    age = db.Column(db.Integer)
    species = db.Column(db.String())
    breed = db.Column(db.String(), nullable=True)
    adopted = db.Column(db.Integer, nullable=True)

    def __init__(self, name, available_from, age, species, breed, adopted):
        self.name = name
        self.available_from = available_from
        self.age = age
        self.species = species
        self.breed = breed
        self.adopted = adopted

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Customer(db.Model):
    __tablename__ = 'Customers'

    id = db.Column(db.Integer, primary_key=True)
    preference = db.Column(db.Integer, nullable=True)
    adopted = db.Column(db.Integer, nullable=True)

    def __init__(self, preference, adopted):
        self.preference = preference
        self.adopted = adopted

    def __repr__(self):
        return '<id {}>'.format(self.id)

class CustomerPreference(db.Model):
    __tablename__ = 'Preferences'

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    species = db.Column(db.String())
    breed = db.Column(db.String(), nullable=True)
    comparator = db.Column(db.String(), nullable=True)

    def __init__(self, age, species, breed, comparator):
        self.age = age
        self.species = species
        self.breed = breed
        self.comparator = comparator

    def __repr__(self):
        return '<id {}>'.format(self.id)
