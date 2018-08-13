import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from math import sqrt
from config import DevelopmentConfig as devConfig
import operator

app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS', devConfig))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app)
db = SQLAlchemy(app)

from models import *
comps = {"<": operator.lt, "<=": operator.le, ">": operator.gt, ">=": operator.ge, "=": operator.eq, "!=": operator.ne}

def calcDistance(petC, custC):
    petCoords = petC.split(",")
    petX = float(petCoords[0])
    petY = float(petCoords[1])

    custCoords = custC.split(",")
    custX = float(custCoords[0])
    custY = float(custCoords[1])

    distance = sqrt(((custX - petX)**2) + ((custY - petY)**2))
    return distance

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/subscribe', methods=['GET'])
def subscribe():
    return render_template('subscribe.html')

@app.route('/pets', methods=['POST'])
def insertPet():
    output = []
    name = request.form['name']
    available_from = request.form['avail']
    age = request.form['age']
    species = request.form['species']
    if 'breed' in request.form and species == 'dog':
        breed = request.form['breed']
    else:
        breed = None
    coordinates = str(request.form['xcoor']) + "," + str(request.form['ycoor'])
    
    pet = Pet(name, available_from, age, species, breed, coordinates, adopted=None)
    db.session.add(pet)
    db.session.commit()

    socketio.emit('pet_added', {"name": name, "avail": available_from, "age": age, "species": species, "breed": breed, "coordinates": coordinates}, broadcast=True)
    
    output.append("Inserted successfully")
    return render_template('index.html', petOutput = output)

@app.route('/pets/<int:ID>', methods=['GET'])
def getPets(ID):
    pet = Pet.query.filter_by(id=ID).first()
    if pet is not None:
        obj = {"name": pet.name, "available_from": pet.available_from, "age": pet.age, "species": pet.species, "breed": pet.breed, "adopted": pet.adopted}
    else:
        return "That pet does not exist!"
    
    return jsonify(obj)

@app.route('/customers', methods=['POST'])
def insertCustomer():
    output = []
    coordinates = str(request.form['xcoor']) + "," + str(request.form['ycoor'])
    if 'preferencePicky' in request.form:
        age = request.form['preferredAge']
        comp = request.form['comp']
        species = request.form['species']
        breed = request.form['breed']
        

        customerPreference = CustomerPreference(age, species, breed, comp)
        db.session.add(customerPreference)
        db.session.commit()

    try:    
        preference = customerPreference.id
    except UnboundLocalError:
        preference = None

    customer = Customer(preference, coordinates, adopted=None)
    db.session.add(customer)
    db.session.commit()

    output.append("Inserted Successfully")

    return render_template('index.html', customerOutput = output)

@app.route('/customers/<int:ID>', methods=['GET'])
def getCustomer(ID):
    customer = Customer.query.filter_by(id=ID).first()

    if customer is not None:
        if customer.preference is not None:
            customerPreference = CustomerPreference.query.filter_by(id=customer.preference).first()
            customerPreference = {"age": customerPreference.age, "species": customerPreference.species, "breed": customerPreference.breed, "comp": customerPreference.comparator}
        else:
            customerPreference = None
        obj = {"id": customer.id, "perference": customerPreference, "adopted": customer.adopted, "coordinates": customer.coordinates}
    else:
        return "That customer does not exist!"

    return jsonify(obj)
        
@app.route('/pets/<int:ID>/matches', methods=['GET'])
def petMatches(ID):
    pet = Pet.query.filter_by(id=ID).first()

    if pet is None:
        return "That pet does not exist!"
    
    petObj = {"name": pet.name, "available_from": pet.available_from, "age": pet.age, "species": pet.species, "breed": pet.breed, "adopted": pet.adopted, "coordinates": pet.coordinates}

    if petObj["adopted"] is None:
        matches = []
        customers = Customer.query.all()

        if len(customers) != 0:
            for each in customers:
                if each.preference is not None:
                    cPref = CustomerPreference.query.filter_by(id=each.preference).first()
                    prefObj = {"age": cPref.age, "species": cPref.species, "breed": cPref.breed, "comp": cPref.comparator}
                    if petObj["species"] == prefObj["species"] and petObj["breed"] == prefObj["breed"] and comps[prefObj["comp"]](petObj["age"], prefObj["age"]):
                        if each.adopted is None:
                            matches.append({"customer": each.id, "coordinates": each.coordinates, "preference": prefObj, "distance": calcDistance(petObj["coordinates"], each.coordinates)})
                else:
                    if each.adopted is None:
                        matches.append({"customer": each.id, "coordinates": each.coordinates, "preference": {}, "distance": calcDistance(petObj["coordinates"], each.coordinates)})

        matches = sorted(matches, key=lambda k: k["distance"]) 
        
        return jsonify(matches)
    else:
        return "Pet " + str(ID) + " has already been adopted by a customer so it has no matching customers" 

