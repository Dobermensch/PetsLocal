from app import db
from sqlalchemy.dialects.postgresql import JSON

##class Result(db.Model):
##    __tablename__ = 'results'
##
##    id = db.Column(db.Integer, primary_key=True)
##    url = db.Column(db.String())
##    result_all = db.Column(JSON)
##    result_no_stop_words = db.Column(JSON)
##
##    def __init__(self, url, result_all, result_no_stop_words):
##        self.url = url
##        self.result_all = result_all
##        self.result_no_stop_words = result_no_stop_words
##
##    def __repr__(self):
##        return '<id {}>'.format(self.id)

class Pet(db.Model):
    __tablename__ = 'Pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    available_from = db.Column(db.TIMESTAMP(False))
    age = db.Column(db.Integer)
    species = db.Column(db.String())
    breed = db.Column(db.String(), nullable=True)

    def __init__(self, name, available_from, age, species, breed):
        self.name = name
        self.available_from = available_from
        self.age = age
        self.species = species
        self.breed = breed

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Customer(db.Model):
    __tablename__ = 'Customers'

    id = db.Column(db.Integer, primary_key=True)
    preference = db.Column(db.Integer)

    def __init__(self, preference):
        self.preference = preference

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
