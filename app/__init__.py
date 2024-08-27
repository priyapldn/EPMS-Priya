from flask import Flask
from flask_sqlalchemy import SQLAlchemy

## db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    ## db.init_app(app)
    return app