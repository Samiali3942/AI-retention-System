import sqlite3
import hashlib
from datetime import datetime
from database.init_db import get_connection

class User:
    def __init__(self, id=None, name=None, email=None, password_hash=None, 
                 created_at=None, last_login=None, is_active=True):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
        self.last_login = last_login
        self.is_active = is_active
    
    @staticmethod
    def hash_password(password):
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def create_user(name, email, password):
        """Create a new user in the database"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute('SELECT id FROM users WHERE email = ?', (email.lower(),))
            if cursor.fetchone():
                conn.close()
                return None, "User with this email already exists"
            
            # Hash password and insert user
            password_hash = User.hash_password(password)
            cursor.execute('''
                INSERT INTO users (name, email, password_hash, created_at)
                VALUES (?, ?, ?, ?)
            ''', (name, email.lower(), password_hash, datetime.now()))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Return the created user
            return User.get_by_id(user_id), "User created successfully"
            
        except sqlite3.Error as e:
            return None, f"Database error: {str(e)}"
        except Exception as e:
            return None, f"Error creating user: {str(e)}"
    
    @staticmethod
    def authenticate(email, password):
        """Authenticate a user with email and password"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            password_hash = User.hash_password(password)
            cursor.execute('''
                SELECT id, name, email, password_hash, created_at, last_login, is_active
                FROM users 
                WHERE email = ? AND password_hash = ? AND is_active = TRUE
            ''', (email.lower(), password_hash))
            
            user_data = cursor.fetchone()
            
            if user_data:
                # Update last login
                cursor.execute('''
                    UPDATE users SET last_login = ? WHERE id = ?
                ''', (datetime.now(), user_data[0]))
                conn.commit()
                
                # Create user object
                user = User(
                    id=user_data[0],
                    name=user_data[1],
                    email=user_data[2],
                    password_hash=user_data[3],
                    created_at=user_data[4],
                    last_login=datetime.now(),
                    is_active=user_data[6]
                )
                conn.close()
                return user, "Login successful"
            else:
                conn.close()
                return None, "Invalid email or password"
                
        except sqlite3.Error as e:
            return None, f"Database error: {str(e)}"
        except Exception as e:
            return None, f"Authentication error: {str(e)}"
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, email, password_hash, created_at, last_login, is_active
                FROM users WHERE id = ?
            ''', (user_id,))
            
            user_data = cursor.fetchone()
            conn.close()
            
            if user_data:
                return User(
                    id=user_data[0],
                    name=user_data[1],
                    email=user_data[2],
                    password_hash=user_data[3],
                    created_at=user_data[4],
                    last_login=user_data[5],
                    is_active=user_data[6]
                )
            return None
            
        except Exception as e:
            print(f"Error getting user by ID: {str(e)}")
            return None
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, email, password_hash, created_at, last_login, is_active
                FROM users WHERE email = ?
            ''', (email.lower(),))
            
            user_data = cursor.fetchone()
            conn.close()
            
            if user_data:
                return User(
                    id=user_data[0],
                    name=user_data[1],
                    email=user_data[2],
                    password_hash=user_data[3],
                    created_at=user_data[4],
                    last_login=user_data[5],
                    is_active=user_data[6]
                )
            return None
            
        except Exception as e:
            print(f"Error getting user by email: {str(e)}")
            return None