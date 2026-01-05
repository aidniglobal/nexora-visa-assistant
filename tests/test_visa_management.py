import json
from pathlib import Path
import os
import app.visa_requirements as vr


def test_restore_default_seed(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    data_dir = repo_root / 'data'
    os.makedirs(data_dir, exist_ok=True)

    seed = data_dir / 'visa_requirements_seed.json'
    default = data_dir / 'visa_requirements_seed_default.json'

    # write a default file
    default_data = {"DEF": {"vt": ["a"]}}
    default.write_text(json.dumps(default_data, indent=2))

    # write a different seed
    seed.write_text(json.dumps({"X": {"vt": ["b"]}}, indent=2))

    # call restore
    vr.restore_default_seed()

    loaded = json.loads(seed.read_text())
    assert 'DEF' in loaded and loaded['DEF']['vt'] == ['a']
