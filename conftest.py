"""
Configuration file for pytest
"""
import os

# Set test environment variables
os.environ["DB_HOST"] = os.getenv("DB_HOST", "localhost")
os.environ["DB_PORT"] = os.getenv("DB_PORT", "3306")
os.environ["DB_USER"] = os.getenv("DB_USER", "root")
os.environ["DB_PASSWORD"] = os.getenv("DB_PASSWORD", "password")
os.environ["DB_NAME"] = os.getenv("DB_NAME", "todo_db_test")
