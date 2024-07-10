from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

# from .models import User

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        from .models import User

        db.create_all()

        from .accounts import accounts
        from .general import general
        from .seed_bp import seed_bp

        app.register_blueprint(accounts)
        app.register_blueprint(general)
        app.register_blueprint(seed_bp)

        login_manager.login_view = "accounts.login"

        @login_manager.user_loader
        def load_user(user_id):
            user = User.query.get(user_id)
            return user

    return app
