import jwt
import os
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
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing or invalid"}), 403

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({"message": "Token is invalid"}), 403

        # Ajouter l'information de l'utilisateur à l'objet request
        g.user = data
        return f(*args, **kwargs)

    return decorated


@app.route('/login', methods=['POST'])
def login():
    # Obtenir les données de l'utilisateur
    username = request.json["username"]
    password = request.json["password"]

    # Appeler le service d'utilisateurs pour vérifier les identifiants
    response = requests.post(f"{USER_SERVICE_URL}/login", json={"username": username, "password": password})

    if response.ok:
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
        # Transmettre l'erreur du service d'utilisateurs
        return response.json(), response.status_code


@app.route('/books', methods=['GET'])
@token_required
def get_books():
    if g.user['role'] != 'admin':
        return jsonify({'message': 'Unauthorized'}), 401
    books = "N/A"
    response = requests.get(f"{BOOK_SERVICE_URL}/books")
    if response.status_code == 200:
        books = response.json()
    else:
        print(f"Erreur {response.status_code}: {response.text}")
    return books


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = "N/A"
    response = requests.delete(f"{BOOK_SERVICE_URL}/books/{book_id}")
    if response.status_code == 200:
        book = response.json()
    else:
        print(f"Erreur {response.status_code}: {response.text}")
    return book


@app.route('/books', methods=['POST'])
def post_books():
    title = request.json['title']
    author = request.json['author']
    book = "N/A"
    response = requests.post(f"{BOOK_SERVICE_URL}/books", json={"title": title, "author": author})
    if response.status_code == 200:
        book = response.json()
    else:
        print(f"Erreur {response.status_code}: {response.text}")
    return book


@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = "N/A"
    response = requests.put(f"{BOOK_SERVICE_URL}/books/{book_id}", json=request.json)
    if response.status_code == 200:
        book = response.json()
    else:
        print(f"Erreur {response.status_code}: {response.text}")
    return book


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
