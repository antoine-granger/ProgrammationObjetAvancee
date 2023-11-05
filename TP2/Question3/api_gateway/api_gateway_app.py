import requests
from flask import Flask, request

app = Flask(__name__)


BOOK_SERVICE_URL = "http://books-service:5000/books"
ClIENT_SERVICE_URL = "http://clients-service:5000/clients"
REVIEW_SERVICE_URL = "http://reviews-service:5000/reviews"
TRANSACTION_SERVICE_URL = "http://transactions-service:5000/transactions"


@app.route('/books', methods=['GET'])
def get_books():
    books = "N/A"
    response = requests.get(f"{BOOK_SERVICE_URL}")
    if response.status_code == 200:
        books = response.json()
    else:
        print(f"Erreur {response.status_code}: {response.text}")
    return books


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = "N/A"
    response = requests.delete(f"{BOOK_SERVICE_URL}/{book_id}")
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
    response = requests.post(f"{BOOK_SERVICE_URL}", json={"title": title, "author": author})
    if response.status_code == 200:
        book = response.json()
    else:
        print(f"Erreur {response.status_code}: {response.text}")
    return book


@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = "N/A"
    response = requests.put(f"{BOOK_SERVICE_URL}/{book_id}", json=request.json)
    if response.status_code == 200:
        book = response.json()
    else:
        print(f"Erreur {response.status_code}: {response.text}")
    return book


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
