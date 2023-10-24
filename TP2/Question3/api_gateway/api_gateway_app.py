import jwt
import os
import re
import requests
from flask import Flask, request, jsonify, g
from functools import wraps

app = Flask(__name__)


BOOK_SERVICE_URL = "http://books-service:5000"
USER_SERVICE_URL = "http://users-service:5000"
REVIEW_SERVICE_URL = "http://reviews-service:5000"
TRANSACTION_SERVICE_URL = "http://transactions-service:5000"
SECRET_KEY = os.environ.get('SECRET_KEY')


def token_required(f):
    """
    Decorator that checks if a valid token is present in the request headers.
    
    :param f: The function to be decorated.
    :type f: function
    
    :return: The decorated function.
    :rtype: function
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"message": "Token is missing or invalid"}), 403
        try:
            token = re.match("^Bearer\s+(.*)", auth_header).group(1)
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token is expired"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is invalid"}), 403
        except Exception as e:
            return jsonify({"message": str(e)}), 403
        # Add the user object to the g object
        g.user = data
        return f(*args, **kwargs)
    return decorated


def role_required(role):
    """
    Decorator function that checks if the user has the required role.

    :param role: The required role that the user must have.
    :type role: str

    :return: A decorator function that can be used to wrap other functions.
    :rtype: function
    """
    def decorator(f):
        @wraps(f)
        @token_required
        def decorated_function(*args, **kwargs):
            if g.user.get('role') != role:
                return jsonify({'message': 'Unauthorized'}), 401
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint for user login.

    :return:
        - If the username or password is missing, returns a JSON response with a message and status code 400.
        - If the login is successful, returns a JSON response with a JWT token and status code 200.
        - If the login is not successful, returns a JSON response with the error message and the corresponding status code.
    """
    username = request.json["username"]
    password = request.json["password"]
    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400
    response = requests.post(f"{USER_SERVICE_URL}/login", json={"username": username, "password": password})
    if response.status_code == 200:
        user_data = response.json()
        token = jwt.encode(
            {
                'username': user_data['username'],
                'role': user_data['role']
            },
            SECRET_KEY,
            algorithm='HS256'
        )
        return jsonify({'token': token}), 200
    else:
        return jsonify(response.json()), response.status_code


@app.route('/books', methods=['GET'])
def get_books():
    """
    A function that retrieves a list of books from the book service API.
    
    :return:
        - If the response from the API is successful (status code 200), returns the list of books in JSON format.
        - If the response from the API is not successful, returns a JSON response and the corresponding status code.
    """
    response = requests.get(f"{BOOK_SERVICE_URL}/books")
    if response.status_code == 200:
        return response.json()
    else:
        return jsonify(response.json()), response.status_code


@app.route('/books/<int:book_id>', methods=['DELETE'])
@role_required('admin')
def delete_book(book_id):
    """
    Deletes a book with the given book ID.

    :param book_id: The ID of the book to be deleted.
    :type book_id: int

    :return: If the book is successfully deleted, the function returns a dictionary containing the response JSON. Otherwise, it returns a tuple containing the response JSON and the status code.
    :rtype: dict or tuple
    """
    response = requests.delete(f"{BOOK_SERVICE_URL}/books/{book_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return jsonify(response.json()), response.status_code


@app.route('/books', methods=['POST'])
@role_required('admin')
def post_books():
    """
    Sends a POST request to the '/books' endpoint to create a new book entry.

    :return:
        - If the request is successful (status code 200), returns the response JSON.
        - If the request is unsuccessful, returns the response JSON and the status code.
    """
    title = request.json['title']
    author = request.json['author']
    response = requests.post(f"{BOOK_SERVICE_URL}/books", json={"title": title, "author": author})
    if response.status_code == 200:
        return response.json()
    else:
        return jsonify(response.json()), response.status_code


@app.route('/books/<int:book_id>', methods=['PUT'])
@role_required('admin')
def update_book(book_id):
    """
    Updates a book with the given book ID.

    :param book_id: The ID of the book to be updated.
    :type book_id: int

    :return: If the book is updated successfully, returns the JSON response. Otherwise, returns a tuple containing the JSON response and the HTTP status code.
    :rtype: dict or tuple
    """
    response = requests.put(f"{BOOK_SERVICE_URL}/books/{book_id}", json=request.json)
    if response.status_code == 200:
        return response.json()
    else:
        return jsonify(response.json()), response.status_code


@app.route('/books/search', methods=['GET'])
def search_books():
    """
    Retrieves books based on search criteria.

    :return:
        If the search is successful, returns a JSON response containing the books found.
        If the search fails, returns a JSON response with an error message and the corresponding HTTP status code.
    """
    search_title = request.args.get('title')
    search_author = request.args.get('author')
    response = requests.get(f"{BOOK_SERVICE_URL}/books/search", params={"author": search_author, "title": search_title})
    if response.status_code == 200:
        return response.json()
    else:
        return jsonify(response.json()), response.status_code


@app.route('/users', methods=['GET'])
def gateway_get_users():
    """
    Send a GET request to the user service to retrieve a list of all users.

    :return: A JSON response containing the list of users and the corresponding HTTP status code.
    :rtype: dict
    """
    response = requests.get(f"{USER_SERVICE_URL}/users")
    return jsonify(response.json()), response.status_code


@app.route('/users/<int:user_id>', methods=['DELETE'])
@role_required('admin')
def gateway_delete_user(user_id):
    """
    A function that deletes a user from the gateway.

    :param user_id: The ID of the user to be deleted.
    :type user_id: int

    :return: A tuple containing the JSON response and the status code of the delete request.
    :rtype: tuple
    """
    response = requests.delete(f"{USER_SERVICE_URL}/users/{user_id}")
    return jsonify(response.json()), response.status_code


@app.route('/users', methods=['POST'])
@role_required('admin')
def gateway_post_user():
    """
    Sends a POST request to the '/users' endpoint of the gateway API with the provided JSON payload.

    :return: A tuple containing the JSON response and the HTTP status code of the POST request.
    :rtype: tuple
    """
    response = requests.post(f"{USER_SERVICE_URL}/users", json=request.json)
    return jsonify(response.json()), response.status_code


@app.route('/users/<int:user_id>', methods=['PUT'])
@role_required('admin')
def gateway_update_user(user_id):
    """
    Updates a user's information in the gateway.
    
    :param user_id: The ID of the user to be updated.
    :type user_id: int
    
    :return: A tuple containing the JSON response and the status code of the update request.
    :rtype: tuple
    """
    response = requests.put(f"{USER_SERVICE_URL}/users/{user_id}", json=request.json)
    return jsonify(response.json()), response.status_code


@app.route('/users/search', methods=['GET'])
def gateway_search_users():
    """
    Gateway function to search for users.
    
    This function is responsible for handling the HTTP GET request to search for users. It takes no parameters.
    
    :return: A JSON response containing the search results and the HTTP status code.
    :rtype: dict
    """
    search_user = request.args.get("username")
    response = requests.get(f"{USER_SERVICE_URL}/users/search", params={"username": search_user})
    return jsonify(response.json()), response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
