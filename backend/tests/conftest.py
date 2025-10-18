# tests/conftest.py
import pytest
from app import create_app, db

@pytest.fixture(scope='module')
def test_app():
    """Create and configure a new app instance for each test module."""
    app = create_app('testing')
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def test_client(test_app):
    """A test client for the app."""
    return test_app.test_client()

@pytest.fixture(scope='function')
def init_database(test_app):
    """Create and drop the database for each test function."""
    with test_app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()