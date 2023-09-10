class Order:

    def __init__(self, order_no, date, customer_id, cart_id, total, discount):
        self.order_no = order_no
        self.date = date
        self.customer_id = customer_id
        self.cart_id = cart_id
        self.total = total
        self.discount = discount

    def __str__(self):
        return str(self.order_no) + " " + str(self.date) + " " + str(self.customer_id) + " " + str(
            self.cart_id) + " " + str(self.total) + " " + str(self.discount)

