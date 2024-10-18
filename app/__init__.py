from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ProfessorSecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medicals.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)

    # Configure Flask-Login
    login_manager.login_view = 'auth.login'

    # Register blueprints
    from .auth import auth_bp
    from .dashboard import dashboard_bp
    from .patient import patients_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(patients_bp)

    # Import User model only after db is initialized
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
