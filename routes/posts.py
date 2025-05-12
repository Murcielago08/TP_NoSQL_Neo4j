from flask import Blueprint, request, jsonify
from models import create_post, get_all_posts, get_post_likes, update_post, like_post, remove_like  # Import get_all_posts, get_post_likes, update_post, like_post, remove_like
from neo4j import GraphDatabase

posts_bp = Blueprint('posts', __name__)
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

@posts_bp.route('/users/<user_id>/posts', methods=['POST'])
def add_post(user_id):
    data = request.json
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Title and content are required"}), 400
    post = create_post(user_id, data['title'], data['content'])
    if post:
        return jsonify({"message": "Post created", "post": dict(post)}), 201
    return jsonify({"error": "User not found"}), 404

@posts_bp.route('/posts', methods=['GET'])
def get_posts():
    posts = get_all_posts()  # Fetch all posts
    return jsonify({"posts": [dict(post) for post in posts]})  # Return as JSON

@posts_bp.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    if not post_id:
        return jsonify({"error": "Post ID is required"}), 400
    with driver.session() as session:
        result = session.run("MATCH (p:Post {id: $post_id}) RETURN p", post_id=post_id)
        post = result.single()
        if post:
            post_data = post["p"]
            return jsonify({
                "id": post_data["id"],
                "title": post_data["title"],
                "content": post_data["content"],
                "created_at": post_data["created_at"]
            }), 200
        else:
            return jsonify({"error": "Post not found"}), 404

@posts_bp.route('/users/<user_id>/posts/<post_id>', methods=['DELETE'])
def delete_user_post(user_id, post_id):
    if not post_id or not user_id:
        return jsonify({"error": "User ID and Post ID are required"}), 400
    with driver.session() as session:
        result = session.run(
            "MATCH (u:User {id: $user_id})-[:CREATED]->(p:Post {id: $post_id}) DETACH DELETE p RETURN p",
            user_id=user_id, post_id=post_id
        )
        if result.consume().counters.nodes_deleted > 0:
            return jsonify({"message": "Post deleted"}), 200
        else:
            return jsonify({"error": "Post not found for this user"}), 404

@posts_bp.route('/users/<user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (u:User {id: $user_id})-[:CREATED]->(p:Post)
            RETURN p, u.name AS user_name
            """,
            user_id=user_id
        )
        posts = [{"id": record["p"]["id"], 
                  "title": record["p"]["title"], 
                  "content": record["p"]["content"], 
                  "created_at": record["p"]["created_at"], 
                  "user_name": record["user_name"]} for record in result]
        if posts:
            return jsonify({"posts": posts}), 200
        else:
            return jsonify({"error": "No posts found for this user"}), 404

@posts_bp.route('/users/<user_id>/posts/<post_id>', methods=['GET'])
def get_user_post(user_id, post_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (u:User {id: $user_id})-[:CREATED]->(p:Post {id: $post_id}) RETURN p",
            user_id=user_id, post_id=post_id
        )
        post = result.single()
        if post:
            post_data = post["p"]
            return jsonify({
                "id": post_data["id"],
                "title": post_data["title"],
                "content": post_data["content"],
                "created_at": post_data["created_at"]
            }), 200
        else:
            return jsonify({"error": "Post not found for this user"}), 404

@posts_bp.route('/posts/<post_id>/likes', methods=['GET'])
def get_post_likes_route(post_id):
    likes = get_post_likes(post_id)
    if likes is not None:
        return jsonify({"likes": likes}), 200
    return jsonify({"error": "Post not found"}), 404

@posts_bp.route('/posts/<post_id>', methods=['PUT'])
def update_post_route(post_id):
    data = request.json
    post = update_post(post_id, title=data.get("title"), content=data.get("content"))
    if post:
        return jsonify({"message": "Post updated", "post": {
            "id": post["id"],
            "title": post["title"],
            "content": post["content"],
            "created_at": post["created_at"]
        }}), 200
    return jsonify({"error": "Post not found"}), 404

@posts_bp.route('/posts/<post_id>/like', methods=['POST'])
def like_post_route(post_id):
    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({"error": "User ID is required"}), 400
    like = like_post(data['user_id'], post_id)
    if isinstance(like, dict) and "error" in like:
        return jsonify(like), 404
    return jsonify({"message": "Post liked"}), 201

@posts_bp.route('/posts/<post_id>/like', methods=['DELETE'])
def remove_like_post_route(post_id):
    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({"error": "User ID is required"}), 400
    user_id = data['user_id']
    with driver.session() as session:
        result = session.run(
            "MATCH (u:User {id: $user_id})-[r:LIKES]->(p:Post {id: $post_id}) DELETE r RETURN COUNT(r) AS deleted_count",
            user_id=user_id, post_id=post_id
        )
        deleted_count = result.single()["deleted_count"]
        if deleted_count > 0:
            return jsonify({"message": "Like removed"}), 200
        return jsonify({"error": "Like not found"}), 404

