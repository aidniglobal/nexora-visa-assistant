import json
from models import db, Inquiry, User


def test_admin_can_view_and_respond(client, login_admin):
    # create one sample inquiry
    with client.application.app_context():
        db.session.query(Inquiry).delete()
        db.session.commit()
        inq = Inquiry(name='Sam', email='sam@example.com', message='Help me')
        db.session.add(inq)
        db.session.commit()
        inq_id = inq.id

    # admin visits the list
    resp = client.get('/admin/inquiries')
    assert resp.status_code == 200
    assert b'Sam' in resp.data

    # admin opens respond page
    resp = client.get(f'/admin/inquiries/respond/{inq_id}')
    assert resp.status_code == 200
    assert b'Help me' in resp.data

    # admin posts a response
    resp = client.post(f'/admin/inquiries/respond/{inq_id}', data={'response':'We can help'}, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Response saved and sent' in resp.data

    with client.application.app_context():
        refreshed = db.session.get(Inquiry, inq_id)
        assert refreshed.response == 'We can help'