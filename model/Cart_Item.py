class CartItem:

    def __init__(self, barcode, quantity):
        self.barcode = barcode
        self.quantity = quantity

    def __str__(self):
        return str(self.barcode) + " " + str(self.quantity)

    def __eq__(self, other):
        return self.barcode == other.barcode
