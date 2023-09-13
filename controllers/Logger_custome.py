try:
    choice = int(input("Enter your choice: "))
    print(choice)
except ValueError:
    print("Please enter a valid choice")
    exit(0)