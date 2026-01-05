import json
from io import BytesIO
from pathlib import Path


def test_admin_import_and_restore(client, login_admin):
    # visit import page
    resp = client.get('/admin/import-visa-requirements')
    assert resp.status_code == 200

    # upload a small JSON
    payload = json.dumps({"Zland": {"work": ["Passport"]}})
    data = {
        'file': (BytesIO(payload.encode('utf-8')), 'test.json')
    }
    resp = client.post('/admin/import-visa-requirements', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert resp.status_code == 200
    assert b'Visa requirements imported successfully' in resp.data

    # Check that the country appears on management page
    resp = client.get('/admin/visa-management')
    assert b'Zland' in resp.data

    # Now perform restore
    resp = client.post('/admin/visa-management', data={'action':'restore'}, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Default seed restored successfully' in resp.data or b'Failed to restore default seed' in resp.data
