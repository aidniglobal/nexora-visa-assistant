from models import db, Inquiry


def test_inquiry_submission(client):
    # Ensure no inquiries exist
    with client.application.app_context():
        db.session.query(Inquiry).delete()
        db.session.commit()

    resp = client.post('/inquiry', data={'name':'Jane Doe','email':'jane@example.com','message':'I need help with visa'}, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Your inquiry has been received' in resp.data

    with client.application.app_context():
        saved = db.session.query(Inquiry).filter_by(email='jane@example.com').first()
        assert saved is not None
        assert saved.message == 'I need help with visa'
