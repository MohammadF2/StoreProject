class Cart:

    def __init__(self, cart_id, customer_id, items):
        self.cart_id = cart_id
        self.items = items
        self.customer_id = customer_id

    def __str__(self):
        return str(self.items)





    #
    # def add_item(self, item):
    #     if item in self.items:
    #         item.quantity += 1
    #         self.total += item.price
    #         return
    #     item.quantity -= 1
    #     self.items.append(item)
    #     print("please enter the quantity: ")
    #     quantity = int(input())
    #     item.quantity += quantity
    #     self.total += item.price * item.quantity
    #
    # def remove_item(self, item):
    #
    #     self.items.remove(item)
    #     self.total -= item.price * item.quantity
    #
    # def remove_item_quantity(self, item, quantity):
    #     if item.quantity < quantity:
    #         print("Not enough quantity to remove")
    #         return
    #
    #     self.total -= item.price * item.quantity
    #     item.quantity -= quantity
    #     self.total += item.price * item.quantity
    #
    # def update_item(self, item, quantity):
    #     self.total -= item.price * item.quantity
    #     item.quantity = quantity
    #     self.total += item.price * item.quantity
    #
    # def apply_discount(self, discount):
    #     if discount > 100:
    #         print("Discount cannot be more than 100%")
    #         return
    #
    #     self.total_discount = self.total - (self.total * (discount / 100))
    #
    # def sort(self):
    #     self.items.sort(key=lambda x: x.name)
    #
    # def print_all(self):
    #     self.sort()
    #     print("Total: " + str(self.total))
    #     print("Total after discount: " + str(self.total_discount))
    #     print("Items: ")
    #     for item in self.items:
    #         print(item)
    #
    # def __eq__(self, other):
    #     return self.items == other.items and self.total == other.total
