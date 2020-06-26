from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_dotenv import DotEnv
import os
import jwt
import datetime 
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SECRET_KEY'] = 'keepitsecretkeepitsafe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'phalanx.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFIACTIONS'] = False

# Initialize Db
db = SQLAlchemy(app)
# Initialize ma
ma = Marshmallow(app)

# database Class/Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

class Needs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    need_name = db.Column(db.String(50), nullable=False)
    need_frequency = db.Column(db.Integer, nullable=False)
    need_quantity = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, need_name, need_frequency, need_quantity, user_id):
        self.need_name = need_name
        self.need_frequency = need_frequency
        self.need_quantity = need_quantity
        self.user_id = user_id

class Supplies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supply_name = db.Column(db.String(50), nullable=False)
    supply_quantity = db.Column(db.Integer, nullable=False)
    supply_frequency = db.Column(db.Integer, nullable=False)
    supply_fail_rate = db.Column(db.Integer, nullable=False)
    supply_life_cycle = db.Column(db.Integer, nullable=False)
    need_demand_per_life_cycle = db.Column(db.Integer, nullable=False)

    need_id = db.Column(db.Integer, db.ForeignKey('needs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, supply_name, supply_quantity, supply_frequency, supply_fail_rate, supply_life_cycle, need_demand_per_life_cycle, need_id, user_id):
        self.supply_name = supply_name
        self.supply_quantity = supply_quantity
        self.supply_frequency = supply_frequency
        self.supply_fail_rate = supply_fail_rate
        self.supply_life_cycle = supply_life_cycle
        self.need_demand_per_life_cycle = need_demand_per_life_cycle
        self.need_id = need_id
        self.user_id = user_id

# Schemas
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'username', 'password')

class NeedsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'need_name', 'need_frequency', 'need_quantity', 'user_id')

class SupplySchema(ma.Schema):
    class Meta:
        fields = ('id', 'supply_name', 'supply_quantity', 'supply_frequency', 'supply_fail_rate', 'supply_life_cycle', 'need_demand_per_life_cycle', 'need_id', 'user_id')

# Initialize Schema
user_schema = UserSchema()
users_schema = UserSchema(many=True,)

need_schema = NeedsSchema()
needs_schema = NeedsSchema(many=True,)

supply_schema = SupplySchema()
supplies_schema = SupplySchema(many=True,)

####################################################################### Create POST Endpoints
@app.route('/register', methods=['POST'])
def add_user():
    name = request.json['name']
    username = request.json['username']
    password = request.json['password']

    hashed_password = generate_password_hash(password, method='sha256')

    new_user = Users(name, username, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/login', methods=['POST'])
def login_user():
    auth = request.authorization

    if auth and auth.password == 'password' & auth and auth.username == 'username':
        token = jwt.encode({'user': auth.username})
    return make_response('Could not verify User', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    this_user = Users(name, username, password)

    db.session.commit()

    return user_schema.jsonify(this_user)

@app.route('/needs', methods=['POST'])
def add_need():
    need_name = request.json['need_name']
    need_frequency = request.json['need_frequency']
    need_quantity = request.json['need_quantity']
    user_id = request.json['user_id']

    new_need = Needs(need_name, need_frequency, need_quantity, user_id)

    db.session.add(new_need)
    db.session.commit()

    return need_schema.jsonify(new_need)

@app.route('/supplies', methods=['POST'])
def add_supply():
    supply_name = request.json['supply_name']
    supply_quantity = request.json['supply_quantity']
    supply_frequency = request.json['supply_frequency']
    supply_fail_rate = request.json['supply_fail_rate']
    supply_life_cycle = request.json['supply_life_cycle']
    need_demand_per_life_cycle = request.json['need_demand_per_life_cycle']
    need_id = request.json['need_id']
    user_id = request.json['user_id']

    new_supply = Supplies(supply_name, supply_quantity, supply_frequency, supply_fail_rate, supply_life_cycle, need_demand_per_life_cycle, need_id, user_id,)

    db.session.add(new_supply)
    db.session.commit()

    return supply_schema.jsonify(new_supply)

####################################################################### Create GET Endpoints
# All Users
@app.route('/users', methods=['GET'])
def get_users():
    all_users = Users.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

# One User
@app.route('/users/<user_id>', methods=['GET'])
def get_one_user(user_id):
    single_user = Users.query.filter_by(id=user_id).first()
    if not single_user:
        return jsonify({'message': 'No user found'})
    print(single_user.name)
    return user_schema.jsonify(single_user)

# All Needs
@app.route('/needs', methods=['GET'])
def get_needs():
    all_needs = Needs.query.all()
    result = needs_schema.dump(all_needs)
    return jsonify(result)

# All Supplies
@app.route('/supplies', methods=['GET'])
def get_supplies():
    all_supplies = Supplies.query.all()
    result = supplies_schema.dump(all_supplies)
    return jsonify(result)

####################################################################### Create DEL Endpoints
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    single_user = Users.query.filter_by(id=user_id).first()
    if not single_user:
        return jsonify({'message': 'No user found'})
    db.session.delete(single_user)
    db.session.commit()
    return jsonify({'message': f"User '{single_user.username}' deleted."}) 

@app.route('/needs/<need_id>', methods=['DELETE'])
def delete_need(need_id):
    single_need = Needs.query.filter_by(id=need_id).first()
    if not single_need:
        return jsonify({'message': 'No need found'})
    db.session.delete(single_need)
    db.session.commit()
    return jsonify({'message': f"Need '{single_need.need_name}' deleted."}) 

@app.route('/supplies/<supply_id>', methods=['DELETE'])
def delete_supply(supply_id):
    single_supply = Supplies.query.filter_by(id=supply_id).first()
    if not single_supply:
        return jsonify({'message': 'No supply found'})
    db.session.delete(single_supply)
    db.session.commit()
    return jsonify({'message': f"Supply '{single_supply.supply_name}' deleted."}) 

####################################################################### Create PUT Endpoints

# run server
if __name__ == '__main__':
    app.run(port=1000, debug=True)
    