### Imports
import requests
import os
import jwt

### Global variables
API_GATEWAY_URL = "http://localhost:5000"
SECRET_KEY = os.environ.get('SECRET_KEY')

username = ""
password = ""
role = "admin"
# Login interface

print("Welcome to the library\n" + "Write login to log or register to create an account")
command = input()


def log_in():
    global username, password
    print("Please enter your credentials\n")
    username = input("Username: ")
    password = input("Password: ")
    logged = False
    log_try = 1
    try:
        response = requests.post(f"{API_GATEWAY_URL}/login", json={"username": username, "password": password})
    except requests.exceptions.ConnectionError:
        print("Connection refused")
        exit(1)
    while not logged:
        if response.status_code == 200:

            user_data = response.json()
            print("Your token is: ", user_data)
            logged = True
        else:
            print("Login failed")
            print("You have " + str(3 - log_try) + " attempts left")
            username = input("Username: ")
            password = input("Password: ")
            response = requests.post(f"{API_GATEWAY_URL}/login", json={"username": username, "password": password})
            log_try += 1
            if log_try > 3:
                print("Too many login attempts")
                exit(1)


def register():
    global username, password, role
    print("Please choose your credentials\n")
    username = input("Username: ")
    password = input("Password: ")
    role = "admin"
    response = requests.post(f"{API_GATEWAY_URL}/users",
                             json={"username": username, "password": password, "role": role})
    print(response.json())
    if response.status_code == 201:
        print("Account created")
    else:
        print("Account creation failed")
        exit(1)


if command == "login":
    log_in()
elif command == "register":
    register()
else:
    print("Invalid command")
    exit(1)




def book_commands(cmd):
    if cmd == "add":
        title = input("Enter title: ")
        author = input("Enter author: ")
        response = requests.post(f"{API_GATEWAY_URL}/books", json={"title": title, "author": author})
        if response.status_code == 201:
            print("Book added")
        else:
            print("Book addition failed")

    elif cmd == "delete":
        title = input("Enter title: ")
        author = input("Enter author: ")
        response = requests.get(f"{API_GATEWAY_URL}/books/search?title={title}&author={author}")
        if response.status_code == 200:
            book_id = response.json()[0]["id"]
            response = requests.delete(f"{API_GATEWAY_URL}/books/{book_id}")
            if response.status_code == 200:
                print("Book deleted")
            else:
                print("Book deletion failed")
        else:
            print("Book not found")

    elif cmd == "update":
        title = input("Enter title: ")
        author = input("Enter author: ")
        response = requests.get(f"{API_GATEWAY_URL}/books/search?title={title}&author={author}")
        if response.status_code == 200:
            book_id = response.json()[0]["id"]
            response = requests.put(f"{API_GATEWAY_URL}/books/{book_id}", json={"title": "title", "author": "author"})
            if response.status_code == 200:
                print("Book updated")
            else:
                print("Book update failed")
        else:
            print("Book not found")

    elif cmd == "display":
        response = requests.get(f"{API_GATEWAY_URL}/books")
        if response.status_code == 200:
            print(response.json())
        else:
            print("Book display failed")

    elif cmd == "search":
        title = input("Enter title: ")
        author = input("Enter author: ")
        response = requests.get(f"{API_GATEWAY_URL}/books/search?title={title}&author={author}")
        if response.status_code == 200:
            print(response.json())
        else:
            print("Book search failed")

    else:
        print("Invalid command")


def user_commands(cmd):
    pass


def transaction_commands(transaction_command):
    pass


def cmd_prompt():
    if role == "admin":
        # Admin section
        print("Here is the list of available commands\n")
        print("Write exit to exit")
        print("Write book to manage books")
        print("Write user to manage users")
        print("Write transaction to manage transactions")
        pass
    elif role == "client":
        # Client section
        print("Here is the list of available commands\n")
        print("\t exit to exit")
        print("\t book to manage books")
        print("\t user to manage users")
        print("\t transaction to manage transactions")
        pass
    else:
        print("Invalid role")
        exit(1)


while True:
    cmd_prompt()
    command = input()
    if command == "exit":
        break
    elif command == "book":
        print("\tBook service")
        print("\tAvailable commands")
        print("\tWrite cancel to exit")
        print("\tWrite add to add books")
        print("\tWrite delete to delete books")
        print("\tWrite update to update books")
        print("\tWrite display to display books")
        print("\tWrite search to search books")
        book_command = input()
        if book_command == "cancel":
            pass
        elif book_command == exit:
            break
        else:
            book_commands(book_command)

    elif command == "user":
        print("User service")
        print("Available commands")
        print("Write cancel to exit")
        print("Write add to add users")
        print("Write delete to delete users")
        print("Write update to update users")
        print("Write display to display users")
        print("Write search to search users")
        user_command = input()
        if user_command == "cancel":
            pass
        elif user_command == exit:
            break
        else:
            user_commands(user_command)
    elif command == "transaction":
        print("Transaction service")
        print("Available commands")
        print("Write cancel to exit")
        print("Write add to add transactions")
        print("Write delete to delete transactions")
        print("Write update to update transactions")
        print("Write display to display transactions")
        print("Write search to search transactions")
        transaction_command = input()
        if transaction_command == "cancel":
            pass
        elif transaction_command == exit:
            break
        else:
            transaction_commands(transaction_command)

    # Display list of actions

    ## Admin section
    # Book service
    # Add, Remove, Update book

    # User service
    # Add, Remove, Update user

    # Transaction service
    # Add, Remove, Update transaction

    ## Client section
    # Book service
    # Display list of books, Search books by title, Search books by author, Borrow book

    # User service
    # Update self account

    else:
        print("Invalid command")
