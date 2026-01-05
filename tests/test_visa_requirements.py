import json
from pathlib import Path
import os
from app import app
import app.visa_requirements as vr


def test_reload_seed(tmp_path, monkeypatch):
    # write a small seed and ensure reload_seed picks it up
    seed = tmp_path / 'seed.json'
    data = {"Y": {"vt": ["doc1","doc2"]}}
    seed.write_text(json.dumps(data))

    repo_root = Path(__file__).resolve().parents[1]
    dest = repo_root / 'data' / 'visa_requirements_seed.json'
    os.makedirs(dest.parent, exist_ok=True)
    dest.write_text(seed.read_text())

    # reload
    vr.reload_seed()
    out = vr.get_requirements(country='Y', visa_type='vt')
    assert 'Y' in out and 'vt' in out['Y']
    assert out['Y']['vt'] == ['doc1', 'doc2']
