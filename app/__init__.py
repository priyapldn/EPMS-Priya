import os
from flask import Flask
from app.database import init_engine
from config import Config

def create_app():
    app = Flask(__name__)

    # Load Config class
    app.config.from_object(Config)

    # Check instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialise database
    with app.app_context():
        init_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    # Initialise engine
    from app.database import Base, engine
    if engine is None:
        raise RuntimeError("Engine is not initialized")
    Base.metadata.create_all(engine)

    # Register app blueprint
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app