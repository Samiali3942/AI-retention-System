from flask import Flask, render_template, url_for, request, jsonify, redirect, session
import os
import sys
from datetime import datetime
from database.init_db import init_database
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
import sqlite3


app = Flask(__name__)
app.secret_key = 'your-secret-key-for-testing'  # Change this in production

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)


def get_current_user():
    """Get current user information from session"""
    if 'logged_in' in session and session['logged_in']:
        return {
            'is_authenticated': True,
            'id': session.get('user_id'),
            'name': session.get('user_name'),
            'email': session.get('user_email'),
            'role': session.get('user_role', 'User'),
            'profile_image': session.get('profile_image', None)
        }
    return {'is_authenticated': False}

def get_db_connection():
    """Get database connection with proper error handling"""
    try:
        conn = sqlite3.connect('database/users.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

@app.context_processor
def inject_user():
    """Make current_user available in all templates"""
    return {'current_user': get_current_user()}

def init_user_tables(cursor):
    """Initialize only essential user tables if they don't exist"""
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                activity_type VARCHAR(50) NOT NULL,
                description TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Add more tables for dashboard features
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dashboard_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name VARCHAR(100) NOT NULL,
                metric_value REAL NOT NULL,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer_segments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                segment_name VARCHAR(100) NOT NULL,
                customer_count INTEGER DEFAULT 0,
                retention_rate REAL DEFAULT 0.0,
                avg_revenue REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id VARCHAR(50) NOT NULL,
                recommendation_type VARCHAR(100) NOT NULL,
                recommendation_text TEXT NOT NULL,
                confidence_score REAL DEFAULT 0.0,
                risk_score REAL DEFAULT 0.0,
                status VARCHAR(50) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.connection.commit()
        
    except Exception as e:
        print(f"Error initializing user tables: {e}")

# Decorator to require authentication
def login_required(f):
    """Decorator to require login for routes"""
    def decorated_function(*args, **kwargs):
        current_user = get_current_user()
        if not current_user['is_authenticated']:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/')
def index():
    """Main landing page route. Redirects to dashboard if authenticated, login if not."""
    current_user = get_current_user()
    
    if not current_user['is_authenticated']:
        return redirect(url_for('auth.login'))
    
    # Redirect authenticated users to dashboard
    return redirect(url_for('dashboard.dashboard_home'))

@app.route('/landing')
def landing():
    """Original landing page (kept for reference)"""
    return render_template('landing.html')

# Existing API endpoints
@app.route('/api/user/profile', methods=['GET'])
@login_required
def get_user_profile():
    """Get user profile data"""
    current_user = get_current_user()
    return jsonify({
        'success': True,
        'user': {
            'id': current_user['id'],
            'name': current_user['name'],
            'email': current_user['email'],
            'role': current_user['role']
        }
    })

@app.route('/api/user/profile', methods=['PUT'])
@login_required
def update_user_profile():
    """Update user profile"""
    try:
        data = request.get_json()
        current_user = get_current_user()
        
        # Basic validation
        name = data.get('name', '').strip()
        if not name:
            return jsonify({'success': False, 'message': 'Name is required'}), 400
        
        # Update session
        session['user_name'] = name
        
        return jsonify({
            'success': True, 
            'message': 'Profile updated successfully',
            'user': {
                'id': current_user['id'],
                'name': name,
                'email': current_user['email'],
                'role': current_user['role']
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to update profile'}), 500

@app.route('/api/dashboard/overview')
@login_required
def dashboard_overview():
    """API endpoint for dashboard overview data"""
    try:
        # Simulate dashboard overview data
        overview_data = {
            'total_customers': 15847,
            'active_segments': 12,
            'ai_recommendations': 247,
            'pending_issues': 23,
            'model_accuracy': 94.2,
            'retention_rate': 87.6,
            'monthly_growth': 12.4,
            'satisfaction_score': 4.3
        }
        
        return jsonify({
            'success': True,
            'data': overview_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'components': {
            'database': False
        }
    }
    
    # Check database
    try:
        conn = get_db_connection()
        if conn:
            conn.close()
            health_status['components']['database'] = True
    except:
        pass
    
    return jsonify(health_status)

# Error handlers (keeping existing ones)
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    try:
        return render_template('errors/404.html'), 404
    except:
        return "<h1>404 - Page Not Found</h1><p>The page you're looking for doesn't exist.</p>", 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    try:
        return render_template('errors/500.html'), 500
    except:
        return "<h1>500 - Internal Server Error</h1><p>Something went wrong. Please try again later.</p>", 500

@app.errorhandler(403)
def forbidden_error(error):
    """Handle 403 errors"""
    try:
        return render_template('errors/403.html'), 403
    except:
        return "<h1>403 - Access Denied</h1><p>You don't have permission to access this resource.</p>", 403

# Create necessary directories
def create_static_dirs():
    """Create static directories for CSS, JS files and templates"""
    directories = [
        'static/css',
        'static/js',
        'static/img',
        'templates',
        'templates/errors',
        'templates/features',
        'database',
        'routes'
    ]
    
    for directory in directories:
        dir_path = os.path.join(app.root_path, directory)
        os.makedirs(dir_path, exist_ok=True)

def initialize_dashboard_data():
    """Initialize sample dashboard data in database"""
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            
            # Initialize user tables
            init_user_tables(cursor)
            
            # Insert sample dashboard stats if not exists
            cursor.execute("SELECT COUNT(*) FROM dashboard_stats")
            if cursor.fetchone()[0] == 0:
                sample_stats = [
                    ('model_accuracy', 94.2),
                    ('active_customers', 15847),
                    ('retention_rate', 87.6),
                    ('avg_response_time', 2.3),
                    ('customer_satisfaction', 4.3)
                ]
                
                for metric_name, metric_value in sample_stats:
                    cursor.execute("""
                        INSERT INTO dashboard_stats (metric_name, metric_value)
                        VALUES (?, ?)
                    """, (metric_name, metric_value))
            
            # Insert sample customer segments if not exists
            cursor.execute("SELECT COUNT(*) FROM customer_segments")
            if cursor.fetchone()[0] == 0:
                sample_segments = [
                    ('High Value Loyalists', 2341, 96.7, 1250.0),
                    ('At-Risk Premium', 856, 73.2, 980.0),
                    ('New Adopters', 1847, 82.4, 420.0),
                    ('Occasional Users', 3245, 68.9, 180.0)
                ]
                
                for name, count, retention, revenue in sample_segments:
                    cursor.execute("""
                        INSERT INTO customer_segments 
                        (segment_name, customer_count, retention_rate, avg_revenue)
                        VALUES (?, ?, ?, ?)
                    """, (name, count, retention, revenue))
            
            # Insert sample AI recommendations if not exists
            cursor.execute("SELECT COUNT(*) FROM ai_recommendations")
            if cursor.fetchone()[0] == 0:
                sample_recommendations = [
                    ('CUST001', 'Churn Prevention', 'Immediate intervention required - offer personalized discount', 0.94, 0.87),
                    ('CUST002', 'Upselling', 'Engage with premium features promotion', 0.89, 0.72),
                    ('CUST003', 'Engagement', 'Send satisfaction survey and follow up', 0.81, 0.65),
                    ('CUST004', 'Retention', 'Provide loyalty rewards and benefits', 0.76, 0.58)
                ]
                
                for customer_id, rec_type, rec_text, confidence, risk in sample_recommendations:
                    cursor.execute("""
                        INSERT INTO ai_recommendations 
                        (customer_id, recommendation_type, recommendation_text, confidence_score, risk_score)
                        VALUES (?, ?, ?, ?, ?)
                    """, (customer_id, rec_type, rec_text, confidence, risk))
            
            conn.commit()
            conn.close()
            print("✓ Dashboard data initialized successfully")
            
    except Exception as e:
        print(f"✗ Error initializing dashboard data: {e}")

# Initialize application
def create_app():
    """Application factory function"""
    
    # Create necessary directories
    create_static_dirs()
    
    # Initialize database
    try:
        init_database()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
    
    # Initialize dashboard data
    initialize_dashboard_data()
    
    return app

if __name__ == '__main__':
    
    # Create the application
    app = create_app()
    
    print("=" * 70)
    print("🚀 RetentionAI Dashboard Server Starting...")
    print("=" * 70)
    print("🌐 Main URL: http://localhost:5000")
    print("🔐 Login URL: http://localhost:5000/login")
    print("📊 Dashboard URL: http://localhost:5000/dashboard")
    print("🧠 E-KYC URL: http://localhost:5000/ekyc")
    print("-" * 70)
    print("Demo Login Credentials:")
    print("  📧 Email: admin@example.com")
    print("  🔑 Password: password")
    print("-" * 70)
    print("Available Dashboard Features:")
    print("  🧠 AI Recommendations: /dashboard/ai-recommendations")
    print("  👥 Customer Segmentation: /dashboard/customer-segmentation") 
    print("  🛡️ E-KYC Issues: /dashboard/ekyc-issues")
    print("  💬 Feedback Support: /dashboard/feedback-support")
    print("  📄 Document Verification: /dashboard/document-verification")
    print("  💰 Maintenance Fee: /dashboard/maintenance-fee")
    print("-" * 70)
    print("🤖 KYC Churn Model Features:")
    print("  🔮 KYC Prediction: /api/kyc/predict")
    print("  📜 Prediction History: /api/kyc/history")
    print("  🌐 E-KYC Page: /ekyc")
    print("-" * 70)
    print("Database Info:")
    print("  📁 Type: SQLite")
    print("  📍 Location: ./database/users.db")
    print("  🔧 Auto-created: Yes")
    print("  📊 Sample Data: Loaded")
    print("-" * 70)
    print("Model Status:")
    if kyc_churn_model is not None:
        print("  🤖 KYC Churn Model: ✓ Loaded")
        print(f"  📁 Model File: {'✓' if os.path.exists('models/kyc_churn_model.pkl') else '✗'}")
    else:
        print("  🤖 KYC Churn Model: ✗ Not available")
        print("  💡 Place kyc_churn_model.pkl in models/ folder")
    print("=" * 70)
    
    # Start the development server
    app.run(debug=True, host='0.0.0.0', port=5000)