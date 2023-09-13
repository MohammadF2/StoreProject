import json

from flask import abort, blueprints
import flask

from controllers.Database.ORM.OMR_CONNECTION import get_item_data, get_customer_by_phone, get_or_create_customer_cart, \
    update_item_quantity, add_item_to_cart, get_all_cart_items, remove_item_from_cart, update_item_quantity_add, \
    update_cart_item_quantity_remove, update_cart_item_quantity_add

CartManagement = blueprints.Blueprint('CartManagement', __name__)


@CartManagement.route('/add_to_cart', methods=['POST'])
def add_item_to_cart_route():
    data = flask.request.json
    item = get_item_data(data['item_barcode'])
    customer = get_customer_by_phone(data['phone'])
    if customer is None:
        abort(404, description="Customer not found with phone: " + str(data['phone']))
    cart = get_or_create_customer_cart(customer.customer_id)
    if item is None:
        abort(404, description="Item not found with barcode: " + str(data['item_barcode']))
    if item.quantity == 0:
        abort(404, description="Item is out of stock")
    if item.quantity < data['quantity']:
        abort(404, description="Not enough quantity we only have: " + str(item.quantity))
    update_item_quantity(data['item_barcode'], data['quantity'])
    add_item_to_cart(cart_id=cart.cart_id, item_barcode=data['item_barcode'], quantity=data['quantity'])
    return json.dumps({"Success": "The item has been added to the cart"})


@CartManagement.route('/remove_from_cart', methods=['POST'])
def remove_item_from_cart_route():
    data = flask.request.json
    customer = get_customer_by_phone(data['phone'])
    if customer is None:
        abort(404, description="Customer not found with phone: " + str(data['phone']))
    cart = get_or_create_customer_cart(customer.customer_id)
    items_cart = get_all_cart_items(cart.cart_id)
    if items_cart is None:
        abort(404, description="You have nothing in the cart: " + str(data['item_barcode']))
    for item in items_cart:
        if item.barcode == data['item_barcode']:
            remove_item_from_cart(cart.cart_id, data['item_barcode'])
            update_item_quantity_add(data['item_barcode'], data['quantity'])
            return json.dumps({"Success": "The item has been removed from the cart"})
    abort(404, description="Item not found with barcode: " + str(data['item_barcode']))


@CartManagement.route('/update_quantity', methods=['POST'])
def return_some_quantity():
    data = flask.request.json
    customer = get_customer_by_phone(data['phone'])
    if customer is None:
        abort(404, description="Customer not found with phone: " + str(data['phone']))
    cart = get_or_create_customer_cart(customer.customer_id)
    items_cart = get_all_cart_items(cart.cart_id)
    if items_cart is None:
        abort(404, description="You have nothing in the cart: " + str(data['item_barcode']))
    for item in items_cart:
        if item.barcode == data['item_barcode']:
            if data['quantity'] == 0:
                remove_item_from_cart(cart.cart_id, data['item_barcode'])
                update_item_quantity_add(data['item_barcode'], data['quantity'])
                return json.dumps({"Success": "The item has been removed from the cart"})
            item_store = get_item_data(data['item_barcode'])
            if item.quantity + item_store.quantity < data['quantity']:
                abort(404, description="Not enough quantity we only have: " + str(item.quantity))
            if data['quantity'] < item.quantity:
                update_item_quantity_add(data['item_barcode'], item.quantity - data['quantity'])
                update_cart_item_quantity_remove(cart_id=cart.cart_id, item_barcode=data['item_barcode'],
                                                 quantity=item.quantity - data['quantity'])
                return json.dumps({"Success": "The item quantity has been updated"})
            if item.quantity < data['quantity']:
                update_cart_item_quantity_add(cart_id=cart.cart_id, item_barcode=data['item_barcode'],
                                              quantity=data['quantity'] - item.quantity)
                update_item_quantity(data['item_barcode'], data['quantity'] - item.quantity)
                return json.dumps({"Success": "The item quantity has been updated"})

    abort(404, description="Item is not in your cart.")


@CartManagement.route('/get_cart_items/<phone>', methods=['GET'])
def get_cart_items(phone):
    customer = get_customer_by_phone(phone)
    if customer is None:
        abort(404, description="Customer not found with phone: " + str(phone))
    cart = get_or_create_customer_cart(customer.customer_id)
    items_cart = get_all_cart_items(cart.cart_id)
    if items_cart is None:
        return json.dumps({"Success": "You have nothing in the cart"})
    return json.dumps(items_cart, default=lambda o: o.__dict__)
