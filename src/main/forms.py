from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, RadioField, DecimalField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from main.models import User, Triebwagen, Waggon, Personenwaggon


class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')



class AddUserForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    is_admin = BooleanField('Admin ?')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
        if not field.data.strip().endswith('@jku-linien.at'):
            raise ValidationError('Only company email allowed (@jku-linien.at)')

class AddTriebwagenForm(FlaskForm):
    spurweite = RadioField('Spurweite (mm)', choices=[('normalspur','1435'),('schmalspur','1000')], default='normalspur')
    fahrgestellnummer = StringField('Fahrgestellnummer', validators=[DataRequired(), Regexp('^[A-Za-z0-9]*$', message="Field may only contain numbers and letters")])
    zugkraft = DecimalField('Zugkraft (t)', validators=[DataRequired()])
    submit = SubmitField('Add Waggon')

    def validate_fahrgestellnummer(self, field):
        if Triebwagen.query.filter_by(fahrgestellnummer=field.data).first() \
                or Personenwaggon.query.filter_by(fahrgestellnummer=field.data).first():
            raise ValidationError('Fahrgestellnummer already in use')

class AddPersonenwaggonForm(FlaskForm):
    spurweite = RadioField('Spurweite (mm)', choices=[('normalspur', '1435'), ('schmalspur', '1000')],
                           default='normalspur')
    fahrgestellnummer = StringField('Fahrgestellnummer', validators=[DataRequired(), Regexp('^[A-Za-z0-9]*$', message="Field may only contain numbers and letters")])
    sitzanzahl = IntegerField('Sitzplätze', validators=[DataRequired()])
    maxGewicht = DecimalField('Maximal-Gewicht (t)', validators=[DataRequired()])
    submi = SubmitField('Add Waggon')

    def validate_fahrgestellnummer(self, field):
        if Triebwagen.query.filter_by(fahrgestellnummer=field.data).first() \
                or Personenwaggon.query.filter_by(fahrgestellnummer=field.data).first():
            raise ValidationError('Fahrgestellnummer already in use')

class EditPasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Retype New Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_old_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('Old Password not correct')