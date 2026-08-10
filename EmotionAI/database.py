from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Initialize SQLAlchemy with Flask App context"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("[Database] SQLite database initialized successfully!")
