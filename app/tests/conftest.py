import pytest
from app import create_app

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # In-memory database for testing
        'WTF_CSRF_ENABLED': False,  # Disable CSRF for testing
    })

    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for click commands."""
    return app.test_cli_runner()
