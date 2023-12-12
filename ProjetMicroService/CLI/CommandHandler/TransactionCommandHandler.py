import requests

from CLI.CommandHandler.utils import API_GATEWAY_URL


class TransactionCommandHandler:
    def __init__(self, session_user):
        self.session_user = session_user

    def handle_command(self, command):
        if command == "reserve":
            self.reserve_book()
        elif command == "release":
            self.release_book()
        elif command == "add":
            self.add_transaction()
        elif command == "delete":
            self.delete_transaction()
        elif command == "update":
            self.update_transaction()
        elif command == "display":
            self.display_transactions()
        elif command == "search":
            self.search_transactions()
        else:
            print("Invalid transaction command")

    def reserve_book(self):
        if self.session_user.role in ["admin", "user"]:
            book_title = input("Enter book title: ")
            response = requests.post(
                f"{API_GATEWAY_URL}/transactions/reserve?"
                f"user={self.session_user.username}&"
                f"book={book_title}&"
                f"category=reserve&"
                f"value=1"
            )
            if response.status_code == 200:
                print("Book reserved")
            else:
                print("Book reservation failed")

    def release_book(self):
        if self.session_user.role in ["admin", "user"]:
            book_title = input("Enter book title: ")
            response = requests.post(
                f"{API_GATEWAY_URL}/transactions/release?"
                f"user={self.session_user.username}&"
                f"book={book_title}&"
                f"category=release&"
                f"value=1"
            )
            if response.status_code == 200:
                print("Book released")
            else:
                print("Book release failed")

    def add_transaction(self):
        user = input("Enter user: ")
        book = input("Enter book: ")
        response = requests.post(
            f"{API_GATEWAY_URL}/transactions",
            json={"user": user, "book": book},
            headers={"Authorization": f"Bearer {self.session_user.secret_key}"},
        )
        if response.status_code == 201:
            print("Transaction added")
        else:
            print("Transaction addition failed")

    def delete_transaction(self):
        transaction_id = input("Enter transaction id: ")
        response = requests.delete(
            f"{API_GATEWAY_URL}/transactions/{transaction_id}",
            headers={"Authorization": f"Bearer {self.session_user.secret_key}"},
        )
        if response.status_code == 200:
            print("Transaction deleted")
        else:
            print("Transaction deletion failed")

    def update_transaction(self):
        transaction_id = input("Enter transaction id: ")
        response = requests.put(
            f"{API_GATEWAY_URL}/transactions/{transaction_id}",
            json={"user": "user", "book": "book"},
            headers={"Authorization": f"Bearer {self.session_user.secret_key}"},
        )
        if response.status_code == 200:
            print("Transaction updated")
        else:
            print("Transaction update failed")

    @staticmethod
    def display_transactions():
        response = requests.get(f"{API_GATEWAY_URL}/transactions")
        if response.status_code == 200:
            print(response.json())
        else:
            print("Transaction display failed")

    @staticmethod
    def search_transactions():
        user = input("Enter user: ")
        book = input("Enter book: ")
        response = requests.get(
            f"{API_GATEWAY_URL}/transactions/search?user={user}&book={book}"
        )
        if response.status_code == 200:
            print(response.json())
        else:
            print("Transaction search failed")

    @staticmethod
    def display_functions(role):
        if role == "admin":
            print("Admin commands:")
            print("\n - \033[36mreserve\033[0m")
            print("\n - \033[36mrelease\033[0m")
            print("\n - \033[36madd\033[0m")
            print("\n - \033[36mdelete\033[0m")
            print("\n - \033[36mupdate\033[0m")
            print("\n - \033[36mdisplay\033[0m")
            print("\n - \033[36msearch\033[0m")
