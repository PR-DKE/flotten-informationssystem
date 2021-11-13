from flask import render_template, redirect, flash, url_for, request
from flask_login import login_required, login_user, logout_user

from main import app, db
from flask import render_template
from main.forms import LoginForm, AddUserForm, AddTriebwagenForm, AddPersonenwaggonForm
from main.models import User, Triebwagen, Personenwaggon


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
        if form.role_id.data:
            role = 1
        user = User(email=form.email.data,
                    password=form.password.data,
                    role_id = role)
        db.session.add(user)
        db.session.commit()
        flash('User {} has been registered.'.format(user.email))
        return redirect(url_for('addUser'))
    return render_template("addUser.html", form=form)

@app.route('/admin/waggon', methods=['GET', 'POST'])
@login_required
def addWaggon():
    form = AddTriebwagenForm()
    form2 = AddPersonenwaggonForm()
    if form.validate_on_submit():
        spurweite=1435
        if form.spurweite.data == 'schmalspur':
            spurweite=1000
        wagen = Triebwagen(fahrgestellnummer=form.fahrgestellnummer.data,
                           spurweite=spurweite,
                           zugkraft=form.zugkraft.data)
        db.session.add(wagen)
        db.session.commit()
        flash('Triebwagen {} has been added: '
              'Spurweite= {} '
              'Zugkraft= {} '.format(form.fahrgestellnummer.data, spurweite, form.zugkraft.data))
        return redirect(url_for('addWaggon'))
    if form2.validate_on_submit():
        if form2.spurweite.data == 'schmalspur':
            spurweite = 1000
        wagen = Personenwaggon(fahrgestellnummer=form2.fahrgestellnummer.data,
                           spurweite=spurweite,
                           sitzanzahl=form2.sitzanzahl.data,
                               maxGewicht=form2.maxGewicht.data)
        db.session.add(wagen)
        db.session.commit()
        flash('Personenwaggon {} has been added: '
              'Spurweite= {} '
              'Sitzplätze= {} '
              'Maximal-Gewicht= {}'.format(form2.fahrgestellnummer.data, spurweite, form2.sitzanzahl.data, form2.maxGewicht.data))
        return redirect(url_for('addWaggon'))
    return render_template("addWaggon.html", form=form, form2=form2)

