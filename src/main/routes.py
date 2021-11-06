from flask import render_template
from main import app

@app.route('/')
@app.route('/admin')
def adminLanding():
    return "Hello Admin";