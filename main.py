from model.Item import Item
from model.Customer import Customer
from model.Cart import Cart


def print_menu(cart):
    for i in range(len(cart.items)):
        print(str(i + 1) + ". " + str(cart.items[i]))
    item = int(input())
    print("How many do you want?")
    quantity = int(input())

    return quantity, item


def main():
    print("Welcome to the shop!")
    print("Please enter your name:")
    name = input()

    cart = Cart([], 0.0)
    customer = Customer(cart=cart, name=name)

    items = [Item(123, "Apple", 5, 1), Item(124, "Orange", 3, 1), Item(125, "Banana", 1, 1)]

    while True:
        print("What do you want to do?")
        print("1. Add item to cart")
        print("2. Remove item from cart")
        print("3. Update item quantity")
        print("4. Return some quantity of an item")
        print("5. Apply discount")
        print("6. Print cart")
        print("7. Exit")
        choice = int(input())

        if choice == 1:
            print("Which item do you want to add?")
            for i in range(len(items)):
                print(str(i + 1) + ". " + str(items[i].__str__()))
            item = int(input())
            cart.add_item(items[item - 1])
        elif choice == 2:
            print("Which item do you want to remove?")
            for i in range(len(cart.items)):
                print(str(i + 1) + ". " + str(cart.items[i]))
            item = int(input())
            items[item - 1].quantity = 1
            cart.remove_item(cart.items[item - 1])
        elif choice == 3:
            print("Which item do you want to update?")
            quantity, item = print_menu(cart)
            cart.update_item(cart.items[item - 1], quantity)
        elif choice == 4:
            print("Which item do you want to return some of it?")
            quantity, item = print_menu(cart)
            cart.remove_item_quantity(cart.items[item - 1], quantity)
        elif choice == 5:
            print("What is the discount?")
            discount = float(input())
            cart.apply_discount(discount)
        elif choice == 6:
            cart.print_all()
        elif choice == 7:
            break
        else:
            print("Invalid choice!")

    if cart.total_discount == 0:
        cart.total_discount = cart.total

    print("Thank you for shopping with us, " + customer.name + "!")
    print("Your cart:")
    cart.print_all()
    print("total before discount: " + str(cart.total))
    print("total after discount: " + str(cart.total_discount))
    print("Goodbye!")


if __name__ == '__main__':
    main()