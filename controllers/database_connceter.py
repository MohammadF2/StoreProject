import mysql.connector

from model.Cart import Cart
from model.Customer import Customer
from model.Item import Item

mydb = mysql.connector.connect(
    host="training-do-user-12296595-0.b.db.ondigitalocean.com",
    port="25060",
    user="doadmin",
    database='store_database',
    password="AVNS_doi88FKQmjypaGIJD3z"
)


def get_all_customers():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM customer")
    result = cursor.fetchall()
    return result


def get_customer_by_id(customer_id):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM customer WHERE customer_id = %s", (customer_id,))
    result = cursor.fetchone()
    return result


def get_customer_order(customer_id):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM orders WHERE customer_id = %s", (customer_id,))
    result = cursor.fetchall()
    return result


def get_customer_cart(customer_id):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM cart WHERE customer_id = %s", (customer_id,))
    result = cursor.fetchall()
    return result


def create_customer(name, phone):
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO customer ( name, phone) VALUES ( %s, %s)",
                   (name, phone))
    mydb.commit()


def create_cart(customer_id):
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO cart ( customer_id) VALUES ( %s)",
                   (customer_id,))
    mydb.commit()


def get_customer_carts(customer_id):
    cursor = mydb.cursor()
    cursor.execute("SELECT cart_id, customer_id FROM cart WHERE customer_id = %s", (customer_id,))
    result = cursor.fetchall()
    if result:
        cart_id, customer_id = result[0]
        return Cart(cart_id=cart_id, customer_id=customer_id, items=[])
    else:
        cursor.execute("INSERT INTO cart ( customer_id) VALUES ( %s)", (customer_id,))
        mydb.commit()
        cursor.execute("SELECT cart_id, customer_id FROM cart WHERE customer_id = %s", (customer_id,))
        result = cursor.fetchall()
        if result:
            cart_id, customer_id = result[0]
            return Cart(cart_id=cart_id, customer_id=customer_id, items=[])
    return None


def insert_order(cart_id, customer_id, total, discount):
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO orders (cart_id, customer_id, total, discount) VALUES (%s, %s, %s, %s)",
                   (cart_id, customer_id, total, discount))
    mydb.commit()
    # get the added order id
    cursor.execute("SELECT max(order_No) FROM orders")
    result = cursor.fetchone()
    return result[0]


def get_customer_by_phone(phone):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM customer WHERE phone = %s", (phone,))
    result = cursor.fetchone()
    if result:
        customer_id, name, phone = result
        return Customer(customer_id, phone, name)
    return None


def get_last_added_cart(customer_id):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM cart WHERE customer_id = %s", (customer_id,))
    result = cursor.fetchone()
    if result:
        print(result[0])
        cart_id, customer_id = result  # Unpack the tuple
        return cart_id, customer_id  # Return both values
    return None


def get_all_items():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM item")
    result = cursor.fetchall()
    items = []

    for row in result:
        barcode, name, price, quantity = row
        item = Item(barcode, name, price, quantity)
        items.append(item)

    return items


def add_item_to_cart(cart_id, item_barcode, quantity):
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO cart_item (item_barcode, cart_id, quantity) VALUES (%s, %s, %s)",
                   (item_barcode, cart_id, quantity))
    mydb.commit()


def update_item_quantity(item_barcode, quantity):
    cursor = mydb.cursor()
    cursor.execute("UPDATE item SET quantity_storage = quantity_storage - %s WHERE barcode = %s",
                   (quantity, item_barcode))
    mydb.commit()


def update_item_quantity_add(item_barcode, quantity):
    cursor = mydb.cursor()
    cursor.execute("UPDATE item SET quantity_storage = quantity_storage + %s WHERE barcode = %s",
                   (quantity, item_barcode))
    mydb.commit()


def update_cart_item_quantity_remove(cart_id, item_barcode, quantity):
    cursor = mydb.cursor()
    cursor.execute("UPDATE cart_item SET quantity = quantity - %s WHERE cart_id = %s AND item_barcode = %s",
                   (quantity, cart_id, item_barcode))
    mydb.commit()


def update_cart_item_quantity_add(cart_id, item_barcode, quantity):
    cursor = mydb.cursor()
    cursor.execute("UPDATE cart_item SET quantity = quantity + %s WHERE cart_id = %s AND item_barcode = %s",
                   (quantity, cart_id, item_barcode))
    mydb.commit()


def get_orders(customer_id):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM orders WHERE customer_id = %s", (customer_id,))
    result = cursor.fetchall()
    return result


def get_all_cart_items(cart_id):
    items = []
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM cart_item WHERE cart_id = %s", (cart_id,))
    results = cursor.fetchall()
    for result in results:
        cursor.execute("SELECT * FROM item WHERE barcode = %s", (result[1],))
        item = cursor.fetchone()
        barcode, name, price, quantity = item
        items.append(Item(barcode, name, price, result[3]))
    return items


def remove_item_from_cart(cart_id, item_barcode):
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM cart_item WHERE cart_id = %s AND item_barcode = %s", (cart_id, item_barcode))
    mydb.commit()


def check_out_cart(cart_id, total, discount, customer_id):
    # update customer id in cart where cart id = cart_id to customer_id = -1
    cursor = mydb.cursor()
    cursor.execute("UPDATE cart SET customer_id = -1 WHERE cart_id = %s", (cart_id,))
    mydb.commit()
    # insert order
    return insert_order(cart_id, customer_id, total, discount)


def get_item_data(barcode):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM item WHERE barcode = %s", (barcode,))
    result = cursor.fetchone()
    if result:
        barcode, name, price, quantity = result
        return Item(barcode, name, price, quantity)
    return None
