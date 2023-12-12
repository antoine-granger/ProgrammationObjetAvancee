API_GATEWAY_URL = "http://localhost:5000"


def display_error(response):
    print(response.json()["message"])
