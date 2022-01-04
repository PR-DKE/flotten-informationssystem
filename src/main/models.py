from datetime import datetime

from flask import url_for
from sqlalchemy import null
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from main import db, login_manager


@login_manager.user_loader
def load_user(user_email):
    return User.query.get(user_email)


class User(UserMixin,db.Model):
    __tablename__='users'

    email = db.Column(db.String(120), primary_key=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def get_id(self):
        return self.email

class Waggon(db.Model):
    fahrgestellnummer = db.Column(db.String(64), primary_key=True)
    spurweite = db.Column(db.Integer, index=True)
    __abstract__ = True

    def __repr__(self):
        return 'Triebwagen {}'.format(self.fahrgestellnummer)


class Triebwagen(Waggon):
    zugkraft = db.Column(db.DECIMAL)
    zug_id = db.Column(db.Integer, db.ForeignKey('zug.id', ondelete='SET NULL'))

class Personenwaggon(Waggon):
    sitzanzahl = db.Column(db.Integer)
    maxGewicht = db.Column(db.DECIMAL)
    zug_id = db.Column(db.Integer, db.ForeignKey('zug.id', ondelete='SET NULL'))

class Zug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default=null)
    triebwagen = db.Column(db.String, db.ForeignKey('triebwagen.fahrgestellnummer'))
    personenwaggons = db.relationship("Personenwaggon", backref="zug")

    def calculate_max_weight(self):
        summe = 0
        waggons = Personenwaggon.query.filter_by(zug_id=self.id)
        for waggon in waggons:
            summe = summe + waggon.maxGewicht
        return summe

    def get_spurweite(self):
        return Triebwagen.query.get(self.triebwagen).spurweite

    def get_zugkraft(self):
        return Triebwagen.query.get(self.triebwagen).zugkraft

    def calculate_seat_number(self):
        summe = 0
        waggons = Personenwaggon.query.filter_by(zug_id=self.id)
        for waggon in waggons:
            summe = summe + waggon.sitzanzahl
        return summe

    def calculate_waggon_number(self):
        summe = 0
        waggons = Personenwaggon.query.filter_by(zug_id=self.id)
        for waggon in waggons:
            summe += 1
        return summe

    def to_json(self):
        triebwagen = Triebwagen.query.get(self.triebwagen)
        waggons = Personenwaggon.query.filter_by(zug_id=self.id)
        sitze = 0
        count = 0
        for waggon in waggons:
            sitze += waggon.sitzanzahl
            count+=1
        ma = Maintenance.query.filter_by(zug_id=self.id)
        filtered_m = [m for m in ma if m.datetime.date() >= datetime.now().date()]
        json_train={
            'url': url_for('get_train', id=self.id),
            'maintenances_url': url_for('get_maintenances_for_train', id=self.id),
            'name': self.name,
            'id': self.id,
            'waggons': count,
            'sitze': sitze,
            'spurweite': triebwagen.spurweite,
            'wartungen': [m.to_json_light() for m in filtered_m]
        }
        return json_train



maintenance_employee_association = db.Table('maintenance_employee_association',
                                      db.Column('maintenance_id', db.ForeignKey('maintenance.id', ondelete="CASCADE")),
                                      db.Column('employee_id', db.ForeignKey('users.email', ondelete="SET NULL")))

class Maintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zug_id = db.Column(db.Integer, db.ForeignKey('zug.id', ondelete="CASCADE"), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.DECIMAL, nullable=True)
    description = db.Column(db.String, nullable=True)
    emp_association = db.relationship("User",
                                      secondary=maintenance_employee_association)

    def to_json_light(self):
        json_m = {
            'date': self.datetime.date().isoformat(),
            'start': self.datetime.time().isoformat(),
            'duration': self.duration
        }
        return json_m

    def to_json_medium(self):
        json_m = {
            'zug_id': self.zug_id,
            'date': self.datetime.date().isoformat(),
            'start': self.datetime.time().isoformat(),
            'duration': self.duration
        }

        return json_m

    def to_json_full(self):
        json_m = {
            'zug_id': self.zug_id,
            'date': self.datetime.date().isoformat(),
            'start': self.datetime.time().isoformat(),
            'duration': self.duration,
            'description': self.description
        }
        return json_m

