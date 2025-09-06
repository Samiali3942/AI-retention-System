from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
import re
from models.database_models import User
from database.init_db import init_database

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password_strength(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, "Password is valid"

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    
    # If already logged in, redirect to dashboard
    if 'user_id' in session and session.get('logged_in'):
        return redirect(url_for('index'))
    
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        try:
            # Get JSON data from request
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'Invalid request data'
                }), 400
            
            email = data.get('email', '').strip()
            password = data.get('password', '')
            remember_me = data.get('remember_me', False)
            
            # Validate input
            if not email or not password:
                return jsonify({
                    'success': False,
                    'message': 'Email and password are required'
                }), 400
            
            # Check demo credentials first
            if email.lower() == 'admin@example.com' and password == 'password':
                session['user_id'] = 'demo'
                session['user_name'] = 'Demo Admin'
                session['user_email'] = email
                session['logged_in'] = True
                
                return jsonify({
                    'success': True,
                    'message': 'Login successful!',
                    'redirect_url': url_for('index')
                })
            
            # Try to authenticate with database
            user, message = User.authenticate(email, password)
            
            if user:
                # Login successful
                session['user_id'] = user.id
                session['user_name'] = user.name
                session['user_email'] = user.email
                session['logged_in'] = True
                
                return jsonify({
                    'success': True,
                    'message': message,
                    'redirect_url': url_for('index')
                })
            else:
                # Login failed
                return jsonify({
                    'success': False,
                    'message': message
                }), 401
                
        except Exception as e:
            print(f"Login error: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'An unexpected error occurred. Please try again.'
            }), 500

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """Signup route"""
    try:
        # Initialize database
        init_database()
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Invalid request data'
            }), 400
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')
        
        # Validation
        if not name:
            return jsonify({
                'success': False,
                'message': 'Please enter your full name'
            }), 400
            
        if not email:
            return jsonify({
                'success': False,
                'message': 'Please enter your email address'
            }), 400
        
        if not validate_email(email):
            return jsonify({
                'success': False,
                'message': 'Please enter a valid email address'
            }), 400
            
        if not password:
            return jsonify({
                'success': False,
                'message': 'Please enter a password'
            }), 400
        
        # Validate password strength
        is_valid, password_message = validate_password_strength(password)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': password_message
            }), 400
            
        if password != confirm_password:
            return jsonify({
                'success': False,
                'message': 'Passwords do not match'
            }), 400
        
        # Create user
        user, message = User.create_user(name, email, password)
        
        if user:
            return jsonify({
                'success': True,
                'message': 'Account created successfully! Please sign in.'
            })
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 400
            
    except Exception as e:
        print(f"Signup error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An unexpected error occurred. Please try again.'
        }), 500

@auth_bp.route('/logout')
def logout():
    """Logout route"""
    # Clear session
    session.clear()
    return redirect(url_for('auth.login'))