from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to history
    history = db.relationship('DetectionHistory', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class DetectionHistory(db.Model):
    __tablename__ = 'detection_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    annotated_filename = db.Column(db.String(255), nullable=False)
    face_detected = db.Column(db.Boolean, default=True)
    faces_count = db.Column(db.Integer, default=1)
    age = db.Column(db.Integer, nullable=False)
    emotion = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'original_filename': self.original_filename,
            'annotated_filename': self.annotated_filename,
            'original_url': f'/static/uploads/{self.original_filename}',
            'annotated_url': f'/static/uploads/{self.annotated_filename}',
            'face_detected': 'YES' if self.face_detected else 'NO',
            'faces_count': self.faces_count,
            'age': self.age,
            'emotion': self.emotion.capitalize(),
            'confidence': round(self.confidence, 1),
            'created_at': self.created_at.strftime('%b %d, %Y - %I:%M %p')
        }
