from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import json
from datetime import datetime, timedelta
import random

# Create dashboard blueprint
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

def get_db_connection():
    """Get database connection with proper error handling"""
    try:
        conn = sqlite3.connect('database/users.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def login_required(f):
    """Decorator to require login for dashboard routes"""
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

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

# Dashboard route handlers
@dashboard_bp.route('/')
@login_required
def dashboard_home():
    """Main dashboard page"""
    current_user = get_current_user()
    
    # Get dashboard statistics
    stats = get_dashboard_stats()
    
    return render_template('dashboard.html', 
                         current_user=current_user,
                         stats=stats)

@dashboard_bp.route('/ai-recommendations')
@login_required
def ai_recommendations():
    """AI Recommendations feature page"""
    try:
        # Simulate AI recommendations data
        recommendations = generate_ai_recommendations()
        
        return render_template('Recommendation.html', 
                             recommendations=recommendations,
                             current_user=get_current_user())
    except Exception as e:
        print(f"Error loading AI recommendations: {e}")
        return render_template('errors/500.html'), 500

@dashboard_bp.route('/customer-segmentation')
@login_required
def customer_segmentation():
    """Customer Segmentation feature page"""
    try:
        # Simulate customer segmentation data
        segments = generate_customer_segments()
        
        return render_template('customer_segmentation.html', 
                             segments=segments,
                             current_user=get_current_user())
    except Exception as e:
        print(f"Error loading customer segmentation: {e}")
        return render_template('errors/500.html'), 500

@dashboard_bp.route('/ekyc-issues')
@login_required
def ekyc_issues():
    """E-KYC Issues feature page"""
    try:
        # Simulate E-KYC issues data
        issues = generate_ekyc_issues()
        
        return render_template('ekyc.html', 
                             issues=issues,
                             current_user=get_current_user())
    except Exception as e:
        print(f"Error loading E-KYC issues: {e}")
        return render_template('errors/500.html'), 500

@dashboard_bp.route('/feedback-support')
@login_required
def feedback_support():
    """Feedback Support feature page"""
    try:
        # Simulate feedback data
        feedback = generate_feedback_data()
        
        return render_template('customer_feedback.html', 
                             feedback=feedback,
                             current_user=get_current_user())
    except Exception as e:
        print(f"Error loading feedback support: {e}")
        return render_template('errors/500.html'), 500

@dashboard_bp.route('/document-verification')
@login_required
def document_verification():
    """Smart Document Verification feature page"""
    try:
        # Simulate document verification data
        documents = generate_document_data()
        
        return render_template('features/document_verification.html', 
                             documents=documents,
                             current_user=get_current_user())
    except Exception as e:
        print(f"Error loading document verification: {e}")
        return render_template('errors/500.html'), 500

@dashboard_bp.route('/maintenance-fee')
@login_required
def maintenance_fee():
    """Maintenance Fee feature page"""
    try:
        # Simulate maintenance fee data
        fees = generate_maintenance_fee_data()
        
        return render_template('maintenance_fee.html', 
                             fees=fees,
                             current_user=get_current_user())
    except Exception as e:
        print(f"Error loading maintenance fee: {e}")
        return render_template('errors/500.html'), 500

# API endpoints
@dashboard_bp.route('/api/stats')
@login_required
def api_dashboard_stats():
    """API endpoint for dashboard statistics"""
    try:
        stats = get_dashboard_stats()
        return jsonify({'success': True, 'data': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@dashboard_bp.route('/api/search', methods=['POST'])
@login_required
def api_search():
    """API endpoint for search functionality"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'success': False, 'error': 'Query is required'}), 400
        
        # Simulate search results
        results = perform_search(query)
        
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@dashboard_bp.route('/api/notifications')
@login_required
def api_notifications():
    """API endpoint for user notifications"""
    try:
        notifications = get_user_notifications()
        return jsonify({'success': True, 'data': notifications})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@dashboard_bp.route('/api/card-click', methods=['POST'])
@login_required
def api_card_click():
    """API endpoint to track card clicks"""
    try:
        data = request.get_json()
        card_type = data.get('card_type')
        user_id = session.get('user_id')
        
        # Log the card click
        log_card_click(user_id, card_type)
        
        return jsonify({'success': True, 'message': 'Click tracked'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@dashboard_bp.route('/api/implement-recommendation', methods=['POST'])
@login_required
def api_implement_recommendation():
    """API endpoint to implement AI recommendation"""
    try:
        data = request.get_json()
        recommendation_id = data.get('recommendation_id')
        user_id = session.get('user_id')
        
        # Log the implementation
        log_recommendation_implementation(user_id, recommendation_id)
        
        return jsonify({'success': True, 'message': 'Recommendation implemented successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Data generation functions (simulating ML model outputs)
def get_dashboard_stats():
    """Generate dashboard statistics"""
    return {
        'model_accuracy': 94.2,
        'active_customers': 15847,
        'retention_rate': 12.4,
        'avg_response_time': 2.3,
        'ai_recommendations_count': 247,
        'customer_segments': 12,
        'pending_ekyc_issues': 23,
        'recent_feedback': 156,
        'documents_processed': 89,
        'monthly_maintenance_fees': 1.2
    }

def generate_ai_recommendations():
    """Generate simulated AI recommendations"""
    recommendations = [
        {
            'id': 1,
            'customer_id': 'CUST001',
            'customer_name': 'John Smith',
            'risk_score': 0.87,
            'recommendation': 'Immediate intervention required - offer personalized discount',
            'confidence': 0.94,
            'category': 'Churn Prevention',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': 2,
            'customer_id': 'CUST002',
            'customer_name': 'Sarah Johnson',
            'risk_score': 0.72,
            'recommendation': 'Engage with premium features promotion',
            'confidence': 0.89,
            'category': 'Upselling',
            'created_at': (datetime.now() - timedelta(hours=2)).isoformat()
        },
        {
            'id': 3,
            'customer_id': 'CUST003',
            'customer_name': 'Mike Wilson',
            'risk_score': 0.65,
            'recommendation': 'Send satisfaction survey and follow up',
            'confidence': 0.81,
            'category': 'Engagement',
            'created_at': (datetime.now() - timedelta(hours=5)).isoformat()
        }
    ]
    return recommendations

def generate_customer_segments():
    """Generate simulated customer segments"""
    segments = [
        {
            'id': 1,
            'name': 'High Value Loyalists',
            'customer_count': 2341,
            'characteristics': ['High LTV', 'Low churn risk', 'Premium users'],
            'retention_rate': 96.7,
            'avg_revenue': 1250
        },
        {
            'id': 2,
            'name': 'At-Risk Premium',
            'customer_count': 856,
            'characteristics': ['Decreasing engagement', 'High value', 'Support tickets'],
            'retention_rate': 73.2,
            'avg_revenue': 980
        },
        {
            'id': 3,
            'name': 'New Adopters',
            'customer_count': 1847,
            'characteristics': ['Recent signup', 'Learning phase', 'High potential'],
            'retention_rate': 82.4,
            'avg_revenue': 420
        }
    ]
    return segments

def generate_ekyc_issues():
    """Generate simulated E-KYC issues"""
    issues = [
        {
            'id': 1,
            'customer_id': 'CUST004',
            'issue_type': 'Document Mismatch',
            'severity': 'High',
            'status': 'Pending Review',
            'created_at': datetime.now().isoformat(),
            'description': 'Address mismatch between submitted documents'
        },
        {
            'id': 2,
            'customer_id': 'CUST005',
            'issue_type': 'ID Verification Failed',
            'severity': 'Medium',
            'status': 'In Progress',
            'created_at': (datetime.now() - timedelta(days=1)).isoformat(),
            'description': 'Facial recognition match below threshold'
        }
    ]
    return issues

def generate_feedback_data():
    """Generate simulated feedback data"""
    feedback = [
        {
            'id': 1,
            'customer_id': 'CUST006',
            'rating': 4.5,
            'sentiment': 'Positive',
            'comment': 'Great service, but response time could be improved',
            'category': 'Support',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': 2,
            'customer_id': 'CUST007',
            'rating': 2.0,
            'sentiment': 'Negative',
            'comment': 'Very disappointed with recent changes',
            'category': 'Product',
            'created_at': (datetime.now() - timedelta(hours=3)).isoformat()
        }
    ]
    return feedback

def generate_document_data():
    """Generate simulated document verification data"""
    documents = [
        {
            'id': 1,
            'customer_id': 'CUST008',
            'document_type': 'Passport',
            'verification_status': 'Verified',
            'confidence_score': 0.97,
            'processed_at': datetime.now().isoformat()
        },
        {
            'id': 2,
            'customer_id': 'CUST009',
            'document_type': 'Driver License',
            'verification_status': 'Under Review',
            'confidence_score': 0.72,
            'processed_at': (datetime.now() - timedelta(minutes=30)).isoformat()
        }
    ]
    return documents

def generate_maintenance_fee_data():
    """Generate simulated maintenance fee data"""
    fees = [
        {
            'month': 'September 2025',
            'total_collected': 1200000,
            'pending_amount': 45000,
            'customers_paid': 8947,
            'customers_pending': 234,
            'collection_rate': 97.8
        },
        {
            'month': 'August 2025',
            'total_collected': 1180000,
            'pending_amount': 12000,
            'customers_paid': 8956,
            'customers_pending': 87,
            'collection_rate': 99.1
        }
    ]
    return fees

def perform_search(query):
    """Simulate search functionality"""
    # This would typically query your database or search engine
    mock_results = [
        {
            'type': 'Customer',
            'id': 'CUST001',
            'name': f'Customer matching "{query}"',
            'relevance': 0.95
        },
        {
            'type': 'Document',
            'id': 'DOC001',
            'name': f'Document containing "{query}"',
            'relevance': 0.87
        }
    ]
    return mock_results

def get_user_notifications():
    """Get user notifications"""
    notifications = [
        {
            'id': 1,
            'type': 'alert',
            'title': 'High Risk Customer Alert',
            'message': '89 customers identified as high churn risk',
            'created_at': (datetime.now() - timedelta(minutes=5)).isoformat(),
            'read': False
        },
        {
            'id': 2,
            'type': 'success',
            'title': 'Model Update Complete',
            'message': 'AI recommendation model updated successfully',
            'created_at': (datetime.now() - timedelta(hours=1)).isoformat(),
            'read': False
        },
        {
            'id': 3,
            'type': 'info',
            'title': 'System Maintenance',
            'message': 'Scheduled maintenance tonight at 2:00 AM',
            'created_at': (datetime.now() - timedelta(hours=3)).isoformat(),
            'read': True
        }
    ]
    return notifications

def log_card_click(user_id, card_type):
    """Log card click for analytics"""
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_activities (user_id, activity_type, description, created_at)
                VALUES (?, 'card_click', ?, ?)
            """, (user_id, f"Clicked on {card_type} card", datetime.now().isoformat()))
            conn.commit()
            conn.close()
    except Exception as e:
        print(f"Error logging card click: {e}")

def log_recommendation_implementation(user_id, recommendation_id):
    """Log recommendation implementation"""
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_activities (user_id, activity_type, description, created_at)
                VALUES (?, 'recommendation_implementation', ?, ?)
            """, (user_id, f"Implemented recommendation {recommendation_id}", datetime.now().isoformat()))
            conn.commit()
            conn.close()
    except Exception as e:
        print(f"Error logging recommendation implementation: {e}")

# Error handlers for dashboard blueprint
@dashboard_bp.errorhandler(404)
def dashboard_not_found(error):
    """Handle 404 errors in dashboard"""
    return render_template('errors/404.html', 
                         message="Dashboard page not found"), 404

@dashboard_bp.errorhandler(500)
def dashboard_internal_error(error):
    """Handle 500 errors in dashboard"""
    return render_template('errors/500.html', 
                         message="Dashboard error occurred"), 500