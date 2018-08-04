import os
from flask import Flask, render_template, send_file, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig as devConfig
from sqlalchemy.dialects.postgresql import insert

app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS', devConfig))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Pet, Customer, CustomerPreference


@app.route('/', methods=['GET', 'POST'])
def index():
    return send_file('templates/index.html')

@app.route('/pets', methods=['POST'])
def insertPet():
    output = []
    name = request.form['name']
    available_from = request.form['avail']
    age = request.form['age']
    species = request.form['species']
    breed = request.form['breed']
    
    pet = Pet(name, available_from, age, species, breed)
    db.session.add(pet)
    db.session.commit()
    output.append("Inserted successfully")
    return render_template('index.html', petOutput = output)

@app.route('/pets/<ID>', methods=['GET'])
def getPets(ID):
    pet = Pet.query.filter_by(id=ID).first()
    obj = {"name": pet.name, "available_from": pet.available_from, "age": pet.age, "species": pet.species, "breed": pet.breed}
    
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

    customer = Customer(preference)
    db.session.add(customer)
    db.session.commit()

    output.append("Inserted Successfully")

    return render_template('index.html', customerOutput = output)

@app.route('/customers/<ID>', methods=['GET'])
def getCustomer(ID):
    customer = Customer.query.filter_by(id=ID).first()
    if customer.preference is not None:
        customerPreference = CustomerPreference.query.filter_by(id=customer.preference).first()
        customerPreference = {"age": customerPreference.age, "species": customerPreference.species, "breed": customerPreference.breed, "comp": customerPreference.comparator}
    else:
        customerPreference = None
    obj = {"id": customer.id, "perference": customerPreference}

    return jsonify(obj)
        
##@app.route('/pets/<ID>/matches', methods=['GET'])
##def petMatches(ID):
##    customers = Customer.query.all()
##    print(type(customers), customers)


##@app.route('/<name>')
##def hello_name(name):
##    return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run()
