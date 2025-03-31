from flask import Flask, request, jsonify
from models import create_user, create_post, create_comment

app = Flask(__name__)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    user = create_user(data['name'], data['email'])
    return jsonify({"message": "User created", "user": dict(user)}), 201

@app.route('/users/<user_id>/posts', methods=['POST'])
def add_post(user_id):
    data = request.json
    post = create_post(user_id, data['title'], data['content'])
    if post:
        return jsonify({"message": "Post created", "post": dict(post)}), 201
    return jsonify({"error": "User not found"}), 404

@app.route('/posts/<post_id>/comments', methods=['POST'])
def add_comment(post_id):
    data = request.json
    comment = create_comment(data['user_id'], post_id, data['content'])
    if comment:
        return jsonify({"message": "Comment added", "comment": dict(comment)}), 201
    return jsonify({"error": "User or Post not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
