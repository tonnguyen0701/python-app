# Database Connection
# MySQL database connection and configuration

import os
import mysql.connector
from mysql.connector import errorcode


class DatabaseConnection:
    """MySQL database connection management"""
    
    _connection = None
    
    DB_CONFIG = {
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", "712005"),
        "database": os.getenv("MYSQL_DATABASE", "thpt_grade_manager"),
        "charset": "utf8mb4",
        "use_unicode": True,
        "autocommit": True
    }
    
    def __init__(self):
        self._ensure_database_exists()
    
    @staticmethod
    def _ensure_database_exists():
        config = DatabaseConnection.DB_CONFIG.copy()
        database = config.pop("database")
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{database}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            conn.close()
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            raise
    
    @staticmethod
    def get_connection():
        """Get database connection (singleton)"""
        if DatabaseConnection._connection is None or not DatabaseConnection._connection.is_connected():
            DatabaseConnection._ensure_database_exists()
            DatabaseConnection._connection = mysql.connector.connect(**DatabaseConnection.DB_CONFIG)
        return DatabaseConnection._connection
    
    @staticmethod
    def close_connection():
        """Close database connection"""
        if DatabaseConnection._connection:
            DatabaseConnection._connection.close()
            DatabaseConnection._connection = None
    
    @staticmethod
    def execute_query(query, params=None):
        """Execute SQL query"""
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            try:
                conn.rollback()
            except:
                pass
            raise
