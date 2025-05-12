from flask import Blueprint, request, jsonify
from models import create_user, get_all_users, update_user, get_user_friends, add_friend, remove_friend, are_friends, get_mutual_friends  # Import get_all_users, update_user, get_user_friends, add_friend, remove_friend, are_friends, get_mutual_friends
from neo4j import GraphDatabase

users_bp = Blueprint('users', __name__)
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

@users_bp.route('/users', methods=['POST'])
def add_user():
    data = request.json
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Invalid input"}), 400
    user = create_user(data['name'], data['email'])
    return jsonify({"message": "User created", "user": dict(user)}), 201

@users_bp.route('/users', methods=['GET'])
def get_users():
    users = get_all_users()
    return jsonify({"users": [dict(user) for user in users]}), 200

@users_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    with driver.session() as session:
        result = session.run("MATCH (u:User {id: $user_id}) RETURN u", user_id=user_id)
        user = result.single()
        if user:
            user_data = user["u"]
            return jsonify({
                "id": user_data["id"],
                "name": user_data["name"],
                "email": user_data["email"],
                "created_at": user_data["created_at"]
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404

@users_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    with driver.session() as session:
        result = session.run("MATCH (u:User {id: $user_id}) DETACH DELETE u RETURN u", user_id=user_id)
        if result.consume().counters.nodes_deleted > 0:
            return jsonify({"message": "User deleted"}), 200
        else:
            return jsonify({"error": "User not found"}), 404

@users_bp.route('/users/<user_id>', methods=['PUT'])
def update_user_route(user_id):
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    user = update_user(user_id, name=data.get('name'), email=data.get('email'))
    if user:
        return jsonify({"message": "User updated", "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "created_at": user["created_at"]
        }}), 200
    return jsonify({"error": "User not found"}), 404

@users_bp.route('/users/<user_id>/friends', methods=['GET'])
def get_user_friends_route(user_id):
    friends = get_user_friends(user_id)
    if friends is not None:
        return jsonify({"friends": friends}), 200
    return jsonify({"error": "User not found"}), 404

@users_bp.route('/users/<user_id>/friends', methods=['POST'])
def add_friend_route(user_id):
    data = request.json
    if not data or 'friend_id' not in data or not data['friend_id']:
        return jsonify({"error": "Friend ID is required"}), 400
    friendship = add_friend(user_id, data['friend_id'])
    if isinstance(friendship, dict) and "error" in friendship:
        return jsonify(friendship), 404
    return jsonify({"message": "Friend added"}), 201

@users_bp.route('/users/<user_id>/friends/<friend_id>', methods=['DELETE'])
def remove_friend_route(user_id, friend_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (u:User {id: $user_id})-[r:FRIENDS_WITH]-(f:User {id: $friend_id}) DELETE r RETURN COUNT(r) AS deleted_count",
            user_id=user_id, friend_id=friend_id
        )
        deleted_count = result.single()["deleted_count"]
        if deleted_count > 0:
            return jsonify({"message": "Friend removed"}), 200
        return jsonify({"error": "Friendship not found"}), 404

@users_bp.route('/users/<user_id>/friends/<friend_id>', methods=['GET'])
def are_friends_route(user_id, friend_id):
    are_friends_result = are_friends(user_id, friend_id)
    return jsonify({"are_friends": are_friends_result}), 200

@users_bp.route('/users/<user_id>/mutual-friends/<other_id>', methods=['GET'])
def get_mutual_friends_route(user_id, other_id):
    mutual_friends = get_mutual_friends(user_id, other_id)
    return jsonify({"mutual_friends": mutual_friends}), 200
