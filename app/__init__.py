from datetime import date
from flask import Flask
from flask_login import LoginManager
from app.database import add_employee, add_review, get_session, init_engine
from app.models import Employee
from config import Config

class AppFactory:
    def __init__(self):
        self.app = None
        self.session = None
        self.login_manager = LoginManager()

    def create_app(self):
        """Set up and return the Flask app."""
        self.app = Flask(__name__)
        self._configure_app()
        self._init_database()
        self._login_manager()
        self._populate_database()

        # Register app blueprint
        self._register_blueprints()

        return self.app

    def _configure_app(self):
        """Load configuration for the Flask app."""
        self.app.config.from_object(Config)

    def _login_manager(self):

        self.session = get_session()

        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(self.app)

        from .models import Employee
        @login_manager.user_loader
        def load_user(employee_number):
            return self.session.query(Employee).get(employee_number)

    def _init_database(self):
        """Initialize the database within the Flask app context."""
        with self.app.app_context():
            init_engine(self.app.config['SQLALCHEMY_DATABASE_URI'])
        
        from app.database import Base, engine
        if engine is None:
            raise RuntimeError("Engine is not initialized")
        Base.metadata.create_all(engine)

        self.session = get_session()

    def _populate_database(self):
        """Populate the database with initial data if the tables are empty."""
        # Add an employee
        add_employee(self.session, 'John Doe', 101, 'johndoe1234', 'john.doe@example.com', 'Password123!', is_admin=False)

        # Add a review for that employee (assuming employee_number 101 exists)
        add_review(self.session, 101, date(2024, 9, 4), 202, 'Excellent', 
                   'My main goal is to take part in leadership opportunities in the next term.',
                   'John has shown great progress in his career goals.')

    def _register_blueprints(self):
        """Register the app's blueprints."""
        from app.routes import main as main_blueprint
        self.app.register_blueprint(main_blueprint)

        from app.auth import auth as auth_blueprint
        self.app.register_blueprint(auth_blueprint)


# Function to be called during flask run
def create_app():
    """Factory function to create the app instance."""
    factory = AppFactory()
    return factory.create_app()