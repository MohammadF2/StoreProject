class Customer:

    def __init__(self, customer_id, phone, name):
        self.customer_id = customer_id
        self.phone = phone
        self.name = name

    def __str__(self):
        return self.name + " " + str(self.phone)

    def __eq__(self, other):
        return self.customer_id == other.customer_id
