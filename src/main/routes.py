from datetime import datetime

from flask import render_template, redirect, flash, url_for, request, abort, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from itertools import accumulate

from sqlalchemy import and_
from sqlalchemy.sql.operators import is_

from main import app, db
from flask import render_template

from main.decorators import admin_required
from main.forms import LoginForm, AddUserForm, AddTriebwagenForm, AddPersonenwaggonForm, EditPasswordForm
from main.models import User, Triebwagen, Personenwaggon, Zug, Maintenance
from main.util import calculate_sitze, calculate_waggons, calculate_maxgewicht, get_spurweite


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
                next = url_for('home')
            return redirect(next)
    return render_template("index.html", form=form, title="Welcome")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have benn logged out')
    return redirect(url_for('indexLanding'))

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST' and current_user.is_admin:
        if request.form.get('personenwaggon'):
            db.session.query(Personenwaggon).filter(Personenwaggon.fahrgestellnummer == request.form.get('personenwaggon')).delete()
            db.session.commit()
            flash("Deleted Personenwaggon: {}".format(request.form.get('personenwaggon')))
        if request.form.get('triebwagen'):
            db.session.query(Triebwagen).filter(
            Triebwagen.fahrgestellnummer == request.form.get('triebwagen')).delete()
            db.session.commit()
            flash("Deleted Triebwagen: {}".format(request.form.get('triebwagen')))
        if request.form.get('zug'):
            db.session.query(Zug).filter(Zug.id==request.form.get('zug')).delete()
            db.session.commit()
            flash("Deleted Zug {}".format(request.form.get('zug')))
        return redirect(url_for('home'))
    triebwagen = Triebwagen.query.all()
    personenwaggons = Personenwaggon.query.all()
    zuege = Zug.query.all()
    m = Maintenance.query.filter(Maintenance.emp_association.any(email=current_user.email)).all()
    m_f = [m for m in m if m.datetime.date() >= datetime.now().date()]
    return render_template("home.html", title="Flotte- Home", triebwaegen=triebwagen, personenwaggons=personenwaggons, zuege=zuege,
                           triebwagen_query=Triebwagen.query, personenwaggon_query=Personenwaggon.query, calculate_sitze=calculate_sitze,
                           calculate_waggons=calculate_waggons, calculate_maxgewicht=calculate_maxgewicht, get_spurweite=get_spurweite,
                           wartungen=m_f)

@app.route('/user', methods=['GET', 'POST'])
@login_required
@admin_required
def addUser():
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    password=form.password.data,
                    is_admin = form.is_admin.data)
        db.session.add(user)
        db.session.commit()
        flash('User {} has been registered.'.format(user.email))
        return redirect(url_for('addUser'))
    return render_template("add-user.html", form=form, title='Add User')

@app.route('/admin/waggon', methods=['GET', 'POST'])
@login_required
@admin_required
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
        spurweite = 1435
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
    return render_template("add-waggon.html", form=form, form2=form2, title='Add Waggons')

@app.route('/api/admin/train', methods=['POST'])
@login_required
@admin_required
def train():
    has_triebwagen = False
    has_error=False
    spurweite = 0
    gewicht = 0
    train = Zug()
    train.name= request.form.get('zug_name')
    db.session.add(train)
    db.session.commit()
    for field in request.form.items():
        if field.__getitem__(0).__contains__('tw'):
            if has_triebwagen:
                flash('Error: Too many Triebwagen')
                has_error=True
            has_triebwagen=True
            tw = Triebwagen.query.filter_by(fahrgestellnummer=field.__getitem__(1)).first()
            spurweite=tw.spurweite
            train.triebwagen=tw.fahrgestellnummer
            tw.zug_id=train.id
        if field.__getitem__(0).__contains__('pw'):
            pw = Personenwaggon.query.filter_by(fahrgestellnummer=field.__getitem__(1)).first()
            if spurweite == 0:
                spurweite = pw.spurweite
            elif spurweite != pw.spurweite:
                flash('Error: Spurweite of Personenwaggon {} does not match'.format(pw.fahrgestellnummer))
                has_error=True
            gewicht=gewicht+pw.maxGewicht
            train.personenwaggons.append(pw)
    if not has_triebwagen:
        flash('No Triebwagen has been selected')
        has_error=True
    elif gewicht > tw.zugkraft:
        flash('Zugkraft is not sufficient')
        has_error=True
    if not has_error:
        db.session.commit()
        flash("Zug with id {} has been added".format(train.id))
    else:
        db.session.rollback()
        db.session.query(Zug).filter(Zug.id == train.id).delete()
        db.session.commit()
    return redirect(url_for('home'))

