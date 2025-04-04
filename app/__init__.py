from datetime import date
from flask import Flask, request, abort, redirect, url_for
from flask_login import LoginManager
from flask_talisman import Talisman
from flask_wtf import CSRFProtect
from werkzeug.security import generate_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix

from app.auth import AuthHandler
from app.database import add_employee, add_review, get_session, init_engine
from app.models import Employee
from config import Config


class AppFactory:
    def __init__(self):
        self.app = None
        self.session = None
        self.csrf = CSRFProtect()
        self.login_manager = LoginManager()
        self.auth_handler = None

    def create_app(self, config=None):
        """Set up and return the Flask app"""
        self.app = Flask(__name__)

        # Apply proxy fix if the app is behind a reverse proxy
        self.app.wsgi_app = ProxyFix(self.app.wsgi_app, x_for=1)

        # Call all functions of AppFactory
        self._configure_app(config)
        self.csrf.init_app(self.app)
        self._init_database()
        self._init_auth_handler()
        self._login_manager()
        self._populate_database()

        # Register app blueprints
        self._register_blueprints()

        # Apply security measures
        self._apply_security()

        return self.app

    def _configure_app(self, config):
        """Load configuration"""
        self.app.config.from_object(Config)

        if config:
            self.app.config.update(config)

    def _login_manager(self):
        """Initialize the login manager"""
        self.login_manager.login_view = "auth.login"
        self.login_manager.init_app(self.app)

        # Retrieve current user
        @self.login_manager.user_loader
        def load_user(employee_number):
            return self.session.query(Employee).get(employee_number)

    def _init_database(self):
        """Initialize the database within the app context."""
        # Use app config for database URI
        with self.app.app_context():
            init_engine(self.app.config["SQLALCHEMY_DATABASE_URI"])

        from app.database import Base, engine

        if engine is None:
            raise RuntimeError("Engine is not initialized")

        Base.metadata.create_all(engine)
        self.session = get_session()

    def _init_auth_handler(self):
        """Initialize the AuthHandler with the session"""
        self.auth_handler = AuthHandler(self.session)

    def _populate_database(self):
        """Populate the database with initial data if the tables are empty"""
        # Add admin
        add_employee(
            self.session,
            "John Doe",
            101,
            "johndoe1234",
            "john.doe@example.com",
            password=generate_password_hash("Password123!"),
            is_admin=True,
        )

        # Add a review for that employee (assuming employee_number 101 exists)
        add_review(
            self.session,
            101,
            date(2024, 9, 4),
            202,
            "Excellent",
            "My main goal is to take part in leadership opportunities in the next term.",
            "John has shown great progress in his career goals.",
        )

    def _register_blueprints(self):
        """Register blueprints"""
        from app.routes import main as main_blueprint

        self.app.register_blueprint(main_blueprint)

        self.app.register_blueprint(self.auth_handler.auth_bp)

    def _apply_security(self):
        """Apply security measures like blocking TRACE, TRACK, OPTIONS methods and removing sensitive headers"""

        # Block TRACE, TRACK, and OPTIONS methods
        @self.app.before_request
        def block_trace_track_options():
            if request.method in ["TRACE", "TRACK", "OPTIONS"]:
                # Method Not Allowed
                abort(405)

        # Remove sensitive headers like X-Powered-By and Server
        @self.app.after_request
        def remove_sensitive_headers(response):
            response.headers["Server"] = "EPMS_Server"
            response.headers.pop("X-Powered-By", None)
            return response

        # Standard error message for 404
        @self.app.errorhandler(404)
        def page_not_found(e):
            return (
                "404 Not Found: The resource you are looking for could not be found.",
                404,
            )

        # Standard error message for 500
        @self.app.errorhandler(500)
        def internal_server_error(e):
            return (
                "500 Internal Server Error: Something went wrong on our end. Please try again later.",
                500,
            )


# Targeted on flask run
def create_app(config=None):
    """Factory function to create the app instance"""
    factory = AppFactory()
    return factory.create_app(config)
