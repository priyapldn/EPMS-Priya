import os

class Config:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    APP_DIR = os.path.join(BASEDIR, 'app')

    # Create instance folder if it doesn't exist
    instance_dir = os.path.join(APP_DIR, 'instance')
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(APP_DIR, 'instance', 'epmstore.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

    # Use the environment variable for SECRET_KEY, fallback to None if not set
    SECRET_KEY = os.getenv('SECRET_KEY')