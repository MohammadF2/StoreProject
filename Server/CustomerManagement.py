from flask import blueprints
import flask
import json

from controllers.OMR_CONNECTION import get_customer_by_phone, create_customer

CustomerManagement = blueprints.Blueprint('CustomerManagement', __name__)


@CustomerManagement.route('/get_customer_data/<phone>', methods=['GET'])
def get_all_customers(phone):
    return json.dumps(get_customer_by_phone(phone=phone), default=lambda o: o.__dict__)


@CustomerManagement.route('/create_customer', methods=['POST'])
def create_new_customer():
    data = flask.request.json
    return json.dumps(create_customer(name=data['name'], phone=data['phone']))
