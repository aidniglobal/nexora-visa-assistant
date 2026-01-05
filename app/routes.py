import os
from flask import Blueprint, render_template

main = Blueprint('main', __name__)
TEMPLATE_DIR = os.path.abspath("templates")

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about_us.html')
