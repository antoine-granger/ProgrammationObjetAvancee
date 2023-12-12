from getpass import getpass

import requests
from requests import RequestException

from CLI.User.User import User

API_GATEWAY_URL = "http://localhost:5000"


class Terminal:
    def __init__(self):
        self.current_user = None
        self.connection_status = False

    def run(self):
        self.healthcheck()
        self.user_interaction_loop()

    def user_interaction_loop(self):
        login_attempts = 3
        while not self.current_user and login_attempts > 0:
            action = input("Choose action: 'login' or 'register': ").lower()
            username = input("Please enter your credentials" "\nUsername: ")
            password = getpass("Password: ")  # Hide password input
            if action.lower() == "login":
                status, result = self.login(username, password)
                if status == 200:
                    print("Login successful:", result)
                else:
                    print("Login failed:", result)
            elif action.lower() == "register":
                self.register(username, password)
            else:
                print("Invalid action.")

        if not self.current_user:
            print("Failed to log in after several attempts.")
            return

        self.command_loop()

    def healthcheck(self):
        print("Checking if the API Gateway is running...")
        try:
            response = requests.get(f"{API_GATEWAY_URL}/ping")
            response.raise_for_status()  # Raise an exception for non-200 status codes
            if response.status_code == 200:
                self.connection_status = True
                print("API Gateway is running.")
            return self.connection_status
        except requests.exceptions.HTTPError as http_err:
            return f"HTTP Error occurred: {http_err}"
        except requests.exceptions.ConnectionError as conn_err:
            return f"Connection Error occurred: {conn_err}"
        except RequestException as req_err:
            return f"An unexpected error occurred while checking API Gateway: {req_err}"

    def login(self, user_info):
        try:
            response = requests.post(
                f"{API_GATEWAY_URL}/login",
                json={"username": user_info["username"], "password": user_info["password"]},
            )
            response.raise_for_status()

            # Extract the token from the response
            secret_key = response.json().get("token")
            role = response.json().get("role")
            if not secret_key or not role:
                return "Missing token or role in the response"
            self.current_user = User(user_info["username"], user_info["password"], role, secret_key)
            return self.current_user

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                return "Invalid credentials, please try again."
            else:
                return e.response.status_code, "HTTP Error occurred"
        except requests.exceptions.Timeout:
            return "Timeout error. Please try again later."
        except requests.exceptions.TooManyRedirects:
            return "Too many redirects. Please check the API gateway URL."
        except requests.exceptions.ConnectionError as e:
            return f"Connection error: {e}"
        except Exception as e:  # Catch-all for any other exceptions
            return f"An unexpected error occurred: {e}"

    def register(self, user_info):
        response = None
        try:
            response = requests.post(
                f"{API_GATEWAY_URL}/users/public",
                json={"username": user_info["username"], "password": user_info["password"], "role": "user"},
            )
            response.raise_for_status()  # Raise an exception for non-200 status codes
            if response.status_code == 201:
                print("Account created successfully.")
                return User(user_info["username"], user_info["password"], "user", "N/A")

        except requests.exceptions.HTTPError as err:
            if response.status_code == 400:
                return "Invalid request: Please check your inputs."
            else:
                return f"HTTP Error: {err}"
        except requests.exceptions.ConnectionError:
            return "Connection refused. Please check your network."
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    def command_loop(self):
        while True:
            print(
                f"Logged in as {self.current_user.role}. Type 'help' for available commands."
            )
            command = input("> ").lower()
            if command == "exit":
                break
            elif command == "help":
                self.show_help()
            else:
                self.handle_command(command)

    def show_help(self):
        # Show available commands based on role
        pass

    def handle_command(self, command):
        # Handle specific commands based on role and command
        pass
