"""Visa document requirements data and helpers.
This module now prefers a JSON seed file in `/data/visa_requirements_seed.json` if present.
It provides helpers to list countries, visa types, and fetch requirements.
"""

import json
import os
from typing import Dict, Any

SEED_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'visa_requirements_seed.json')

# Default minimal fallback if JSON is missing
FALLBACK = {
    'Portugal': {
        'residence_by_investment': [
            'Passport (valid for at least 6 months)',
            'Proof of investment',
            'Passport-size photo (biometric)'
        ]
    }
}


def _load_from_seed() -> Dict[str, Any]:
    if os.path.exists(SEED_PATH):
        try:
            with open(SEED_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except Exception as e:
            print('Error loading visa requirements seed:', e)
    return FALLBACK


VISA_REQUIREMENTS = _load_from_seed()

DEFAULT_SEED_PATH = os.path.join(os.path.dirname(SEED_PATH), 'visa_requirements_seed_default.json')


def reload_seed():
    """Reload the in-memory VISA_REQUIREMENTS from the JSON seed file."""
    global VISA_REQUIREMENTS
    VISA_REQUIREMENTS = _load_from_seed()
    return VISA_REQUIREMENTS


def restore_default_seed():
    """Restore the seed from the default copy and reload."""
    if os.path.exists(DEFAULT_SEED_PATH):
        try:
            with open(DEFAULT_SEED_PATH, 'r', encoding='utf-8') as src, open(SEED_PATH, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
            return reload_seed()
        except Exception as e:
            print('Error restoring default seed:', e)
            return None
    else:
        # no default; write current in-memory as default
        try:
            with open(DEFAULT_SEED_PATH, 'w', encoding='utf-8') as f:
                json.dump(VISA_REQUIREMENTS, f, indent=2, ensure_ascii=False)
            return reload_seed()
        except Exception as e:
            print('Error writing default seed:', e)
            return None


def list_countries():
    return sorted(VISA_REQUIREMENTS.keys())


def list_visa_types(country):
    return sorted(VISA_REQUIREMENTS.get(country, {}).keys())


def get_requirements(country=None, visa_type=None):
    """Return a dict of requirements. If country provided, narrow to that country.
    If visa_type provided, narrow further. Returns structure: {country: {visa_type: [docs]}} or similar."""
    if country and visa_type:
        data = {}
        country_data = VISA_REQUIREMENTS.get(country, {})
        if visa_type in country_data:
            data[country] = {visa_type: country_data[visa_type]}
        return data

    if country:
        return {country: VISA_REQUIREMENTS.get(country, {})}

    return VISA_REQUIREMENTS
