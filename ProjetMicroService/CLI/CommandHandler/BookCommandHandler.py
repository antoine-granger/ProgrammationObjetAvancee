import requests
from CLI.CommandHandler.utils import API_GATEWAY_URL, display_error


class BookCommandHandler:
    def __init__(self, session_user):
        self.session_user = session_user

    def handle_command(self, command):
        if command == "display":
            self.display_books()
        elif command == "search":
            self.search_books()
        elif command == "add":
            self.add_book()
        elif command == "delete":
            self.delete_book()
        elif command == "update":
            self.update_book()
        else:
            print("Invalid book command")

    def display_books(self):
        response = requests.get(f"{API_GATEWAY_URL}/books")
        if response.status_code == 200:
            print("Number of books: " + str(len(response.json())))
            for book in response.json():
                self.display_book(book)
        else:
            display_error(response)

    def search_books(self):
        title = input("Enter title: ")
        author = input("Enter author: ")
        response = requests.get(
            f"{API_GATEWAY_URL}/books/search?title={title}&author={author}"
        )
        if response.status_code == 200:
            self.display_book(response.json()[0])
        else:
            display_error(response)

    def add_book(self):
        if self.session_user.role in ["admin"]:
            title = input("Enter title: ")
            author = input("Enter author: ")
            response = requests.post(
                f"{API_GATEWAY_URL}/books",
                json={"title": title, "author": author},
                headers={"Authorization": f"Bearer {self.session_user.secret_key}"},
            )
            if response.status_code == 201:
                print("Book added")
            else:
                display_error(response)
        else:
            print("Permission denied")

    def delete_book(self):
        if self.session_user.role in ["admin"]:
            title = input("Enter title: ")
            author = input("Enter author: ")
            response = requests.get(
                f"{API_GATEWAY_URL}/books/search?title={title}&author={author}"
            )
            if response.status_code == 200:
                book_id = response.json()[0]["id"]
                response = requests.delete(
                    f"{API_GATEWAY_URL}/books/{book_id}",
                    headers={"Authorization": f"Bearer {self.session_user.secret_key}"},
                )
                if response.status_code == 200:
                    print("Book deleted")
                else:
                    display_error(response)
            else:
                display_error(response)
        else:
            print("Permission denied")

    def update_book(self):
        if self.session_user.role in ["admin"]:
            title = input("Enter title: ")
            author = input("Enter author: ")
            response = requests.get(
                f"{API_GATEWAY_URL}/books/search?title={title}&author={author}"
            )
            if response.status_code == 200:
                book_id = response.json()[0]["id"]
                response = requests.put(
                    f"{API_GATEWAY_URL}/books/{book_id}",
                    json={"title": "title", "author": "author"},
                    headers={"Authorization": f"Bearer {self.session_user.secret_key}"},
                )
                if response.status_code == 200:
                    print("Book updated")
                else:
                    display_error(response)
            else:
                print("Book not found")
        else:
            print("Permission denied")

    @staticmethod
    def display_book(book):
        print("Title: " + book["title"])
        print("Author: " + book["author"])

    @staticmethod
    def display_functions(role):
        if role == "admin":
            print(
                "Available commands:",
                "\n - \033[36mdisplay\033[0m",
                "\n - \033[36msearch\033[0m",
                "\n - \033[36madd\033[0m",
                "\n - \033[36mdelete\033[0m",
                "\n - \033[36mupdate\033[0m",
            )
        elif role == "user":
            print(
                "Available commands:",
                "\n - \033[36mdisplay\033[0m",
                "\n - \033[36msearch\033[0m",
            )