@app.route('/customers/<int:ID>/matches', methods=['GET'])
def customerMatches(ID):
    customer = Customer.query.filter_by(id=ID).first()

    if customer is None:
        return "That customer does not exist!"
    
    matches = []
    pets = Pet.query.all()

    if customer.adopted is None:    
        if customer.preference is not None:
            cPref = CustomerPreference.query.filter_by(id=customer.preference).first()
            cPref = {"species": cPref.species, "breed": cPref.breed, "age": cPref.age, "comp": cPref.comparator}
            for pet in pets:
                petObj = {"name": pet.name, "available_from": pet.available_from, "age": pet.age, "species": pet.species, "breed": pet.breed, "coordinates": pet.coordinates, "distance": calcDistance(pet.coordiantes, customer.coordinates)}
                if petObj["species"] == cPref["species"] and petObj["breed"] == cPref["breed"] and comps[cPref["comp"]](petObj["age"], cPref["age"]):
                    if pet.adopted is None:
                        matches.append(petObj)
        else:    
            for pet in pets:
                if pet.adopted is None:
                    matches.append({"name": pet.name, "available_from": pet.available_from, "age": pet.age, "species": pet.species, "breed": pet.breed, "coordinates": pet.coordinates, "distance": calcDistance(pet.coordinates, customer.coordinates)})

        matches = sorted(matches, key=lambda k: k["distance"])

        return jsonify(matches)
    else:
        return "Customer " + str(ID) + " has already adopted a pet so it has no matching pets"

@app.route('/customers/<int:ID>/adopt', methods=['POST', 'GET'])
def adopt(ID):
    pet_ID = request.args["pet_id"]
    customer = Customer.query.filter_by(id=ID).first()
    pet = Pet.query.filter_by(id=pet_ID).first()

    if customer is None:
        return "That customer does not exist!"
    if pet is None:
        return "That pet does not exist!"
    
    if pet and customer.adopted is None:
        customer.adopted = pet.id
        pet.adopted = customer.id
        db.session.commit()
        return "Customer " + str(ID) + " successfully adopted Pet " + str(pet_ID) + "!"
    else:
        if not pet:
             return "Pet " + str(pet_ID) + " was not found"
        if customer.adopted is not None:
            return "Customer " + str(ID) + " has already adopted a pet"


@app.route('/get/all', methods=['GET'])
def getAll():
    result = {}
    pets = []
    customers= []

    allCustomers = Customer.query.all()
    if len(allCustomers) != 0:
        for customer in allCustomers:
            customers.append({"id": customer.id, "preference": customer.preference, "adopted": customer.adopted, "coordinates": customer.coordinates})

    allPets = Pet.query.all()
    if len(allPets) != 0:
        for pet in allPets:
            pets.append({"id": pet.id, "name": pet.name, "available_from": pet.available_from, "age": pet.age, "species": pet.species, "breed": pet.breed, "adopted": pet.adopted, "coordinates": pet.coordinates})

    result["customers"] = customers
    result["pets"] = pets

    return jsonify(result)

@app.route('/customers/<int:ID>/preference', methods=['GET'])
def getPreference(ID):
    customer = Customer.query.filter_by(id=ID).first()

    if customer is None:
        return "That customer does not exist!"

    custPref = customer.preference

    prefObj = {}
    if custPref is not None:
        pref = CustomerPreference.query.filter_by(id=custPref).first()
        prefObj["prefID"] = pref.id
        prefObj["age"] = pref.age
        prefObj["species"] = pref.species
        prefObj["breed"] = pref.breed
        prefObj["comp"] = pref.comparator

    return jsonify(prefObj)

@app.route('/get/pets', methods=['GET'])
def getAllPets():
    pets = []
    result = {}

    allPets = Pet.query.all()
    if len(allPets) != 0:
        for pet in allPets:
            pets.append({"id": pet.id, "name": pet.name, "available_from": pet.available_from, "age": pet.age, "species": pet.species, "breed": pet.breed, "adopted": pet.adopted, "coordinates": pet.coordinates})

    result["pets"] = pets

    return jsonify(result)

if __name__ == '__main__':
    socketio.run(app)
