"""CLI helper to import a JSON file into `data/visa_requirements_seed.json`.
Usage: python scripts/import_visa_requirements.py path/to/file.json

This script validates basic shape (dict of countries -> visa types -> list of strings) and writes to data/visa_requirements_seed.json
"""
import json
import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SEED_DEST = os.path.join(ROOT, 'data', 'visa_requirements_seed.json')


def validate_structure(data):
    if not isinstance(data, dict):
        return False, 'Root must be an object/dict of countries.'
    for country, types in data.items():
        if not isinstance(types, dict):
            return False, f'Country {country} must map to dict of visa types.'
        for vtype, docs in types.items():
            if not isinstance(docs, list) or not all(isinstance(d, str) for d in docs):
                return False, f'Visa type {vtype} for {country} must be a list of strings.'
    return True, None


def import_file(src):
    if not os.path.exists(src):
        print('Source file not found:', src)
        return 2
    with open(src, 'r', encoding='utf-8') as f:
        data = json.load(f)
    ok, err = validate_structure(data)
    if not ok:
        print('Validation failed:', err)
        return 3
    os.makedirs(os.path.dirname(SEED_DEST), exist_ok=True)
    with open(SEED_DEST, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print('Successfully imported to', SEED_DEST)
    return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python scripts/import_visa_requirements.py path/to/file.json')
        sys.exit(1)
    src = sys.argv[1]
    sys.exit(import_file(src))