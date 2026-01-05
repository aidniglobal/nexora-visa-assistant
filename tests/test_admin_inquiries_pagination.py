from models import db, Inquiry


def test_admin_inquiries_pagination(client, login_admin):
    with client.application.app_context():
        db.session.query(Inquiry).delete()
        for i in range(12):
            db.session.add(Inquiry(name=f'User{i}', email=f'u{i}@ex.com', message='Hi'))
        db.session.commit()

    # page 1 should contain 5 items
    resp = client.get('/admin/inquiries?page=1')
    assert resp.status_code == 200
    assert b'User0' in resp.data
    # page 3 should exist (12 items, 5 per page -> 3 pages)
    resp = client.get('/admin/inquiries?page=3')
    assert resp.status_code == 200
    assert b'User10' in resp.data or b'User11' in resp.data