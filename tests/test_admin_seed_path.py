import json
from io import BytesIO

import app.visa_requirements as vr


def test_admin_import_writes_seed_and_reload(client, login_admin, tmp_path, monkeypatch):
    # Use a temporary file for the seed so test doesn't touch repo data
    seed_path = tmp_path / "visa_requirements_seed.json"
    default_path = tmp_path / "visa_requirements_seed_default.json"

    # Monkeypatch module-level constants safely (automatically restored by pytest)
    monkeypatch.setattr(vr, 'SEED_PATH', str(seed_path))
    monkeypatch.setattr(vr, 'DEFAULT_SEED_PATH', str(default_path))

    # Ensure no existing seed
    if seed_path.exists():
        seed_path.unlink()

    payload = json.dumps({"Narnia": {"tourist": ["Passport"]}})
    data = {"file": (BytesIO(payload.encode('utf-8')), 'test.json')}

    # Post via admin UI to ensure the same code-path is exercised
    resp = client.post('/admin/import-visa-requirements', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert resp.status_code == 200

    # Seed file should have been written to the canonical (patched) path
    assert seed_path.exists(), f"Expected seed file at {seed_path}"

    # Explicitly reload in-memory representation and assert the new country is visible
    vr.reload_seed()
    countries = vr.list_countries()
    assert 'Narnia' in countries

    # Additional verification: read file contents
    with open(seed_path, 'r', encoding='utf-8') as f:
        d = json.load(f)
    assert 'Narnia' in d
