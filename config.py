import os


class Config:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    APP_DIR = os.path.join(BASEDIR, 'app')

    # Create instance folder if it doesn't exist
    instance_dir = os.path.join(APP_DIR, 'instance')
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(APP_DIR, 'instance', 'epmstore.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

    SECRET_KEY = os.getenv('SECRET_KEY', 'a9e3c5383ad2c41293d572afe33d844f1ae4f3248a842524e572abdf62034823')