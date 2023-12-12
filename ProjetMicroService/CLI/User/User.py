class User:
    def __init__(self, username, password, role, secret_key):
        self.username = username
        self.password = password
        self.role = role
        self.secret_key = secret_key

    def display_info(self):
        return f"Username: {self.username}, Role: {self.role}"
