from transactions_service import app, db
from transactions_service.models.transaction import Transaction
from transactions_service.models.available_ids import AvailableIDs
from flask import jsonify, request


def get_min_available_id():
    auth_ids = db.session.query(Transaction.id).all()
    auth_ids = [auth_id[0] for auth_id in auth_ids]
    if not auth_ids:
        return 1
    # Trouver le plus petit ID non utilisé
    # Pour cela, on crée une série d'IDs à partir de 1 jusqu'au maximum ID utilisé + 1
    all_ids = set(range(1, max(auth_ids) + 1))
    available_ids = all_ids - set(auth_ids)

    # Retourner le plus petit ID disponible
    return min(available_ids) if available_ids else max(auth_ids) + 1


def remove_available_id(used_id):
    AvailableIDs.query.filter_by(id=used_id).delete()
    db.session.commit()


# Add new transaction in the database
@app.route("/transactions", methods=["POST"])
def post_transaction():
    min_id = get_min_available_id()
    user = request.json["user"]
    book = request.json["book"]
    category = request.json["category"]
    value = request.json["value"]
    transaction = Transaction(id=min_id, user=request.json["user"], book=request.json["book"],category=category, value=value)
    db.session.add(transaction)
    db.session.commit()
    return


# Remove transaction from the database
@app.route("/transactions/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    transaction_id = Transaction.query.get(transaction_id)
    if transaction_id is None:
        return jsonify({"message": "Transaction not found"}), 404
    db.session.delete(transaction_id)
    db.session.commit()
    remove_available_id(transaction_id)
    return jsonify({"message": "Transaction deleted successfully"}), 200


# Update transaction in the database
@app.route("/transactions/<int:transaction_id>", methods=["PUT"])
def update_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if transaction is None:
        return jsonify({"message": "Transaction not found"}), 404
    transaction.user = request.json["user"]
    transaction.book = request.json["book"]
    transaction.category = request.json["category"]
    transaction.value = request.json["value"]
    db.session.commit()
    return jsonify({"message": "Transaction updated successfully"}), 200


# Get transactions from database
@app.route("/transactions", methods=["GET"])
def get_transactions():
    transactions = Transaction.query.order_by(Transaction.id).all()
    return jsonify([transaction.serialize() for transaction in transactions]), 200


# Get transaction for single user in the database
@app.route("/transactions/user/<int:user_id>", methods=["GET"])
def get_transactions_for_user(user_id):
    transactions = Transaction.query.filter_by(user=user_id).all()
    if transactions is None:
        return jsonify({"message": "Transaction not found"}), 404
    return jsonify([transaction.serialize() for transaction in transactions]), 200


# Get transaction from single book in the database
@app.route("/transactions/book/<int:book_id>", methods=["GET"])
def get_transactions_for_book(book_id):
    transactions = Transaction.query.filter_by(book=book_id).all()
    if transactions is None:
        return jsonify({"message": "Transaction not found"}), 404
    return jsonify([transaction.serialize() for transaction in transactions]), 200


# Get transaction from single category in the database
@app.route("/transactions/category/<string:category>", methods=["GET"])
def get_transactions_for_category(category):
    transactions = Transaction.query.filter_by(category=category).all()
    if transactions is None:
        return jsonify({"message": "Transaction not found"}), 404
    return jsonify([transaction.serialize() for transaction in transactions]), 200
