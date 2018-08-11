import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig as devConfig
import operator

app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS', devConfig))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Pet, Customer, CustomerPreference
comps = {"<": operator.lt, "<=": operator.le, ">": operator.gt, ">=": operator.ge, "=": operator.eq, "!=": operator.ne}

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
    
    pet = Pet(name, available_from, age, species, breed, adopted=None)
    db.session.add(pet)
    db.session.commit()
    
    output.append("Inserted successfully")
    return render_template('index.html', petOutput = output)

@app.route('/pets/<int:ID>', methods=['GET'])
def getPets(ID):
    pet = Pet.query.filter_by(id=ID).first()
    obj = {"name": pet.name, "available_from": pet.available_from, "age": pet.age, "species": pet.species, "breed": pet.breed, "adopted": pet.adopted}
    
    return jsonify(obj)

@app.route('/customers', methods=['POST'])
def insertCustomer():
    output = []
    print(request.form)
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

    customer = Customer(preference, adopted=None)
    db.session.add(customer)
    db.session.commit()

    output.append("Inserted Successfully")

    return render_template('index.html', customerOutput = output)

@app.route('/customers/<int:ID>', methods=['GET'])
def getCustomer(ID):
    customer = Customer.query.filter_by(id=ID).first()
    if customer.preference is not None:
        customerPreference = CustomerPreference.query.filter_by(id=customer.preference).first()
        customerPreference = {"age": customerPreference.age, "species": customerPreference.species, "breed": customerPreference.breed, "comp": customerPreference.comparator}
    else:
        customerPreference = None
    obj = {"id": customer.id, "perference": customerPreference, "adopted": customer.adopted}

    return jsonify(obj)
        
@app.route('/pets/<int:ID>/matches', methods=['GET'])
def petMatches(ID):
    pet = Pet.query.filter_by(id=ID).first()
    petObj = {"name": pet.name, "available_from": pet.available_from, "age": pet.age, "species": pet.species, "breed": pet.breed, "adopted": pet.adopted}

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
                            matches.append({"customer": each.id, "preference": prefObj})
                else:
                    if each.adopted is None:
                        matches.append({"customer": each.id, "preference": {}})

        return jsonify(matches)
    else:
        return "Pet " + str(ID) + " has already been adopted by a customer so it has no matching customers" 

@app.route('/customers/<int:ID>/matches', methods=['GET'])
def customerMatches(ID):
    customer = Customer.query.filter_by(id=ID).first()
    matches = []
    pets = Pet.query.all()

    if customer.adopted is None:    
        if customer.preference is not None:
            cPref = CustomerPreference.query.filter_by(id=customer.preference).first()
            cPref = {"species": cPref.species, "breed": cPref.breed, "age": cPref.age, "comp": cPref.comparator}
            for pet in pets:
                petObj = {"name": pet.name, "available_from": pet.available_from, "age": pet.age, "species": pet.species, "breed": pet.breed, }
                if petObj["species"] == cPref["species"] and petObj["breed"] == cPref["breed"] and comps[cPref["comp"]](petObj["age"], cPref["age"]):
                    if pet.adopted is None:
                        matches.append(petObj)
        else:    
            for pet in pets:
                if pet.adopted is None:
                    matches.append({"name": pet.name, "available_from": pet.available_from, "age": pet.age, "species": pet.species, "breed": pet.breed})

        return jsonify(matches)
    else:
        return "Customer " + str(ID) + " has already adopted a pet so it has no matching pets"

@app.route('/customers/<int:ID>/adopt', methods=['POST', 'GET'])
def adopt(ID):
    pet_ID = request.args["pet_id"]
    customer = Customer.query.filter_by(id=ID).first()
    pet = Pet.query.filter_by(id=pet_ID).first()
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
            customers.append({"id": customer.id, "preference": customer.preference, "adopted": customer.adopted})

    allPets = Pet.query.all()
    if len(allPets) != 0:
        for pet in allPets:
            pets.append({"id": pet.id, "name": pet.name, "available_from": pet.available_from, "age": pet.age, "species": pet.species, "breed": pet.breed, "adopted": pet.adopted})

    result["customers"] = customers
    result["pets"] = pets

    return jsonify(result)

@app.route('/customers/<int:ID>/preference', methods=['GET'])
def getPreference(ID):
    customer = Customer.query.filter_by(id=ID).first()

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
            pets.append({"id": pet.id, "name": pet.name, "available_from": pet.available_from, "age": pet.age, "species": pet.species, "breed": pet.breed, "adopted": pet.adopted})

    result["pets"] = pets

    return jsonify(result)

if __name__ == '__main__':
    socketio.run(app)
