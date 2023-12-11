import requests
from CLI.CommandHandler.utils import API_GATEWAY_URL, display_error


class UserCommandHandler:
    def __init__(self, session_user):
        self.session_user = session_user

    def handle_command(self, command):
        if command == "add":
            self.add_user()
        elif command == "delete":
            self.delete_user()
        elif command == "update":
            self.update_user()
        elif command == "search":
            self.search_user()
        elif command == "display":
            self.display_users()
        else:
            print("Invalid user command")

    def add_user(self):
        name = input("Enter username: ")
        pwd = input("Enter password: ")
        role = input("Enter role: ")
        response = requests.post(
            f"{API_GATEWAY_URL}/users",
            json={"username": name, "password": pwd, "role": role},
            headers={"Authorization": f"Bearer {self.session_user.secret_key}"},
        )
        if response.status_code == 201:
            print("User added")
        else:
            display_error(response)

    def delete_user(self):
        name = input("Enter username: ")
        pwd = input("Enter password: ")
        response = requests.get(
            f"{API_GATEWAY_URL}/users/search?username={name}&password={pwd}"
        )
        if response.status_code == 200:
            user_id = response.json()[0]["id"]
            response = requests.delete(
                f"{API_GATEWAY_URL}/users/{user_id}",
                headers={"Authorization": f"Bearer {self.session_user.secret_key}"},
            )
            if response.status_code == 200:
                print("User deleted")
            else:
                display_error(response)
        else:
            print("User not found")

    def update_user(self):
        name = input("Enter username: ")
        pwd = input("Enter password: ")
        response = requests.get(
            f"{API_GATEWAY_URL}/users/search?username={name}&password={pwd}"
        )
        if response.status_code == 200:
            user_id = response.json()[0]["id"]
            new_username = input("Enter new username: ")
            new_password = input("Enter new password: ")
            new_role = input("Enter new role: ")
            response = requests.put(
                f"{API_GATEWAY_URL}/users/{user_id}",
                json={
                    "username": new_username,
                    "password": new_password,
                    "role": new_role,
                },
                headers={"Authorization": f"Bearer {self.session_user.secret_key}"},
            )
            if response.status_code == 200:
                print("User updated")
            else:
                display_error(response)
        else:
            print("User not found")

    def search_user(self):
        name = input("Enter username: ")
        response = requests.get(f"{API_GATEWAY_URL}/users/search?username={name}")
        if response.status_code == 200:
            self.display_user(response.json()[0])
        else:
            print("User search failed")

    def display_users(self):
        response = requests.get(f"{API_GATEWAY_URL}/users")
        if response.status_code == 200:
            for user in response.json():
                self.display_user(user)
        else:
            display_error(response)

    @staticmethod
    def display_user(user):
        print(f"ID: {user['id']}, Username: {user['username']}, Role: {user['role']}")

    @staticmethod
    def display_functions(role):
        if role == "admin":
            print(
                "Available commands:",
                "\n - \033[36madd\033[0m",
                "\n - \033[36mdelete\033[0m",
                "\n - \033[36mupdate\033[0m",
                "\n - \033[36msearch\033[0m",
                "\n - \033[36mdisplay\033[0m",
            )
