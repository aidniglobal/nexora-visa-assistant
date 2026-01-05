import pytest
from app import app as flask_app
from models import db, User
import tempfile


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use a temporary DB
    db_file = tmp_path / 'test.db'
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file}'
    flask_app.config['TESTING'] = True

    # Initialize DB
    with flask_app.app_context():
        db.init_app(flask_app)
        db.create_all()
        # create an admin user
        admin = User(name='Admin', email='admin@example.com')
        admin.set_password('password')
        admin.is_admin = True
        db.session.add(admin)
        db.session.commit()

    with flask_app.test_client() as client:
        yield client


@pytest.fixture
def login_admin(client):
    # log in as admin using post to /login
    resp = client.post('/login', data={'email':'admin@example.com','password':'password'}, follow_redirects=True)
    assert resp.status_code in (200, 302)
    return client