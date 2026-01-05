from models import db, Inquiry


def test_admin_quick_reply_and_close(client, login_admin):
    with client.application.app_context():
        db.session.query(Inquiry).delete()
        db.session.commit()
        inq = Inquiry(name='Q', email='q@example.com', message='Help')
        db.session.add(inq)
        db.session.commit()
        inq_id = inq.id

    # quick reply
    resp = client.post(f'/admin/inquiries/quick_reply/{inq_id}', follow_redirects=True)
    assert resp.status_code == 200

    with client.application.app_context():
        refreshed = db.session.get(Inquiry, inq_id)
        assert refreshed.response is not None
        assert refreshed.status == 'responded'

    # close
    resp = client.post(f'/admin/inquiries/close/{inq_id}', follow_redirects=True)
    assert resp.status_code == 200
    with client.application.app_context():
        refreshed = db.session.get(Inquiry, inq_id)
        assert refreshed.status == 'closed'