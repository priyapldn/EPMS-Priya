import os


class Config:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    APP_DIR = os.path.join(BASEDIR, 'app')

    # This creates an instance folder if it doesn't exist
    instance_dir = os.path.join(APP_DIR, 'instance')
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(APP_DIR, 'instance', 'my_db.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')