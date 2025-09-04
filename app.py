from flask import Flask, render_template, url_for, request, jsonify, redirect, flash, session
import os
import joblib
import pandas as pd
from utils.csv_store import read_csv_safe, write_csv_safe
import numpy as np

app = Flask(__name__)
app.secret_key = 'your-secret-key-for-testing'

# Mock user class
class MockUser:
    def __init__(self, email=None, name=None):
        self.is_authenticated = email is not None
        self.name = name
        self.email = email
        self.avatar_url = None

# Initialize current_user as None (not authenticated)
current_user = MockUser()

@app.context_processor
def inject_user():
    """Make current_user available in all templates"""
    return {'current_user': current_user}

@app.route('/')
def index():
    """Main dashboard route"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    global current_user
    
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
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
        
        # Check demo credentials (you can add more users here)
        valid_credentials = {
            'admin@retentionai.com': {'password': 'admin123', 'name': 'Admin User'},
            'user@retentionai.com': {'password': 'user123', 'name': 'John Doe'},
            'demo@retentionai.com': {'password': 'demo123', 'name': 'Demo User'}
        }
        
        if email in valid_credentials and valid_credentials[email]['password'] == password:
            # Login successful
            user_info = valid_credentials[email]
            current_user = MockUser(email=email, name=user_info['name'])
            
            # Store login state in session
            session['logged_in'] = True
            session['user_email'] = email
            session['user_name'] = user_info['name']
            
            return jsonify({
                'success': True,
                'message': 'Login successful!',
                'redirect_url': url_for('index')
            })
        else:
            # Login failed
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401

@app.route('/logout')
def auth_logout():
    """Logout route"""
    global current_user
    
    # Clear session
    session.clear()
    
    # Reset current_user to unauthenticated state
    current_user = MockUser()
    
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

# Check session on each request to maintain login state
@app.before_request
def check_login_state():
    """Check if user is logged in based on session"""
    global current_user
    
    if 'logged_in' in session and session['logged_in']:
        if not current_user.is_authenticated:
            # Restore user from session
            current_user = MockUser(
                email=session.get('user_email'),
                name=session.get('user_name')
            )
    else:
        # Ensure user is not authenticated
        if current_user.is_authenticated:
            current_user = MockUser()

# Mock routes for navbar links (these prevent 404 errors)
@app.route('/data-upload')
def data_upload_index():
    """Data upload route"""
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return "<h1>Data Upload Page</h1><p>This is a placeholder for data upload functionality.</p>"

@app.route('/predictions/run')
def predictions_run_prediction():
    """Predictions route"""
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return "<h1>Run Prediction Page</h1><p>This is a placeholder for prediction functionality.</p>"

@app.route('/reports/generate')
def reports_generate():
    """Reports route"""
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return "<h1>Generate Report Page</h1><p>This is a placeholder for report generation.</p>"

@app.route('/customers')
def customers():
    """Customers route"""
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return "<h1>Customers Page</h1><p>This is a placeholder for customers page.</p>"

# --- ML pipelines and CSV config ---
# Paths
APP_DIR = os.path.dirname(__file__)
CHURN_PIPELINE_PATH = os.path.join(APP_DIR, 'models', 'pipelines', 'churn_pipeline.joblib')
SEGMENTATION_PIPELINE_PATH = os.path.join(APP_DIR, 'models', 'pipelines', 'segmentation_pipeline.joblib')
RAW_DATA_CSV = os.path.join(APP_DIR, 'data', 'raw', 'newone.csv')
PREDICTIONS_OUT_CSV = os.path.join(APP_DIR, 'data', 'processed', 'churn_predictions.csv')
SEGMENTATION_OUT_CSV = os.path.join(APP_DIR, 'data', 'processed', 'segmentation_results.csv')

# Lazy-loaded globals
_churn_pipeline = None
_segmentation_pipeline = None


def get_churn_pipeline():
    global _churn_pipeline
    if _churn_pipeline is None:
        if not os.path.exists(CHURN_PIPELINE_PATH):
            raise FileNotFoundError(f"Churn pipeline not found at {CHURN_PIPELINE_PATH}")
        _churn_pipeline = joblib.load(CHURN_PIPELINE_PATH)
    return _churn_pipeline


def get_segmentation_pipeline():
    global _segmentation_pipeline
    if _segmentation_pipeline is None:
        if not os.path.exists(SEGMENTATION_PIPELINE_PATH):
            raise FileNotFoundError(f"Segmentation pipeline not found at {SEGMENTATION_PIPELINE_PATH}")
        _segmentation_pipeline = joblib.load(SEGMENTATION_PIPELINE_PATH)
    return _segmentation_pipeline


def read_source_data() -> pd.DataFrame:
    df = read_csv_safe(RAW_DATA_CSV)
    if df.empty:
        raise FileNotFoundError(f"Source CSV empty or not found at {RAW_DATA_CSV}")
    return df


@app.route('/api/data/source', methods=['GET'])
def api_read_source():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        df = read_source_data()
        return jsonify({'columns': list(df.columns), 'rows': df.head(50).to_dict(orient='records')})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/predict/churn', methods=['POST'])
def api_predict_churn():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        df = read_source_data()
        pipeline = get_churn_pipeline()
        preds = pipeline.predict(df)
        proba = None
        if hasattr(pipeline, 'predict_proba'):
            try:
                proba = pipeline.predict_proba(df)[:, -1]
            except Exception:
                proba = None
        out_df = df.copy()
        out_df['churn_prediction'] = preds
        if proba is not None:
            out_df['churn_probability'] = proba
        write_csv_safe(out_df, PREDICTIONS_OUT_CSV, index=False)
        return jsonify({'success': True, 'output_csv': PREDICTIONS_OUT_CSV})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/predict/segment', methods=['POST'])
def api_predict_segment():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        df = read_source_data()
        pipeline = get_segmentation_pipeline()
        segments = pipeline.predict(df)
        out_df = df.copy()
        out_df['segment'] = segments
        write_csv_safe(out_df, SEGMENTATION_OUT_CSV, index=False)
        return jsonify({'success': True, 'output_csv': SEGMENTATION_OUT_CSV})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# API endpoints for navbar functionality
@app.route('/api/notifications/mark-read', methods=['POST'])
def mark_notifications_read():
    """Mark notifications as read"""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify({'success': True})

@app.route('/api/notifications/count')
def notifications_count():
    """Get notification count"""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify({'count': 3})

# Create static directories if they don't exist
def create_static_dirs():
    """Create static directories for CSS and JS files"""
    static_dir = os.path.join(app.root_path, 'static')
    css_dir = os.path.join(static_dir, 'css')
    js_dir = os.path.join(static_dir, 'js')
    
    os.makedirs(css_dir, exist_ok=True)
    os.makedirs(js_dir, exist_ok=True)

# ------ Customer Insights ------
@app.route('/insights')
def insights_page():
    return render_template('insights/index.html')


@app.route('/api/insights', methods=['GET'])
def insights_api():
    try:
        try:
            df = read_source_data()
        except FileNotFoundError as e:
            return jsonify({
                'shape': {'rows': 0, 'cols': 0},
                'columns': [],
                'numeric': {},
                'categorical': {},
                'extra': {},
                'notice': str(e)
            })
        summary = {}
        # Basic summary
        summary['shape'] = {'rows': int(df.shape[0]), 'cols': int(df.shape[1])}
        summary['columns'] = list(df.columns)

        # Numeric histograms (bin edges as labels, counts)
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        numeric = {}
        for col in numeric_cols[:6]:  # limit to 6 to keep UI tidy
            series = df[col].dropna()
            if series.empty:
                continue
            hist_counts, hist_bins = np.histogram(series, bins=10)
            labels = [f"{round(hist_bins[i],2)} - {round(hist_bins[i+1],2)}" for i in range(len(hist_bins)-1)]
            numeric[col] = {'labels': labels, 'counts': hist_counts.tolist()}
        summary['numeric'] = numeric

        # Categorical counts
        categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
        categorical = {}
        for col in categorical_cols[:6]:
            vc = df[col].astype('category').value_counts().head(12)
            categorical[col] = {'labels': vc.index.astype(str).tolist(), 'counts': vc.values.tolist()}
        summary['categorical'] = categorical

        # If predictions exist, attach churn/segment distributions
        extra = {}
        if 'churn_prediction' in df.columns:
            vc = df['churn_prediction'].value_counts()
            extra['churn_prediction'] = {'labels': vc.index.astype(str).tolist(), 'counts': vc.values.tolist()}
        if 'churn_probability' in df.columns:
            series = df['churn_probability'].dropna()
            if not series.empty:
                hist_counts, hist_bins = np.histogram(series, bins=10)
                labels = [f"{round(hist_bins[i],2)} - {round(hist_bins[i+1],2)}" for i in range(len(hist_bins)-1)]
                extra['churn_probability'] = {'labels': labels, 'counts': hist_counts.tolist()}
        if 'segment' in df.columns:
            vc = df['segment'].astype(str).value_counts()
            extra['segment'] = {'labels': vc.index.tolist(), 'counts': vc.values.tolist()}
        summary['extra'] = extra

        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    create_static_dirs()
    print("=" * 50)
    print("RetentionAI Development Server Starting...")
    print("=" * 50)
    print("Login Credentials:")
    print("  Email: admin@retentionai.com")
    print("  Password: admin123")
    print("=" * 50)
    print("  Email: user@retentionai.com") 
    print("  Password: user123")
    print("=" * 50)
    print("  Email: demo@retentionai.com")
    print("  Password: demo123")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)