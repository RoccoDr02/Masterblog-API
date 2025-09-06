from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()


    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    if "title" not in data:
        return jsonify({"error": "title is required"}), 400
    if "content" not in data:
        return jsonify({"error": "content is required"}), 400

    new_id = max([post["id"] for post in POSTS], default=0) + 1
    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"]
    }

    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post_to_delete = next((post for post in POSTS if post["id"] == id), None)
    if not post_to_delete:
        return jsonify({"error": "Post not found"}), 404

    POSTS.remove(post_to_delete)
    return jsonify({"message": f"Post with id {id} has been deleted successfully"}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
