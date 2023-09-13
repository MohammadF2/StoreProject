from flask import abort, blueprints

from controllers.Database.ORM.OMR_CONNECTION import get_customer_by_phone, return_orders_as_json

orders = blueprints.Blueprint('orders', __name__)


@orders.route('/list_orders/<phone>', methods=['GET'])
def list_orders(phone):
    customer = get_customer_by_phone(phone)
    if customer is None:
        abort(404, description="Customer not found with phone: " + str(phone))
    orders = return_orders_as_json(customer.customer_id)
    if orders is None:
        abort(404, description="You have no orders")
    return orders