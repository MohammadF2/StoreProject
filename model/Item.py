class Item:

    def __init__(self, barcode, name, price, quantity):
        self.barcode = barcode
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        if self.quantity == 0:
            return self.name + ", price: " + str(self.price) + ", quantity: out of stock"
        return self.name + ", price: " + str(self.price) + ", quantity: " + str(self.quantity)

    def __eq__(self, other):
        return self.barcode == other.barcode
