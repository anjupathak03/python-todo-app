"""
Flask Todo API Application
"""
from flask import Flask, request, jsonify
from models import Todo
from repository import todo_repository
from database import db

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


@app.route("/todos", methods=["GET"])
def get_todos():
    """Get all todos"""
    todos = todo_repository.get_all()
    return jsonify([todo.to_dict() for todo in todos]), 200


@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    """Get a specific todo"""
    todo = todo_repository.get_by_id(todo_id)
    if todo:
        return jsonify(todo.to_dict()), 200
    return jsonify({"error": "Todo not found"}), 404


@app.route("/todos", methods=["POST"])
def create_todo():
    """Create a new todo"""
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    todo = Todo(
        title=data["title"],
        description=data.get("description", ""),
        completed=data.get("completed", False),
    )

    created_todo = todo_repository.create(todo)
    if created_todo:
        return jsonify(created_todo.to_dict()), 201
    return jsonify({"error": "Failed to create todo"}), 500


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    """Update a todo"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    existing_todo = todo_repository.get_by_id(todo_id)
    if not existing_todo:
        return jsonify({"error": "Todo not found"}), 404

    todo = Todo(
        title=data.get("title", existing_todo.title),
        description=data.get("description", existing_todo.description),
        completed=data.get("completed", existing_todo.completed),
    )

    updated_todo = todo_repository.update(todo_id, todo)
    if updated_todo:
        return jsonify(updated_todo.to_dict()), 200
    return jsonify({"error": "Failed to update todo"}), 500


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    """Delete a todo"""
    success = todo_repository.delete(todo_id)
    if success:
        return jsonify({"message": "Todo deleted successfully"}), 200
    return jsonify({"error": "Todo not found"}), 404


if __name__ == "__main__":
    # Initialize database on startup
    db.init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
