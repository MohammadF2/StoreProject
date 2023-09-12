from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import controllers.Sql_Class
from controllers.Sql_Class import Customer, Item, Order, CartItem, Cart
from model.Cart import Cart
from model.Customer import Customer
from model.Item import Item
from model.Order import Order
from datetime import date

# Create a MySQL database connection
DATABASE_URL = "mysql://root:123456789@localhost/store_database"

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


def get_all_customers():
    customers = session.query(Customer).all()
    return customers


def get_customer_by_id(customer_id):
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    return customer


def get_customer_orders(customer_id):
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if customer:
        return customer.orders
    return []


def get_customer_carts(customer_id):
    cart = session.query(controllers.Sql_Class.Cart).filter(
        controllers.Sql_Class.Cart.customer_id == customer_id).first()
    if cart:
        return Cart(cart_id=cart.cart_id, customer_id=cart.customer_id, items=get_all_cart_items(cart.cart_id))
    return []


def create_customer(name, phone):
    new_customer = controllers.Sql_Class.Customer(name=name, phone=phone)
    session.add(new_customer)
    try:
        session.commit()
    except:
        print("error creating customer")
        session.rollback()
    return new_customer.id


def get_or_create_customer_cart(customer_id):
    cart = session.query(controllers.Sql_Class.Cart).filter(
        controllers.Sql_Class.Cart.customer_id == customer_id).first()
    if cart:
        return Cart(cart.cart_id, cart.customer_id, get_all_cart_items(cart.cart_id))
    else:
        # Create a new cart for the customer
        new_cart = controllers.Sql_Class.Cart(customer_id=customer_id)
        session.add(new_cart)
        try:
            session.commit()
        except:
            print("error creating cart")
            session.rollback()
        return Cart(new_cart.cart_id, new_cart.customer_id, [])


def create_cart(customer_id):
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if customer:
        new_cart = Cart(customer_id=customer_id)
        session.add(new_cart)
        try:
            session.commit()
        except:
            print("error creating cart")
            session.rollback()


def get_customer_by_phone(phone):
    customer = session.query(controllers.Sql_Class.Customer).filter(
        controllers.Sql_Class.Customer.phone == phone).first()
    if customer:
        return Customer(customer.id, customer.phone, customer.name)
    return None


def get_all_items():
    items_data = session.query(controllers.Sql_Class.Item).all()
    items = []
    for row in items_data:
        item = Item(row.barcode, row.name, row.price, row.quantity_storage)
        items.append(item)
    return items


def add_item_to_cart(cart_id, item_barcode, quantity):
    contains = session.query(controllers.Sql_Class.CartItem).filter(controllers.Sql_Class.CartItem.cart_id == cart_id,
                                                                    controllers.Sql_Class.CartItem.item_barcode == item_barcode).first()
    if contains:
        contains.quantity += quantity
        try:
            session.commit()
        except:
            print("error adding item to cart")
            session.rollback()
        return
    cart_item = CartItem(cart_id=cart_id, item_barcode=item_barcode, quantity=quantity)
    session.add(cart_item)
    try:
        session.commit()
    except:
        print("error adding item to cart")
        session.rollback()


def update_item_quantity(item_barcode, quantity):
    item = session.query(controllers.Sql_Class.Item).filter(controllers.Sql_Class.Item.barcode == item_barcode).first()
    if item:
        item.quantity_storage -= quantity
        try:
            session.commit()
        except:
            session.rollback()
            print("error updating item quantity")


def update_cart_item_quantity_remove(cart_id, item_barcode, quantity):
    cart_item = session.query(CartItem).filter(CartItem.cart_id == cart_id,
                                               CartItem.item_barcode == item_barcode).first()
    if cart_item:
        cart_item.quantity -= quantity
        try:
            session.commit()
        except:
            session.rollback()
            print("error updating cart item quantity")


def update_cart_item_quantity_add(cart_id, item_barcode, quantity):
    cart_item = session.query(CartItem).filter(CartItem.cart_id == cart_id,
                                               CartItem.item_barcode == item_barcode).first()
    if cart_item:
        cart_item.quantity += quantity
        try:
            session.commit()
        except:
            print("error updating cart item quantity")
            session.rollback()


def update_item_quantity_add(item_barcode, quantity):
    item = session.query(controllers.Sql_Class.Item).filter(controllers.Sql_Class.Item.barcode == item_barcode).first()
    if item:
        item.quantity_storage += quantity
        try:
            session.commit()
        except:
            print("error updating item quantity")
            session.rollback()


def get_orders(customer_id):
    orders = session.query(controllers.Sql_Class.Order).filter(
        controllers.Sql_Class.Order.customer_id == customer_id).all()
    orders_arr = []
    for order in orders:
        orders_arr.append(
            Order(order.order_No, date.today(), order.customer_id, order.cart_id, order.total, order.discount))
    return orders_arr


def get_item_by_barcode(barcode):
    item = session.query(controllers.Sql_Class.Item).filter(controllers.Sql_Class.Item.barcode == barcode).first()
    return item


def get_all_cart_items(cart_id):
    results = session.query(controllers.Sql_Class.CartItem).filter(
        controllers.Sql_Class.CartItem.cart_id == cart_id).all()
    items = []
    for row in results:
        item = get_item_by_barcode(row.item_barcode)
        items.append(Item(item.barcode, item.name, item.price, row.quantity))
    if len(items) > 0:
        return items
    return None


def remove_item_from_cart(cart_id, item_barcode):
    cart_item = session.query(CartItem).filter(CartItem.cart_id == cart_id,
                                               CartItem.item_barcode == item_barcode).first()
    if cart_item:
        session.delete(cart_item)
        try:
            session.commit()
        except:
            print("error removing item from cart")
            session.rollback()


def get_item_data(item_barcode):
    try:
        item = session.query(controllers.Sql_Class.Item).filter(
            controllers.Sql_Class.Item.barcode == item_barcode).first()
        if item:
            return Item(item.barcode, item.name, item.price, item.quantity_storage)
    except:
        return None


def insert_order(cart_id, customer_id, total, discount):
    new_order = controllers.Sql_Class.Order(cart_id=cart_id, customer_id=customer_id, total=total, discount=discount)
    session.add(new_order)
    try:
        session.commit()
    except:
        print("error inserting order")
        session.rollback()
    return get_max_order_no()


def get_max_order_no():
    order = session.query(controllers.Sql_Class.Order).order_by(controllers.Sql_Class.Order.order_No.desc()).first()
    if order:
        return order.order_No
    return 0


def check_out_cart(cart_id, total, discount, customer_id):
    # update customer id in cart where cart id = cart_id to customer_id = -1
    cart = session.query(controllers.Sql_Class.Cart).filter(controllers.Sql_Class.Cart.cart_id == cart_id).first()
    if cart:
        cart.customer_id = 1
        try:
            session.commit()
        except:
            print("error checking out cart")
            session.rollback()
    # insert order
    return insert_order(cart_id, customer_id, total, discount)


def close_session():
    try:
        session.close()
    except:
        print("error closing session")
