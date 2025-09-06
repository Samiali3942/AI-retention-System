import sqlite3
import os
from datetime import datetime

def get_db_path():
    """Get the path to the database file"""
    # Create database directory if it doesn't exist
    db_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(db_dir, 'retention_app.db')

def init_database():
    """Initialize the database and create tables"""
    db_path = get_db_path()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP NULL,
            is_active BOOLEAN DEFAULT TRUE
        )
    ''')
    
    # Create index on email for faster lookups
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)
    ''')
    
    # Create user sessions table (optional, for better session management)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print(f"Database initialized at: {db_path}")

def get_connection():
    """Get database connection"""
    return sqlite3.connect(get_db_path())

if __name__ == '__main__':
    init_database()