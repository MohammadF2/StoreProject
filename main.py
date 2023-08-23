from controllers.database_connceter import create_customer, get_customer_by_phone, create_cart, get_customer_carts, \
    get_last_added_cart, get_all_items, add_item_to_cart, get_orders, update_item_quantity, get_all_cart_items, \
    remove_item_from_cart, update_item_quantity_add, update_cart_item_quantity_remove, update_cart_item_quantity_add, \
    check_out_cart, get_item_data
from model.Cart import Cart
from model.Customer import Customer


def print_menu():
    print("Please select an option: ")
    print("1. Add item to cart: ")
    print("2. Remove item from cart: ")
    print("3. Update quantity of an item: ")
    print("4. Show cart: ")
    print("5. Checkout: ")
    print("6. Show orders: ")
    print("7. Exit")


def main():
    print("Welcome to the shopping cart program, please enter your phone number to continue or -1 to create new user: ")
    customer_phone = int(input())

    customer = None

    if customer_phone == -1:
        print("Please enter your name: ")
        name = input()
        print("Please enter your phone number: ")
        phone = input()
        id = create_customer(name, phone)
        customer = Customer(id, phone, name)
        create_cart(customer.customer_id)
    else:
        customer = get_customer_by_phone(customer_phone)
        if customer is None:
            print("Customer not found")
            return

    print("Welcome " + customer.name + " please select an option: ")
    print_menu()
    choice = int(input())

    cart = get_customer_carts(customer.customer_id)

    items = get_all_items()

    while choice != 7:
        if choice == 1:
            print("Please select an item (enter its number): ")
            count = 0
            for item in items:
                print(str(count + 1) + " - " + item.__str__())
            print("Please enter the item barcode or -1 to cancel: ")
            item_barcode = int(input())
            if item_barcode == -1:
                print_menu()
                choice = int(input())
                continue
            if items[item_barcode - 1].quantity == 0:
                print("This item is out of stock")
                continue
            print("Please enter the quantity: ")
            quantity = int(input())

            while quantity <= 0:
                print("Please enter a valid quantity: ")
                quantity = int(input())
            while quantity > items[item_barcode - 1].quantity:
                print(f'We only have {items[item_barcode - 1].quantity} of this item, please enter a valid quantity: ')
                quantity = int(input())
            add_item_to_cart(cart.cart_id, items[item_barcode - 1].barcode, quantity)
            update_item_quantity(items[item_barcode - 1].barcode, quantity)
            items[item_barcode - 1].quantity -= quantity
        elif choice == 2:
            print("You selected the option to remove item from cart")
            items_cart = get_all_cart_items(cart.cart_id)
            print("Please select an item (enter its number): ")
            count = 0
            for item in items_cart:
                print(str(count + 1) + " - " + item.__str__())
                count += 1
            print("Please enter the item barcode or -1 to cancel: ")
            item_barcode = int(input())
            if item_barcode == -1:
                print_menu()
                choice = int(input())
            if item_barcode > len(items_cart) or item_barcode < 0:
                print("Invalid item")
                continue
            remove_item_from_cart(cart.cart_id, items_cart[item_barcode - 1].barcode)
            update_item_quantity_add(items_cart[item_barcode - 1].barcode, items_cart[item_barcode - 1].quantity)
            items[item_barcode - 1].quantity += items_cart[item_barcode - 1].quantity
            items_cart.pop(item_barcode - 1)
        elif choice == 3:
            print("You selected the option to update quantity of an item")
            items_cart = get_all_cart_items(cart.cart_id)
            print("Please select an item (enter its number): ")
            count = 0
            for item in items_cart:
                print(str(count + 1) + " - " + item.__str__())
                count += 1
            print("Please enter the item barcode or -1 to cancel: ")
            item_barcode = int(input())
            if item_barcode == -1:
                print_menu()
                choice = int(input())
                continue
            print("Please enter the quantity: ")
            quantity = int(input())
            while quantity < 0:
                print("Please enter a valid quantity: ")
                quantity = int(input())
            if quantity == 0:
                print("You selected to remove the item")
                remove_item_from_cart(cart.cart_id, items_cart[item_barcode - 1].barcode)
                update_item_quantity_add(items_cart[item_barcode - 1].barcode, items_cart[item_barcode - 1].quantity)
                items[item_barcode - 1].quantity += items_cart[item_barcode - 1].quantity
                items_cart.pop(item_barcode - 1)
                print_menu()
                choice = int(input())
                continue
            while quantity > (items[item_barcode - 1].quantity + items_cart[item_barcode - 1].quantity):
                print(f'We only have {items[item_barcode - 1].quantity} of this item, please enter a valid quantity ('
                      f'Or enter -1 to cancel): ')
                quantity = int(input())
                if quantity == -1:
                    print_menu()
                    choice = int(input())
                    continue
            if quantity < items_cart[item_barcode - 1].quantity:
                print("You selected to remove some quantity of the item")
                update_item_quantity_add(items[item_barcode - 1].barcode, quantity)
                update_cart_item_quantity_remove(cart_id=cart.cart_id, item_barcode=items[item_barcode - 1].barcode, quantity=quantity)
                items[item_barcode - 1].quantity += quantity
            elif quantity > items_cart[item_barcode - 1].quantity:
                print("You selected to add some quantity of the item")
                update_cart_item_quantity_add(cart_id=cart.cart_id, item_barcode=items[item_barcode - 1].barcode, quantity=quantity)
                update_item_quantity(items[item_barcode - 1].barcode, quantity)
                items[item_barcode - 1].quantity -= quantity
        elif choice == 4:
            print("You selected the option to show cart")
            cart_items = get_all_cart_items(cart.cart_id)
            for cart_item in cart_items:
                print(cart_item)
        elif choice == 5:
            print("You selected the option to checkout")
            cart_items = get_all_cart_items(cart.cart_id)
            if len(cart_items) == 0:
                print("You have no items in your cart")
                print_menu()
                choice = int(input())
                continue
            total = 0
            for cart_item in cart_items:
                total += cart_item.price * cart_item.quantity
            print("Total: " + str(total))
            print("Do you have discount? (y/n): ")
            discount = input()
            if discount == 'y':
                print("Please enter the discount percentage: ")
                discount = int(input())
                while discount > 100 or discount < 0:
                    print("Please enter a valid discount percentage: ")
                    discount = int(input())
                total = total - (total * (discount / 100))
            print("total after discount: " + str(total))
            print("Do you want to checkout? (y/n): ")
            checkout = input()
            if checkout == 'y':
                #TODO: checkout
                order_no = check_out_cart(cart.cart_id, total, discount, customer.customer_id)
                print("Your order number is: " + str(order_no))
                print("Thank you for shopping with us")
                pass
            else:
                print_menu()
                choice = int(input())
                continue
        elif choice == 6:
            print("You selected the option to show orders")
            orders = get_orders(customer.customer_id)
            if len(orders) == 0:
                print("You have no orders")
            else:
                for order in orders:
                    order_no, customer_id, cart_id, discount, total = order
                    print("Order number: " + str(order_no) + " Total: " + str(total) + " Discount: " + str(discount))
                print("Please enter the order number to show its items (If you dont want enter -1): ")
                order_no = int(input())
                if order_no == -1:
                    print_menu()
                    choice = int(input())
                    continue
                for order in orders:
                    if order[0] == order_no:
                        order_no, customer_id, cart_id, discount, total = order
                        cart_items = get_all_cart_items(cart_id)
                        for cart_item in cart_items:
                            item = get_item_data(cart_item.barcode)
                            print(item.name + ", price:" + str(item.price) + ", quantity:" + str(cart_item.quantity))
                        print("order_No: " + str(order_no) + " Total: " + str(total) + " Discount: " + str(discount))
                        break
        elif choice == 7:
            print("You selected the option to exit")
        else:
            print("Invalid option")
        print_menu()
        choice = int(input())


if __name__ == '__main__':
    main()
