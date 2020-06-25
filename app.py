from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Initialize app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
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

    def __init__(self, need_name, need_frequency, need_quantity):
        self.need_name = need_name
        self.need_frequency = need_frequency
        self.need_quantity = need_quantity

class Supplies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supply_name = db.Column(db.String(50), nullable=False)
    supply_quantity = db.Column(db.String(50), nullable=False)
    supply_frequency = db.Column(db.String(50), nullable=False)
    supply_fail_rate = db.Column(db.Integer, nullable=False)
    supply_life_cycle = db.Column(db.Integer, nullable=False)
    need_demand_per_life_cycle = db.Column(db.Integer, nullable=False)

    need_id = db.Column(db.Integer, db.ForeignKey('needs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, supply_name, supply_quantity, supply_frequency, supply_fail_rate, supply_life_cycle, need_demand_per_life_cycle):
        self.supply_name = supply_name
        self.supply_quantity = supply_quantity
        self.supply_frequency = supply_frequency
        self.supply_fail_rate = supply_fail_rate
        self.supply_life_cycle = supply_life_cycle
        self.need_demand_per_life_cycle = need_demand_per_life_cycle

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

# run server
if __name__ == '__main__':
    app.run(port=1000, debug=True)
    