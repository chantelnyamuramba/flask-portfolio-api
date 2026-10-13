import pytest
from app import create_app, db

@pytest.fixture
def app():
    """Create and configure a clean Flask application instance for each test."""
    app = create_app('test')
    
    with app.app_context():
        db.create_all()  # Build temporary database tables in memory
        yield app
        db.session.remove()
        db.drop_all()    # Clean up tables after test completes

@pytest.fixture
def client(app):
    """A test client that can make simulated HTTP requests to your Flask API."""
    return app.test_client()