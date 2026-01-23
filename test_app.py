"""
Pytest tests for the Todo API
These tests can be run with Keploy mocking to avoid real database calls
"""
import os
import pytest
from app import app
from database import db
from repository import todo_repository
from models import Todo

@pytest.fixture(scope="session")
def setup_database():
    """Initialize database once per test session"""
    # Drop and recreate the table once at the start of the test session
    db.init_db(drop_if_exists=True)
    yield
    # Final cleanup after all tests


@pytest.fixture
def client(setup_database):
    """Create a test client with database setup"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def init_database(setup_database):
    """Clean database before each test"""

    # Clean up all todos before each test
    try:
        with db.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM todos")
            connection.commit()
    except Exception as e:
        print(f"Pre-test cleanup error: {e}")
    yield
    # Clean up all todos after each test
    try:
        with db.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM todos")
            connection.commit()
    except Exception as e:
        print(f"Post-test cleanup error: {e}")


class TestHealthEndpoint:
    """Test health check endpoint"""

    def test_health_check(self, client):
        """Test health endpoint returns 200"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json["status"] == "healthy"


class TestTodoEndpoints:
    """Test Todo CRUD endpoints"""

    def test_create_todo_without_title(self, client):
        """Test creating todo without title fails"""
        todo_data = {"description": "Missing title"}
        response = client.post("/todos", json=todo_data)
        assert response.status_code == 400
        assert "error" in response.json

    # test_get_all_todos removed as requested

    def test_get_nonexistent_todo(self, client):
        """Test getting a non-existent todo returns 404"""
        response = client.get("/todos/99999")
        assert response.status_code == 404
        assert "error" in response.json

    def test_update_nonexistent_todo(self, client):
        """Test updating a non-existent todo returns 404"""
        response = client.put(
            "/todos/99999", json={"title": "Updated", "completed": True}
        )
        assert response.status_code == 404
        assert "error" in response.json

    def test_delete_nonexistent_todo(self, client):
        """Test deleting a non-existent todo returns 404"""
        response = client.delete("/todos/99999")
        assert response.status_code == 404
        assert "error" in response.json


class TestTodoModel:
    """Test Todo model"""

    def test_todo_to_dict(self):
        """Test converting todo to dictionary"""
        todo = Todo(
            id=1, title="Test", description="Test description", completed=False
        )
        todo_dict = todo.to_dict()
        assert todo_dict["id"] == 1
        assert todo_dict["title"] == "Test"
        assert todo_dict["description"] == "Test description"
        assert todo_dict["completed"] is False

    def test_todo_from_dict(self):
        """Test creating todo from dictionary"""
        data = {
            "id": 1,
            "title": "Test",
            "description": "Test description",
            "completed": True,
        }
        todo = Todo.from_dict(data)
        assert todo.id == 1
        assert todo.title == "Test"
        assert todo.description == "Test description"
        assert todo.completed is True
