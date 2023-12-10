import requests
import atexit

from ProjetMicroService.deploy import main as deploy
from ProjetMicroService.stop import main as stop
from ProjetMicroService.clear import main as clear


"""  
- Modifier les intéractions / menus [Click]
"""

API_GATEWAY_URL = "http://localhost:5000"

def exit_handler():
    # Handler executed when the program exits
    print("Exiting program...")
    stop()


def healthcheck():
    # Check if the containers are running
    print("Checking if the containers are running...")
    try:
        requests.post(f"{API_GATEWAY_URL}/ping")
    except Exception as e:
        print(e)
        print("Connection refused "
              "\nContainers are not running"
              "\nDeploying containers...")
        deploy()
    try:
        requests.post(f"{API_GATEWAY_URL}/ping")
    except Exception as e:
        print(f"An error occurred while deploying containers \n error: {e}")
        exit(1)
    print("Containers are running")


def purge():
    print("Purging...")
    stop()
    clear()
    deploy()


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
    role = "user"

    try:
        response = requests.post(f"{API_GATEWAY_URL}/users/public",
                                 json={"username": username, "password": password, "role": role})
    except requests.exceptions.ConnectionError:
        print("Connection refused")
        exit(1)
    if response.status_code == 201:
        print("Account created")
    else:
        print(response.status_code)
        display_error(response)


def book_commands(cmd):
    if role == "admin" or role == "user":
        if cmd == "display":
            response = requests.get(f"{API_GATEWAY_URL}/books")
            if response.status_code == 200:
                print("Number of books: " + str(len(response.json())))
                for book in response.json():
                    display_book(book)
            else:
                display_error(response)

        elif cmd == "search":
            title = input("Enter title: ")
            author = input("Enter author: ")
            response = requests.get(f"{API_GATEWAY_URL}/books/search?title={title}&author={author}")
            if response.status_code == 200:
                display_book(response.json()[0])
            else:
                display_error(response)
        else:
            print("Invalid command")
    else:
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
                response = requests.put(f"{API_GATEWAY_URL}/books/{book_id}",
                                        json={"title": "title", "author": "author"},
                                        headers={"Authorization": f"Bearer {SECRET_KEY}"})
                if response.status_code == 200:
                    print("Book updated")
                else:
                    display_error(response)
            else:
                print("Book not found")
        else:
            print("Invalid command")


def display_book(book):
    print("Title: " + book["title"])
    print("Author: " + book["author"])


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
                print("User updated")
            else:
                display_error(response)
        else:
            print("User not found")
    elif cmd == "search":
        name = input("Enter username: ")
        response = requests.get(f"{API_GATEWAY_URL}/users/search?username={username}")
        if response.status_code == 200:
            display_user(response.json()[0])
        else:
            print("User search failed")
    elif cmd == "display":
        response = requests.get(f"{API_GATEWAY_URL}/users")
        if response.status_code == 200:
            for user in response.json():
                display_user(user)

        else:
            display_error(response)
    else:
        print("Invalid command")


def display_user(user):
    print("ID:", user["id"])
    print("Username:", user["username"])
    print("Role:", user["role"])
    print()


def transaction_commands(cmd):
    global username
    if role == "user" or role == "admin":
        if cmd == "reserve":
            book_title = input("Enter book title: ")
            # delete book
            response = requests.post(
                f"{API_GATEWAY_URL}/transactions/reserve?user={username}&book={book_title}&category=reserve&value=1")
            if response.status_code == 200:
                print("Book reserved")
            else:
                print("Book reservation failed")
        elif cmd == "release":
            book_title = input("Enter book title: ")
            # delete book
            response = requests.post(
                f"{API_GATEWAY_URL}/transactions/release?user={username}&book={book_title}&category=release&value=1")
            if response.status_code == 200:
                print("Book released")
            else:
                print("Book release failed")
        else:
            print("Invalid command")
    else:
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
        print("Admin space")
        print("Here is the list of available commands\n")
        print("Write exit to exit")
        print("Write book to manage books")
        print("Write user to manage users")
        print("Write transaction to manage transactions")
        print("Write purge to purge the database and redeploy \n")
        pass
    elif role == "user":
        print("User space")
        # Client section
        print("Here is the list of available commands\n")
        print("\t exit to exit")
        print("\t books to list books")
        print("\t search to search for a book")
        print("\t reserve to reserve a book")
        print("\t release to release a book")
        pass
    else:
        print("Invalid role")
        exit(1)


def main():
    username = ""
    password = ""
    SECRET_KEY = ""
    role = ""
    logged = False
    log_try = 3
    healthcheck()
    atexit.register(exit_handler)
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
        print("=====================")
        cmd_prompt()
        command = input()
        if role == "admin":
            if command == "exit":
                break
            if command == "purge":
                purge()
            elif command == "book":
                print(
                    "\tBook service"
                    "\tAvailable commands"
                    "\tWrite cancel to exit"
                    "\tWrite add to add books"
                    "\tWrite delete to delete books"
                    "\tWrite update to update books"
                    "\tWrite display to display books"
                    "\tWrite search to search books"
                )
                book_command = input()
                if book_command == "cancel":
                    pass
                elif book_command == exit:
                    break
                else:
                    book_commands(book_command)

            elif command == "user":
                print(
                    "\tUser service"
                    "\tAvailable commands"
                    "\tWrite cancel to exit"
                    "\tWrite add to add users"
                    "\tWrite delete to delete users"
                    "\tWrite update to update users"
                    "\tWrite display to display users"
                    "\tWrite search to search users"
                )
                user_command = input()
                if user_command == "cancel":
                    pass
                elif user_command == exit:
                    break
                else:
                    user_commands(user_command)
            elif command == "transaction":
                print(
                    "\tTransaction service"
                    "\tAvailable commands"
                    "\tWrite cancel to exit"
                    "\tWrite add to add transactions"
                    "\tWrite delete to delete transactions"
                    "\tWrite update to update transactions"
                    "\tWrite display to display transactions"
                    "\tWrite search to search transactions"
                )
                transaction_command = input()
                if transaction_command == "cancel":
                    pass
                elif transaction_command == exit:
                    break
                else:
                    transaction_commands(transaction_command)
            else:
                print("Invalid command")
        elif role == "user":
            if command == "exit":
                break
            elif command == "books":
                book_commands("display")
            elif command == "search":
                book_commands("search")
            elif command == "reserve":
                transaction_commands("reserve")
            elif command == "release":
                transaction_commands("release")
            else:
                print("Invalid command")

        else:
            print("Invalid role")
            exit(1)

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


if __name__ == '__main__':
    main()