from users_service import app, db
from users_service.models.user import User
from users_service.models.available_ids import AvailableIDs
from flask import jsonify, request
from werkzeug.security import check_password_hash


def get_min_available_id():
    user_ids = db.session.query(User.id).all()
    user_ids = [user_id[0] for user_id in user_ids]
    if not user_ids:
        return 1
    # Trouver le plus petit ID non utilisé
    # Pour cela, on crée une série d'IDs à partir de 1 jusqu'au maximum ID utilisé + 1
    all_ids = set(range(1, max(user_ids) + 1))
    available_ids = all_ids - set(user_ids)

    # Retourner le plus petit ID disponible
    return min(available_ids) if available_ids else max(user_ids) + 1


def remove_available_id(used_id):
    AvailableIDs.query.filter_by(id=used_id).delete()
    db.session.commit()


@app.route("/login", methods=["POST"])
def login():
    # Obtenir les données d'authentification
    username = request.json["username"]
    password = request.json["password"]

    # Rechercher l'utilisateur dans la DB
    user = User.query.filter_by(username=username).first()

    # Vérifier le mot de passe
    if user and check_password_hash(user.password_hash, password):
        # Retourner les données utilisateur nécessaires pour le token
        return jsonify({"username": user.username, "role": user.role}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.order_by(User.id).all()
    return jsonify([user.serialize() for user in users]), 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    remove_available_id(user_id)
    return jsonify({"message": "User deleted successfully"}), 200


@app.route("/users", methods=["POST"])
def post_user():
    username = request.json["username"]
    password = request.json["password"]
    role = request.json["role"]
    # Check if the username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        # If a user with this username already exists, return a conflict response
        return jsonify({"message": "Username already taken"}), 409
    min_id = get_min_available_id()
    user = User(id=min_id, username=username, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "user not found"}), 404
    user.username = request.json["username"]
    user.set_password(request.json["password"])
    user.role = request.json["role"]
    db.session.commit()
    return jsonify({"message": "user updated successfully"}), 200


@app.route("/users/search", methods=["GET"])
def search_users():
    search_user = request.args.get("username")
    query = User.query
    if search_user:
        query = query.filter(User.username.ilike(f"%{search_user}%"))
    users = query.all()
    users_data = [user.serialize() for user in users]
    if not users:
        return jsonify(404, {"message": "No users found"})
    return jsonify(users_data), 200
