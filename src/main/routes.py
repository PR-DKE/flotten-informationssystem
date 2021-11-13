from flask import render_template, redirect, flash, url_for, request
from flask_login import login_required, login_user, logout_user

from main import app, db
from flask import render_template
from main.forms import LoginForm, AddUserForm
from main.models import User


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def indexLanding():
    form=LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.email.data, form.remember_me.data))
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('adminLanding')
            return redirect(next)
    return render_template("index.html", form=form, title="Welcome")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have benn logged out')
    return redirect(url_for('indexLanding'))

@app.route('/admin')
@login_required
def adminLanding():
    return render_template("admin.html", title="Flotte- Home")

@app.route('/admin/user', methods=['GET', 'POST'])
@login_required
def addUser():
    form = AddUserForm()
    if form.validate_on_submit():
        role = 0
        if form.role_id:
            role = 1
        user = User(email=form.email.data,
                    password=form.password.data,
                    role_id = role)
        db.session.add(user)
        db.session.commit()
        flash('User {} has been registered'.format(user.email))
        return redirect(url_for('addUser'))
    return render_template("addUser.html", form=form)

