class Item:

    def __init__(self, barcode, name, price, quantity):
        self.barcode = barcode
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return self.name + ", price: " + str(self.price) + ", quantity: " + str(self.quantity)

    def __repr__(self):
        return self.barcode + " " + self.name + " " + str(self.price) + " " + str(self.quantity)

    def __eq__(self, other):
        return self.barcode == other.barcode
