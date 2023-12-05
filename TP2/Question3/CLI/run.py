### Imports
import requests
import os
import jwt

# TODO
"""  
- Modifier les intéractions / menus [Click]
- Gestion de l'interface user
- Inscription 
"""

### Global variables
API_GATEWAY_URL = "http://localhost:5000"
username = ""
password = ""
SECRET_KEY = ""
role = ""
logged = False
log_try = 3


# Login interface


def display_error(response):
    print(response.json()["message"])


def log_in():
    global username, password, SECRET_KEY, role, logged, log_try
    print("Please enter your credentials\n")
    username = input("Username: ")
    password = input("Password: ")
    try:
        response = requests.post(f"{API_GATEWAY_URL}/login", json={"username": username, "password": password})
    except requests.exceptions.ConnectionError:
        print("Connection refused")
        exit(1)
    if response.status_code == 200:
        SECRET_KEY = response.json()["token"]
        logged = True
    else:
        display_error(response)
        if log_try <= 0:
            print("Too many login attempts")
            exit(1)
        log_try -= 1
        print("You have " + str(log_try) + " attempts left")


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
        display_error(response)
        exit(1)


def book_commands(cmd):
    if cmd == "add":
        title = input("Enter title: ")
        author = input("Enter author: ")
        response = requests.post(f"{API_GATEWAY_URL}/books", json={"title": title, "author": author},
                                 headers={"Authorization": f"Bearer {SECRET_KEY}"})
        if response.status_code == 201:
            print("Book added")
        else:
            display_error(response)

    elif cmd == "delete":
        title = input("Enter title: ")
        author = input("Enter author: ")
        response = requests.get(f"{API_GATEWAY_URL}/books/search?title={title}&author={author}")
        if response.status_code == 200:
            book_id = response.json()[0]["id"]
            response = requests.delete(f"{API_GATEWAY_URL}/books/{book_id}",
                                       headers={"Authorization": f"Bearer {SECRET_KEY}"})
            if response.status_code == 200:
                print("Book deleted")
            else:
                display_error(response)
        else:
            display_error(response)

    elif cmd == "update":
        title = input("Enter title: ")
        author = input("Enter author: ")
        response = requests.get(f"{API_GATEWAY_URL}/books/search?title={title}&author={author}")
        if response.status_code == 200:
            book_id = response.json()[0]["id"]
            response = requests.put(f"{API_GATEWAY_URL}/books/{book_id}", json={"title": "title", "author": "author"},
                                    headers={"Authorization": f"Bearer {SECRET_KEY}"})
            if response.status_code == 200:
                print("Book updated")
            else:
                display_error(response)
        else:
            print("Book not found")

    elif cmd == "display":
        response = requests.get(f"{API_GATEWAY_URL}/books")
        if response.status_code == 200:
            print(response.json())
        else:
            display_error(response)

    elif cmd == "search":
        title = input("Enter title: ")
        author = input("Enter author: ")
        response = requests.get(f"{API_GATEWAY_URL}/books/search?title={title}&author={author}")
        if response.status_code == 200:
            print(response.json())
        else:
            display_error(response)

    else:
        print("Invalid command")


