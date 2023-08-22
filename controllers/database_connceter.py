import mysql.connector

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
    cursor.execute("SELECT * FROM cart WHERE customer_id = %s", (customer_id,))
    result = cursor.fetchall()
    return result

def insert_order(cart_id, customer_id, total, discount):
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO orders (cart_id, customer_id, total, discount) VALUES (%s, %s, %s, %s)",
                   (cart_id, customer_id, total, discount))
    mydb.commit()
    #get the added order id
    cursor.execute("SELECT LAST_INSERT_ID()")
    result = cursor.fetchone()
    return result[0]
