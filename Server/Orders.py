import json

from flask import abort, blueprints
import flask

from controllers.OMR_CONNECTION import get_customer_by_phone

orders = blueprints.Blueprint('orders', __name__)


@orders.route('/list_orders', methods=['POST'])
def list_orders():
    data = flask.request.json
    customer = get_customer_by_phone(data['phone'])
    if customer is None:
        abort(404, description="Customer not found with phone: " + str(data['phone']))
    orders = get_all_orders(customer.customer_id)
    if orders is None:
        abort(404, description="You have no orders")
    return json.dumps(orders, default=lambda o: o.__dict__)