from model.Customer import Customer


def main():
    print("Welcome to the shopping cart program, please enter your id to continue or -1 to create new user: ")
    customer_id = int(input())

    if customer_id == -1:
        print("Please enter your name: ")
        name = input()
        print("Please enter your phone number: ")
        phone = input()
        customer = Customer(customer_id, phone, name)


if __name__ == '__main__':
    main()
