class Customer:

    def __init__(self, name, cart):
        self.name = name
        self.cart = cart

    def __str__(self):
        return self.name + " " + str(self.cart)

    def __repr__(self):
        return self.name + " " + str(self.cart)

    def __eq__(self, other):
        return self.name == other.name and self.cart == other.cart
