from users_service import app, db
from users_service.models.user import User
from users_service.models.available_ids import AvailableIDs
from flask import jsonify, request


def get_min_available_id():
    auth_ids = db.session.query(User.id).all()
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
    min_id = get_min_available_id()
    user = User(id=min_id, username=username, title=password)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "user not found"}), 404
    user.title = request.json["username"]
    user.author = request.json["password"]
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
