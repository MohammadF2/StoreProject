import json

from flask import abort, blueprints
import flask

from controllers.Database.ORM.OMR_CONNECTION import get_customer_by_phone, get_or_create_customer_cart, get_all_cart_items, \
    check_out_cart

Checkout = blueprints.Blueprint('Checkout', __name__)


@Checkout.route('/checkout', methods=['POST'])
def checkout():
    data = flask.request.json
    customer = get_customer_by_phone(data['phone'])
    if customer is None:
        abort(404, description="Customer not found with phone: " + str(data['phone']))
    cart = get_or_create_customer_cart(customer.customer_id)
    items_cart = get_all_cart_items(cart.cart_id)
    if items_cart is None:
        abort(404, description="You have nothing in the cart to checkout")
    # calculate total
    total = 0
    for item in items_cart:
        total += item.price * item.quantity
    if data['discount'] > 0:
        total = total - (total * data['discount'] / 100)
    order_no = check_out_cart(cart.cart_id, total, data['discount'], customer.customer_id)
    return json.dumps({"Success": "The order has been checked out", "order_no": order_no})



