from flask.ext.wtf import Form
from flask.ext.wtf.file import FileRequired, FileAllowed, FileField
from wtforms import StringField, BooleanField, PasswordField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Optional


class LoginForm(Form):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember me', default=False)


class RegistrationForm(Form):
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm = PasswordField('Confirm password:', validators=[EqualTo('password')])


class PostForm(Form):
    title = StringField('Title:', validators=[DataRequired()])
    body = TextAreaField('Body:', validators=[DataRequired()])
    startnow = BooleanField('Start now', validators=[Optional()], default=True)
    date = DateField('Start date: (if not now)', validators=[Optional()])


class SubmissionForm(Form):
    body = TextAreaField('Body:', validators=[DataRequired()])
    image = FileField('Image:', validators=[
        FileRequired(),
    ])