import os
from flask import Blueprint, render_template

main = Blueprint('main', __name__)
TEMPLATE_DIR = os.path.abspath("templates")

@main.route('/')
def home():
    return render_template(os.path.join(TEMPLATE_DIR, "index.html"))

@main.route('/about')
def about():
    return render_template(os.path.join(TEMPLATE_DIR, 'about_us.html'))
