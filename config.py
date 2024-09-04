import os


class Config:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASEDIR, 'instance', 'epmstore.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_USERNAME = os.getenv('DB_USERNAME', 'epm-user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'epmstore-pass-123')

    # Need to check this
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
