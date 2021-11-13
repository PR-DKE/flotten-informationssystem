from main import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Waggon(db.Model):
    fahrgestellnummer = db.Column(db.String(64), primary_key=True)
    spurweite = db.Column(db.Integer, index=True)
    __abstract__ = True

    def __repr__(self):
        return 'Triebwagen {}'.format(self.fahrgestellnummer)


class Triebwagen(Waggon):
    zugkraft = db.Column(db.Integer)

class Personenwaggon(Waggon):
    sitzanzahl = db.Column(db.Integer)
    maxGewicht = db.Column(db.Integer)





