from flask import Blueprint, request, jsonify
from models import create_comment, get_all_comments, get_comment_likes, update_comment, like_comment, remove_like  # Import get_all_comments, get_comment_likes, update_comment, like_comment, remove_like
from neo4j import GraphDatabase

comments_bp = Blueprint('comments', __name__)
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

@comments_bp.route('/posts/<post_id>/comments', methods=['POST'])
def add_comment(post_id):
    data = request.json
    comment = create_comment(data['user_id'], post_id, data['content'])
    if comment:
        return jsonify({"message": "Comment added", "comment": dict(comment)}), 201
    return jsonify({"error": "User or Post not found"}), 404

@comments_bp.route('/comments', methods=['GET'])
def get_comments():
    comments = get_all_comments()  # Fetch all comments
    return jsonify({"comments": [dict(comment) for comment in comments]})  # Return as JSON

@comments_bp.route('/comments/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    if not comment_id:
        return jsonify({"error": "Comment ID is required"}), 400
    with driver.session() as session:
        result = session.run("MATCH (c:Comment {id: $comment_id}) RETURN c", comment_id=comment_id)
        comment = result.single()
        if comment:
            comment_data = comment["c"]
            return jsonify({
                "id": comment_data["id"],
                "content": comment_data["content"],
                "created_at": comment_data["created_at"]
            }), 200
        else:
            return jsonify({"error": "Comment not found"}), 404

@comments_bp.route('/comments/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    if not comment_id:
        return jsonify({"error": "Comment ID is required"}), 400
    with driver.session() as session:
        result = session.run("MATCH (c:Comment {id: $comment_id}) DETACH DELETE c RETURN c", comment_id=comment_id)
        if result.consume().counters.nodes_deleted > 0:
            return jsonify({"message": "Comment deleted"}), 200
        else:
            return jsonify({"error": "Comment not found"}), 404

@comments_bp.route('/comments/<comment_id>/likes', methods=['GET'])
def get_comment_likes_route(comment_id):
    likes = get_comment_likes(comment_id)
    if likes is not None:
        return jsonify({"likes": likes}), 200
    return jsonify({"error": "Comment not found"}), 404

@comments_bp.route('/comments/<comment_id>', methods=['PUT'])
def update_comment_route(comment_id):
    data = request.json
    comment = update_comment(comment_id, content=data.get("content"))
    if comment:
        return jsonify({"message": "Comment updated", "comment": {
            "id": comment["id"],
            "content": comment["content"],
            "created_at": comment["created_at"]
        }}), 200
    return jsonify({"error": "Comment not found"}), 404

@comments_bp.route('/comments/<comment_id>/like', methods=['POST'])
def like_comment_route(comment_id):
    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({"error": "User ID is required"}), 400
    like = like_comment(data['user_id'], comment_id)
    if like:
        return jsonify({"message": "Comment liked"}), 201
    return jsonify({"error": "User or Comment not found"}), 404

@comments_bp.route('/comments/<comment_id>/like', methods=['DELETE'])
def remove_like_comment_route(comment_id):
    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({"error": "User ID is required"}), 400
    success = remove_like(data['user_id'], comment_id, "Comment")
    if success:
        return jsonify({"message": "Like removed"}), 200
    return jsonify({"error": "Like not found"}), 404

@comments_bp.route('/posts/<post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    with driver.session() as session:
        result = session.run("MATCH (p:Post {id: $post_id})-[:HAS_COMMENT]->(c:Comment) RETURN c", post_id=post_id)
        comments = [record["c"] for record in result]
        if comments:
            return jsonify({"comments": [
                {
                    "id": comment["id"],
                    "content": comment["content"],
                    "created_at": comment["created_at"]
                } for comment in comments
            ]}), 200
        else:
            return jsonify({"error": "No comments found for this post"}), 404

@comments_bp.route('/posts/<post_id>/comments/<comment_id>', methods=['DELETE'])
def delete_post_comment(post_id, comment_id):
    with driver.session() as session:
        result = session.run(
            "MATCH (p:Post {id: $post_id})-[:HAS_COMMENT]->(c:Comment {id: $comment_id}) DETACH DELETE c RETURN c",
            post_id=post_id, comment_id=comment_id
        )
        if result.consume().counters.nodes_deleted > 0:
            return jsonify({"message": "Comment deleted"}), 200
        else:
            return jsonify({"error": "Comment not found for this post"}), 404