@app.route("/admin/train/<id>")
@login_required
@admin_required
def edit_train(id):
    zug = Zug.query.get(id)
    triebwagen = Triebwagen.query.get(zug.triebwagen)
    waggons= Personenwaggon.query.filter_by(spurweite=triebwagen.spurweite)
    own_waggons = Personenwaggon.query.filter_by(zug_id=id)
    return render_template("edit-train.html", waggons=waggons, zug=zug, own_waggons=own_waggons, calculate_sitze=calculate_sitze,
                           calculate_waggons=calculate_waggons, calculate_maxgewicht=calculate_maxgewicht, get_spurweite=get_spurweite,
                           triebwagen_query=Triebwagen.query, personenwaggon_query=Personenwaggon.query)


@app.route("/admin/train/<id>/wartung")
@login_required
@admin_required
def wartung(id):
    zug = Zug.query.get(id)
    emps = User.query.filter_by(is_admin=False)
    return render_template("wartung.html", zug=zug, emps=emps)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = EditPasswordForm()
    if form.validate_on_submit():
        u = User.query.get(current_user.get_id())
        u.password = form.password.data
        db.session.commit()
        flash("Password has been changed")
    return render_template('settings.html', form=form)


@app.route("/api/admin/train/<id>/wartung", methods=["POST"])
@login_required
@admin_required
def scheduleMaintenance(id):
    flash("Scheduled")
    if request.method=='POST':
        form = request.form
        maintenance = Maintenance(datetime=form.get('date'),
                                  duration=form.get('duration'),
                                    description=form.get('description'),
                                  zug_id=id
                                  )
        db.session.add(maintenance)
        db.session.commit()
        for field in form.items():
            if field.__getitem__(0).__contains__('emp.'):
                mail = field.__getitem__(1)
                u = User.query.filter_by(email=mail).first()
                maintenance.emp_association.append(u)
        db.session.commit()
    return redirect(url_for("wartung", id=id))

@app.route("/api/admin/train/<id>/waggon/<fahrgestellnummer>", methods=["POST"])
@login_required
@admin_required
def add_waggon_to_train(id, fahrgestellnummer):
    zug = Zug.query.get(id)
    waggon = Personenwaggon.query.get(fahrgestellnummer)
    triebwagen = Triebwagen.query.get(zug.triebwagen)

    if waggon.spurweite != triebwagen.spurweite:
        flash("Spurweite does not match")
        abort(500)

    waggons = Personenwaggon.query.filter_by(zug_id=id)
    maxGewicht = 0
    for w in waggons:
        maxGewicht = maxGewicht+w.maxGewicht

    if maxGewicht + waggon.maxGewicht > triebwagen.zugkraft:
        flash("Zugkraft not sufficient")
    else:
        zug.personenwaggons.append(waggon)
        db.session.commit()
        flash("Waggon {} added to train {}".format(waggon.fahrgestellnummer, id))
    return redirect(url_for('edit_train', id=id))

@app.route("/api/admin/train/<id>/waggon/own/<fahrgestellnummer>", methods=['POST'])
@login_required
@admin_required
def remove_waggon_from_train(id, fahrgestellnummer):
    waggon = Personenwaggon.query.get(fahrgestellnummer)
    waggon.zug_id = None
    db.session.commit()
    flash("Personenwaggon {} removed from train {}".format(fahrgestellnummer, id))
    return redirect(url_for('edit_train', id=id))

@app.route("/api/admin/train/<id>/name", methods=["POST"])
@login_required
@admin_required
def edit_train_name(id):
    form = request.form
    train = Zug.query.get(id)
    train.name = request.form.get('name')
    db.session.commit()
    return redirect(url_for('edit_train', id=id))

@app.route("/api/admin/train/<id>", methods=["GET"])
@login_required
@admin_required
def delete_train(id):
    db.session.query(Zug).filter(
        Zug.id == id).delete()
    db.session.commit()
    flash("Zug {} deleted".format(id))
    return redirect(url_for('home'))

@app.route("/api/train")
def get_trains():
    trains = Zug.query.all()
    return jsonify({'trains':[train.to_json() for train in trains]})

@app.route("/api/train/<id>")
def get_train(id):
    train = Zug.query.get(id)
    return jsonify(train.to_json())

@app.route("/api/train/<id>/maintenance")
def get_maintenances_for_train(id):
    m = Maintenance.query.filter_by(zug_id=id)
    m_f = [m for m in m if m.datetime.date() >= datetime.now().date()]
    return jsonify({'maintenances': [m.to_json_medium() for m in m]})
