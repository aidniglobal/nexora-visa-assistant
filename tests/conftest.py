import sys
import os
import pytest

# Ensure repo root is on sys.path so tests can import 'app' and 'scripts'
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import create_app
# Create a fresh app instance for the test suite and allow overriding DB URI when needed
flask_app = create_app()
from models import db, User


@pytest.fixture
def client(tmp_path):
    # Create a fresh app with a temporary DB before initializing SQLAlchemy
    db_file = tmp_path / 'test.db'
    test_config = {
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_file}',
        'TESTING': True,
    }
    app = create_app(test_config=test_config)

    with app.app_context():
        db.drop_all()
        db.create_all()
        # create an admin user
        admin = User(name='Admin', email='admin@example.com')
        admin.set_password('password')
        admin.is_admin = True
        db.session.add(admin)
        db.session.commit()

    with app.test_client() as client:
        yield client


@pytest.fixture
def login_admin(client):
    # Bypass login endpoint and set session directly for tests
    from models import db, User
    with client.application.app_context():
        admin = db.session.query(User).filter_by(email='admin@example.com').first()
        assert admin is not None
    with client.session_transaction() as sess:
        sess['_user_id'] = str(admin.id)
    return client