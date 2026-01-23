"""
Todo repository for database operations
"""
from typing import List, Optional
from mysql.connector import Error
from models import Todo
from database import db


class TodoRepository:
    """Repository for Todo CRUD operations"""

    def create(self, todo: Todo) -> Optional[Todo]:
        """Create a new todo"""
        try:
            with db.get_connection() as connection:
                cursor = connection.cursor()
                query = """
                INSERT INTO todos (title, description, completed)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query, (todo.title, todo.description, todo.completed))
                connection.commit()
                todo.id = cursor.lastrowid
                return self.get_by_id(todo.id)
        except Error as e:
            print(f"Error creating todo: {e}")
            return None

    def get_all(self) -> List[Todo]:
        """Get all todos"""
        try:
            with db.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM todos ORDER BY created_at DESC")
                rows = cursor.fetchall()
                return [
                    Todo(
                        id=row["id"],
                        title=row["title"],
                        description=row["description"],
                        completed=bool(row["completed"]),
                        created_at=row["created_at"],
                        updated_at=row["updated_at"],
                    )
                    for row in rows
                ]
        except Error as e:
            print(f"Error getting todos: {e}")
            return []

    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        """Get todo by ID"""
        try:
            with db.get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
                row = cursor.fetchone()
                if row:
                    return Todo(
                        id=row["id"],
                        title=row["title"],
                        description=row["description"],
                        completed=bool(row["completed"]),
                        created_at=row["created_at"],
                        updated_at=row["updated_at"],
                    )
                return None
        except Error as e:
            print(f"Error getting todo by id: {e}")
            return None

    def update(self, todo_id: int, todo: Todo) -> Optional[Todo]:
        """Update a todo"""
        try:
            with db.get_connection() as connection:
                cursor = connection.cursor()
                query = """
                UPDATE todos
                SET title = %s, description = %s, completed = %s
                WHERE id = %s
                """
                cursor.execute(
                    query, (todo.title, todo.description, todo.completed, todo_id)
                )
                connection.commit()
                if cursor.rowcount > 0:
                    return self.get_by_id(todo_id)
                return None
        except Error as e:
            print(f"Error updating todo: {e}")
            return None

    def delete(self, todo_id: int) -> bool:
        """Delete a todo"""
        try:
            with db.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
                connection.commit()
                return cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting todo: {e}")
            return False


# Singleton instance
todo_repository = TodoRepository()
