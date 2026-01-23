"""
Database connection and initialization
"""
import os
import time
import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager


class Database:
    """MySQL Database connection manager"""

    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", "3306"))
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "password")
        self.database = os.getenv("DB_NAME", "todo_db")

    @contextmanager
    def get_connection(self):
        """Get database connection as context manager"""
        connection = None
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                ssl_disabled=True,  # <--- FIX: Disable SSL for Keploy
                connection_timeout=10,  # 10 seconds timeout
                autocommit=False
            )
            yield connection
        except Error as e:
            print(f"Database connection error: {e}")
            raise
        finally:
            if connection and connection.is_connected():
                connection.close()

    def init_db(self, drop_if_exists=False):
        """Initialize database and create tables
        
        Args:
            drop_if_exists: If True, drop the table before creating it (useful for tests)
        """
        connection = None  # <--- FIX: Initialize variables safely
        cursor = None
        
        # Retry logic for Keploy proxy
        max_retries = 3
        retry_delay = 2  # seconds
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # First connect without database to create it
                connection = mysql.connector.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    ssl_disabled=True,  # <--- FIX: Disable SSL for Keploy
                    connection_timeout=10,  # 10 seconds timeout
                    autocommit=False
                )
                cursor = connection.cursor()

                # Create database if not exists
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
                cursor.execute(f"USE {self.database}")

                # Drop table if requested (for tests)
                if drop_if_exists:
                    cursor.execute("DROP TABLE IF EXISTS todos")
                
                # Create todos table
                create_table_query = """
                CREATE TABLE IF NOT EXISTS todos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    completed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
                """
                cursor.execute(create_table_query)
                connection.commit()
                print("Database initialized successfully")
                return  # Success, exit the retry loop
                
            except Error as e:
                last_error = e
                print(f"Error initializing database (attempt {attempt + 1}/{max_retries}): {e}")
                
                # Clean up connection before retry
                if cursor:
                    try:
                        cursor.close()
                    except:
                        pass
                if connection:
                    try:
                        if connection.is_connected():
                            connection.close()
                    except:
                        pass
                
                # If not the last attempt, wait before retrying
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    # Last attempt failed, raise the error
                    raise last_error
            finally:
                # Only clean up if we're not retrying (successful or final failure)
                if attempt == max_retries - 1 or 'return' in locals():
                    if cursor:
                        try:
                            cursor.close()
                        except:
                            pass
                    if connection:
                        try:
                            if connection.is_connected():
                                connection.close()
                        except:
                            pass


# Singleton instance
db = Database()