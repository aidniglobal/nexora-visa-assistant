import sys
import os

# Ensure the correct module path - import from app.py, not app/ directory
if 'app' in sys.modules:
    del sys.modules['app']

# Import the Flask app from app.py
import importlib.util
spec = importlib.util.spec_from_file_location("flask_app", os.path.join(os.path.dirname(__file__), "app.py"))
flask_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(flask_app)
app = flask_app.app

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
