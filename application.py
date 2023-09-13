# To setup Flask
from flask import Flask, request
app = Flask(__name__)

#import of sqlalchemy for Flask
from flask_sqlalchemy import SQLAlchemy


# Configuration of Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' 
db = SQLAlchemy(app)    # Setup of Database

# We gonna define our database structure, here we are using SQLAlchemy
# In this we will define all the things that go into database as Model.
class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)    # Size defined inside String
    description = db.Column(db.String(120))

    def __repr__(self): # this method shows how data will be represented, self means "any object"
        return f"{self.name} - {self.description}"



# To create a Route -> When we visit this Route, this method index() should Run.
@app.route('/')
def index():
    return 'Hello!'

@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    output = []     # An Empty list
    for drink in drinks:
        drink_data = {"name" : drink.name, "description" : drink.description}
        output.append(drink_data)
    return {"drinks": output}

@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {"name" : drink.name, "description" : drink.description}

@app.route('/drinks', methods=['POST'])
def add_drinks():
    drink = Drink(name = request.json['name'], description = request.json['description'])   # Here we access json that user will input with request
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id}

@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"error" : "drink not found"}
    db.session.delete(drink)
    db.session.commit()
    return {"message" : "drink is deleted"}

    
