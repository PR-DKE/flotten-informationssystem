from flask import render_template, redirect, flash, url_for
from main import app
from flask import render_template
from main.forms import LoginForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def indexLanding():
    form=LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('adminLanding'))
    return render_template("index.html", form=form, title="Welcome")

@app.route('/admin')
def adminLanding():
    return render_template("admin.html", title="Flotte- Home")

