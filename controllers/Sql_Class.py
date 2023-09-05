from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, registry
from sqlalchemy.orm import declarative_base

# Create a MySQL database connection
DATABASE_URL = "mysql://root:123456789@localhost/store_database"
engine = create_engine(DATABASE_URL, echo=True)  # Set echo=True for debugging

# Create a base class for declarative models
Base = declarative_base()


# Define the User model
class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
    phone = Column(String(32))


class Cart(Base):
    __tablename__ = 'cart'

    cart_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))

    # Define the many-to-one relationship with Customer
    customer = relationship('Customer')
    cart_items = relationship('CartItem')


class Item(Base):
    __tablename__ = 'item'

    barcode = Column(Integer, primary_key=True)
    name = Column(String(16))
    price = Column(Float)
    quantity_storage = Column(Integer)

    cart_items = relationship('CartItem')


class CartItem(Base):
    __tablename__ = 'cart_item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_barcode = Column(Integer, ForeignKey('item.barcode'))
    cart_id = Column(Integer, ForeignKey('cart.cart_id'))
    quantity = Column(Integer)

    # Define the many-to-one relationships with Item and Cart



class Order(Base):
    __tablename__ = 'orders'

    order_No = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    cart_id = Column(Integer, ForeignKey('cart.cart_id'))
    discount = Column(Float)
    total = Column(Float)

    # Define relationships to customer and cart
    customer = relationship('Customer')
    cart = relationship('Cart')
