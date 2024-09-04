from flask import current_app
from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

# Set engine and session for DB
engine = None
Session = sessionmaker()

# Initialises engine through creation of tables
def init_engine(database_uri):
    global engine
    engine = create_engine(database_uri, echo=True)
    Base.metadata.create_all(engine)

# Retrieve session to utilise operations
def get_session():
    if engine is None:
        raise RuntimeError("Engine is not initialized")
    return Session(bind=engine)