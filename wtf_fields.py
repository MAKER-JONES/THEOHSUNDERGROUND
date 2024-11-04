from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, EqualTo, InputRequired, EqualTo, ValidationError, Email
from app import *
from passlib.hash import pbkdf2_sha256




def invalid_credentials(form, field):
    username_entered = form.username.data
    password_entered = field.data

    user_object = User.query.filter_by(username=username_entered).first()

    if user_object is None:
        raise ValidationError(' username or password incorrect ')
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError(' username or password incorrect ')



class RegistrationForm(FlaskForm):
    email = StringField('email-label', 
        validators=[InputRequired(message='email required'), Email(message='invalid email')  ])
    username = StringField('username-label',
        validators=[InputRequired(message='username required')])
    password = PasswordField('password-label',
        validators=[InputRequired(message='password required'), Length(min=4, message='password must be more than 4 characters')])
    confirm_pswd = PasswordField('confirm_pswd-label', validators=[InputRequired(message='password required'), 
        EqualTo('password', message='password much match ')])
    name = StringField('name-label',
        validators=[InputRequired(message='name required')])
    phone  =StringField('phone-label',
        validators=[Length(min=10,max=10, message='invalid number, make sure there are no dashes')])
    why = TextAreaField('why-label',
        validators=[InputRequired(message='must be filled out')])
    submit_button = SubmitField('create')

    def validate_username(self, username):
       
        user_object = User.query.filter_by(username=username.data).first()
        userBan_object = banned.query.filter_by(username=username.data).first()
        
        
        if user_object:
            raise ValidationError(' username already exists ')
        elif userBan_object:
           raise ValidationError(' usrename already exists ')
        elif ' ' in username.data:
            raise ValidationError(' cannot have spaces in username')
    def validate_name(self, name):
        userBan_name = banned.query.filter_by(name = name.data).first()
        userOB = User.query.filter_by(name = name.data).first()
        if userBan_name:
           raise ValidationError('You are banned')
        if userOB:
            raise ValidationError('Name is taken')
class DoorForm(FlaskForm):
    password = PasswordField('password-label',
        validators=[InputRequired(message='input required')])
    submit_button = SubmitField('login')

    


class LoginForm(FlaskForm):
    username = StringField('username-label', 
        validators=[InputRequired(message='username required'), ])
    password = PasswordField('password-label', 
        validators=[InputRequired(message='password required'), invalid_credentials]) 
    submit_button = SubmitField('Login')

    def validate_username(self, username):
        user_object = banned.query.filter_by(username=username.data).first()
        user_object2 = Req.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError('You are banned')
        if user_object2:
            raise ValidationError('Your account is still in the acceptence process')

    
