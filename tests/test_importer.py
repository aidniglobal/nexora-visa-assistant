import json
import tempfile
from scripts.import_visa_requirements import validate_structure, import_file


def test_validate_structure_accepts_valid():
    data = {
        "Testland": {
            "work_visa": ["Passport", "Contract"]
        }
    }
    ok, err = validate_structure(data)
    assert ok and err is None


def test_validate_structure_rejects_invalid():
    data = ["not","a","dict"]
    ok, err = validate_structure(data)
    assert not ok and isinstance(err, str)


def test_import_file_writes_seed(tmp_path):
    src = tmp_path / 'sample.json'
    content = {
        "X": {"v1": ["A","B"]}
    }
    src.write_text(json.dumps(content, indent=2))

    # call import_file; it will write to the repo's data path
    res = import_file(str(src))
    assert res == 0
    # verify file exists
    from pathlib import Path
    dest = Path(__file__).resolve().parents[1] / 'data' / 'visa_requirements_seed.json'
    assert dest.exists()
    loaded = json.loads(dest.read_text())
    assert 'X' in loaded and 'v1' in loaded['X']