def user_commands(cmd):
    if cmd == "add":
        name = input("Enter username: ")
        pwd = input("Enter password: ")
        r = input("Enter role: ")
        response = requests.post(f"{API_GATEWAY_URL}/users", json={"username": name, "password": pwd, "role": r},
                                 headers={"Authorization": f"Bearer {SECRET_KEY}"})
        if response.status_code == 201:
            print("User added")
        else:

            display_error(response)
    elif cmd == "delete":
        name = input("Enter username: ")
        pwd = input("Enter password: ")
        response = requests.get(f"{API_GATEWAY_URL}/users/search?username={name}&password={pwd}")
        if response.status_code == 200:
            user_id = response.json()[0]["id"]
            response = requests.delete(f"{API_GATEWAY_URL}/users/{user_id}",
                                       headers={"Authorization": f"Bearer {SECRET_KEY}"})
            if response.status_code == 200:
                print("User deleted")
            else:

                display_error(response)
        else:
            print("User not found")
    elif cmd == "update":
        name = input("Enter username: ")
        pwd = input("Enter password: ")
        response = requests.get(f"{API_GATEWAY_URL}/users/search?username={name}&password={pwd}")
        if response.status_code == 200:
            user_id = response.json()[0]["id"]
            response = requests.put(f"{API_GATEWAY_URL}/users/{user_id}",
                                    json={"username": "username", "password": "password", "role": "role"},
                                    headers={"Authorization": f"Bearer {SECRET_KEY}"})
            if response.status_code == 200:

                display_error(response)
            else:
                display_error(response)
        else:
            print("User not found")
    elif cmd == "display":
        response = requests.get(f"{API_GATEWAY_URL}/users")
        if response.status_code == 200:
            for user in response.json():
                print("ID:", user["id"])
                print("Username:", user["username"])
                print("Role:", user["role"])
                print()

        else:
            display_error(response)
    elif cmd == "search":
        name = input("Enter username: ")
        pwd = input("Enter password: ")
        response = requests.get(f"{API_GATEWAY_URL}/users/search?username={username}&password={password}")
        if response.status_code == 200:
            print(response.json())
        else:
            print("User search failed")
    else:
        print("Invalid command")


def transaction_commands(cmd):
    if cmd == "add":
        user = input("Enter user: ")
        book = input("Enter book: ")
        response = requests.post(f"{API_GATEWAY_URL}/transactions", json={"user": user, "book": book},
                                 headers={"Authorization": f"Bearer {SECRET_KEY}"})
        if response.status_code == 201:
            print("Transaction added")
        else:
            print("Transaction addition failed")
    elif cmd == "delete":
        transaction_id = input("Enter transaction id: ")
        response = requests.delete(f"{API_GATEWAY_URL}/transactions/{transaction_id}",
                                   headers={"Authorization": f"Bearer {SECRET_KEY}"})
        if response.status_code == 200:
            print("Transaction deleted")
        else:
            print("Transaction deletion failed")
    elif cmd == "update":
        transaction_id = input("Enter transaction id: ")
        response = requests.put(f"{API_GATEWAY_URL}/transactions/{transaction_id}",
                                json={"user": "user", "book": "book"},
                                headers={"Authorization": f"Bearer {SECRET_KEY}"})
        if response.status_code == 200:
            print("Transaction updated")
        else:
            print("Transaction update failed")
    elif cmd == "display":
        response = requests.get(f"{API_GATEWAY_URL}/transactions")
        if response.status_code == 200:
            print(response.json())
        else:
            print("Transaction display failed")
    elif cmd == "search":
        user = input("Enter user: ")
        book = input("Enter book: ")
        response = requests.get(f"{API_GATEWAY_URL}/transactions/search?user={user}&book={book}")
        if response.status_code == 200:
            print(response.json())
        else:
            print("Transaction search failed")
    else:
        print("Invalid command")


def cmd_prompt():
    if role == "admin":
        # Admin section
        print("Here is the list of available commands\n")
        print("Write exit to exit")
        print("Write book to manage books")
        print("Write user to manage users")
        print("Write transaction to manage transactions")
        pass
    elif role == "user":
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


## ============  Main section ============ ##

print("Welcome to the library\n")
while not logged:
    print("Write login to log or register to create an account \n")
    command = input()
    if command == "login":
        log_in()
    elif command == "register":
        register()
    else:
        print("Invalid command")
        exit(1)
r = requests.get(f"{API_GATEWAY_URL}/users/search?username={username}&password={password}")
role = r.json()[0]["role"]
print(role)
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
        print("\tUser service")
        print("\tAvailable commands")
        print("\tWrite cancel to exit")
        print("\tWrite add to add users")
        print("\tWrite delete to delete users")
        print("\tWrite update to update users")
        print("\tWrite display to display users")
        print("\tWrite search to search users")
        user_command = input()
        if user_command == "cancel":
            pass
        elif user_command == exit:
            break
        else:
            user_commands(user_command)
    elif command == "transaction":
        print("\tTransaction service")
        print("\tAvailable commands")
        print("\tWrite cancel to exit")
        print("\tWrite add to add transactions")
        print("\tWrite delete to delete transactions")
        print("\tWrite update to update transactions")
        print("\tWrite display to display transactions")
        print("\tWrite search to search transactions")
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
