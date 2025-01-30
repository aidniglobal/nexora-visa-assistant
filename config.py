import os

class Config:
    SECRET_KEY = os.environ.get('eafcf00803afe5300d29b09f92de1545') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/nova.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True