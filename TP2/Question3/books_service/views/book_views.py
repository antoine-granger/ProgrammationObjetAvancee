from books_service import app, db
from books_service.models.available_ids import AvailableIDs
from books_service.models.book import Book
from flask import jsonify, request


def get_min_available_id():
    book_ids = db.session.query(Book.id).all()
    book_ids = [book_id[0] for book_id in book_ids]
    if not book_ids:
        return 1
    # Trouver le plus petit ID non utilisé
    # Pour cela, on crée une série d'IDs à partir de 1 jusqu'au maximum ID utilisé + 1
    all_ids = set(range(1, max(book_ids) + 1))
    available_ids = all_ids - set(book_ids)

    # Retourner le plus petit ID disponible
    return min(available_ids) if available_ids else max(book_ids) + 1


def remove_available_id(used_id):
    AvailableIDs.query.filter_by(id=used_id).delete()
    db.session.commit()


@app.route("/books", methods=["GET"])
def get_books():
    """
    Get a list of all books.

    :return: A JSON response containing the serialized data of all books.
    """
    books = Book.query.order_by(Book.id).all()
    return jsonify([book.serialize() for book in books]), 200


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    """
    Delete a book from the database based on its ID.

    :param book_id: int: The ID of the book to be deleted.

    Returns:
        dict: A JSON response indicating the success of the deletion.
            - message (str): A message indicating the success of the deletion.
    """
    # Recherche du livre par son ID
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({"message": "Book not found"}), 404
    db.session.delete(book)
    db.session.commit()
    remove_available_id(book_id)
    return jsonify({"message": "Book deleted successfully"}), 200


@app.route("/books", methods=["POST"])
def post_books():
    """
    Create a new book and add it to the database.

    :return: A JSON response containing the serialized book object.
    """
    title = request.json["title"]
    author = request.json["author"]
    min_id = get_min_available_id()
    book = Book(id=min_id, title=title, author=author)
    db.session.add(book)
    db.session.commit()
    return jsonify(book.serialize()), 201


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    """
    Update a book in the database based on its ID.

    :param book_id: int: The ID of the book to be updated.

    Returns:
        dict: A JSON response indicating the success of the update.
            - message (str): A message indicating the success of the update.
    """
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({"message": "Book not found"}), 404
    book.title = request.json["title"]
    book.author = request.json["author"]

    db.session.commit()

    return jsonify({"message": "Book updated successfully"}), 200


@app.route("/books/search", methods=["GET"])
def search_books():
    """
    Search for books based on title or author.

    :return: A JSON response containing the serialized data of the found books.
    """
    search_title = request.args.get("title")
    search_author = request.args.get("author")

    query = Book.query
    if search_title:
        query = query.filter(Book.title.ilike(f"%{search_title}%"))
    if search_author:
        query = query.filter(Book.author.ilike(f"%{search_author}%"))

    books = query.all()
    books_data = [book.serialize() for book in books]
    if not books:
        return jsonify(404, {"message": "No books found"})
    return jsonify(books_data), 200
