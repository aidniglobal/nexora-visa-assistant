import json
from io import BytesIO


def test_seed_write_and_reload(client, login_admin, tmp_path, monkeypatch):
    """Integration-style test: ensure admin import writes to VISA_REQUIREMENTS.SEED_PATH
    and that reload_seed() picks up the new data."""
    import app.visa_requirements as vr

    # Point the module to temp seed files
    seed_file = tmp_path / "visa_seed.json"
    default_file = tmp_path / "visa_seed_default.json"
    monkeypatch.setattr(vr, "SEED_PATH", str(seed_file))
    monkeypatch.setattr(vr, "DEFAULT_SEED_PATH", str(default_file))

    # Ensure no seed exists beforehand
    if seed_file.exists():
        seed_file.unlink()

    payload = json.dumps({"Zland": {"work": ["Passport"]}})
    data = {"file": (BytesIO(payload.encode("utf-8")), "test.json")}    

    # Perform the admin import via the web UI
    resp = client.post('/admin/import-visa-requirements', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert resp.status_code == 200
    assert 'Visa requirements imported successfully' in resp.data.decode('utf-8')

    # Confirm file was written to the canonical (monkeypatched) path
    assert seed_file.exists()
    content = json.loads(seed_file.read_text(encoding='utf-8'))
    assert 'Zland' in content

    # Call reload_seed() and ensure in-memory data reflects the new content
    vr.reload_seed()
    assert 'Zland' in vr.VISA_REQUIREMENTS
