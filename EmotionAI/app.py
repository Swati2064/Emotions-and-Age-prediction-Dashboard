import os
import uuid
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename

from config import Config
from database import db, init_db
from models import User, DetectionHistory

from ai_models.face_detector import detect_faces, annotate_and_save_image
from ai_models.emotion import detect_emotion
from ai_models.age_detection import detect_age
from music.recommendation import get_recommendations

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Database
init_db(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access the AI dashboard.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# =========================================================================
# PAGE ROUTES
# =========================================================================

@app.route('/')
def index():
    """Landing Page"""
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User Registration"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validations
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('signup.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('signup.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('signup.html')

        # Check existing user
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            flash('Email or Username is already registered.', 'danger')
            return render_template('signup.html')

        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User Login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            session.permanent = True
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password credentials.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    """User Logout"""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Main AI Dashboard Page"""
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=user)


# =========================================================================
# REST API ENDPOINTS
# =========================================================================

@app.route('/api/analyze', methods=['POST'])
@login_required
def analyze_image():
    """
    AI Image Processing API
    Detects faces, predicts age & emotion, draws bounding box, and saves prediction history.
    """
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image file uploaded in request.'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected image file.'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Invalid file format. Please upload JPG or PNG.'}), 400

    try:
        # Generate unique filenames
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        unique_id = uuid.uuid4().hex[:10]
        raw_filename = f"raw_{unique_id}.{file_ext}"
        annotated_filename = f"annotated_{unique_id}.{file_ext}"

        raw_filepath = os.path.join(app.config['UPLOAD_FOLDER'], raw_filename)
        annotated_filepath = os.path.join(app.config['UPLOAD_FOLDER'], annotated_filename)

        # Save raw uploaded image
        file.save(raw_filepath)

        # 1. AI Face Detection
        faces, face_count, shape = detect_faces(raw_filepath)
        face_detected = (face_count > 0)

        # 2. AI Emotion Detection
        emotion, confidence, emotion_scores = detect_emotion(raw_filepath)

        # 3. AI Age Prediction
        age = detect_age(raw_filepath, faces)

        # 4. Draw HUD Bounding Boxes & Annotate Image
        annotate_and_save_image(raw_filepath, faces, age, emotion, confidence, annotated_filepath)

        # 5. Save Record to Database
        history_item = DetectionHistory(
            user_id=session['user_id'],
            original_filename=raw_filename,
            annotated_filename=annotated_filename,
            face_detected=face_detected,
            faces_count=face_count,
            age=age,
            emotion=emotion,
            confidence=confidence
        )
        db.session.add(history_item)
        db.session.commit()

        # 6. Fetch Emotion-Based Music Recommendations
        recommendations = get_recommendations(emotion)

        return jsonify({
            'success': True,
            'results': history_item.to_dict(),
            'recommendations': recommendations
        })

    except Exception as e:
        print(f"[API Error] Image analysis error: {e}")
        return jsonify({'success': False, 'error': f'AI Model Execution Error: {str(e)}'}), 500


@app.route('/api/history', methods=['GET'])
@login_required
def get_history():
    """Fetch user's past detection logs"""
    try:
        user_id = session['user_id']
        history_records = DetectionHistory.query.filter_by(user_id=user_id).order_by(DetectionHistory.created_at.desc()).all()
        return jsonify({
            'success': True,
            'history': [item.to_dict() for item in history_records]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/history/<int:history_id>', methods=['DELETE'])
@login_required
def delete_history(history_id):
    """Delete single history record"""
    try:
        record = DetectionHistory.query.filter_by(id=history_id, user_id=session['user_id']).first()
        if not record:
            return jsonify({'success': False, 'error': 'History entry not found.'}), 404

        # Clean up files from static/uploads if existing
        for fn in [record.original_filename, record.annotated_filename]:
            fp = os.path.join(app.config['UPLOAD_FOLDER'], fn)
            if os.path.exists(fp):
                try:
                    os.remove(fp)
                except OSError:
                    pass

        db.session.delete(record)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Record deleted successfully.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("  Starting EmotionAI Dashboard Server...")
    print("  Local URL: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
