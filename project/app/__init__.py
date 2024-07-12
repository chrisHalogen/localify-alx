from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize Flask extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    # Create a Flask application instance
    app = Flask(__name__)

    # Load configuration from the Config class
    app.config.from_object("config.Config")

    # Initialize extensions with the app instance
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        # Import User model here to avoid circular imports
        from .models import User

        # Create database tables for all models
        db.create_all()

        # Register blueprints for modularized routes
        from .accounts import accounts
        from .general import general
        from .seed_bp import seed_bp

        app.register_blueprint(accounts)
        app.register_blueprint(general)
        app.register_blueprint(seed_bp)

        # Set the login view for the login manager
        login_manager.login_view = "accounts.login"

        # User loader callback for Flask-Login
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(user_id)

    return app
