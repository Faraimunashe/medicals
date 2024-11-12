from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ProfessorSecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medical.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'faraimunashe.m11@gmail.com'
    app.config['MAIL_PASSWORD'] = 'vdpdwbzmbhflivoc'
    app.config['MAIL_DEFAULT_SENDER'] = 'faraimunashe.m11@gmail.com'


    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    

    # Configure Flask-Login
    login_manager.login_view = 'auth.login'

    # Register blueprints
    from .auth import auth_bp
    from .dashboard import dashboard_bp
    from .patient import patients_bp
    from .medical import medicals_bp
    from .appointment import appointments_bp
    from .user import users_bp
    from .report import report_bp
    from .audit import audits_bp
    from .plan import plan_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(medicals_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(audits_bp)
    app.register_blueprint(plan_bp)

    # Import User model only after db is initialized
    from app.models import User, AuditLog

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()
        

    return app
