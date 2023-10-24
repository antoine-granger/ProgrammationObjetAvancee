from users_service import app, db
from users_service.models.user import User
from users_service.models.available_ids import AvailableIDs
from flask import jsonify, request
from werkzeug.security import check_password_hash


def get_min_available_id():
    """
    Generates the smallest available ID that can be used for a new book.
    This function queries the database to retrieve all existing book IDs,
    creates a set of all possible IDs from 1 to the maximum existing ID + 1,
    and returns the smallest ID that is not currently in use.

    :return:
        int: The smallest available ID for a new book. If no IDs are available,
        the function returns the maximum existing ID + 1.
    """
    user_ids = db.session.query(User.id).all()
    user_ids = [user_id[0] for user_id in user_ids]
    if not user_ids:
        return 1
    # Find the minimum available ID
    all_ids = set(range(1, max(user_ids) + 1))
    available_ids = all_ids - set(user_ids)
    # Return the minimum available ID
    return min(available_ids) if available_ids else max(user_ids) + 1


def remove_available_id(used_id):
    """
    Remove the used ID from the AvailableIDs table.

    :param used_id: int: The ID to be removed from the AvailableIDs table.
    :type used_id: int
    """
    AvailableIDs.query.filter_by(id=used_id).delete()
    db.session.commit()


@app.route("/login", methods=["POST"])
def login():
    """
    Handle the login request.

    This function is responsible for handling the "/login" POST request. It retrieves the username and password from the
     request's JSON body. If either the username or password is missing, it returns a JSON response with a 400 status
     code and a message indicating the missing field.

    After retrieving the username and password, it queries the database to find a user with the given username.
    If a user is found and the provided password matches the hashed password stored in the database, it returns a JSON
    response with the user's username and role, along with a 200 status code.

    If either no user is found or the provided password does not match the hashed password, it returns a JSON response
    with a 401 status code and a message indicating an invalid username or password.

    :return:A JSON response containing either the user's information and a 200 status code, or an error message and the
            appropriate status code.
    :rtype: dict
    """
    username = request.json["username"]
    password = request.json["password"]
    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return jsonify({"username": user.username, "role": user.role}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


@app.route("/users", methods=["GET"])
def get_users():
    """
    Retrieve all users from the database.
 
    :return: A JSON response containing a list of serialized user objects.
    :rtype: tuple
    """
    users = User.query.order_by(User.id).all()
    return jsonify([user.serialize() for user in users]), 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Deletes a user from the database.

    :param user_id: The ID of the user to be deleted.
    :type user_id: int

    :return: A JSON response containing a message and a status code.
    :rtype: tuple
    """
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    remove_available_id(user_id)
    return jsonify({"message": "User deleted successfully"}), 200


@app.route("/users", methods=["POST"])
def post_user():
    """
    Handles the POST request to create a new user.

    :return: A JSON response containing the serialized user object and a status code.
    :rtype: tuple
    """
    username = request.json["username"]
    password = request.json["password"]
    role = request.json["role"].lower()
    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400
    if role not in ["admin", "user"]:
        return jsonify({"message": "Invalid role, must be 'admin' or 'user"}), 400
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
    """
    Update a user with the given user_id.
    
    :param user_id: The ID of the user to update.
    :type user_id: int
    
    :return: A JSON response containing the updated user's information and a status code.
    :rtype: tuple
    """
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "user not found"}), 404
    user.username = request.json["username"]
    user.set_password(request.json["password"])
    user.role = request.json["role"].lower()
    if not user.username or not user.password:
        return jsonify({"message": "Missing username or password"}), 400
    if user.role not in ["admin", "user"]:
        return jsonify({"message": "Invalid role, must be 'admin' or 'user"}), 400
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "user updated successfully"}), 200


@app.route("/users/search", methods=["GET"])
def search_users():
    """
    Searches for users based on a given username.

    :return: A JSON response containing a list of serialized user objects.
    :rtype: tuple
    """
    search_user = request.args.get("username")
    query = User.query
    if search_user:
        query = query.filter(User.username.ilike(f"%{search_user}%"))
    users = query.all()
    users_data = [user.serialize() for user in users]
    if not users:
        return jsonify(404, {"message": "No users found"})
    return jsonify(users_data), 200
