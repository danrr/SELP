from flask.ext.wtf import Form
from flask.ext.wtf.file import FileRequired, FileField
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, RadioField, DateTimeField, FieldList
from wtforms.validators import DataRequired, Email, EqualTo


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
    ingredients = FieldList(StringField('Ingredient', validators=[DataRequired()]), min_entries=1)
    difficulty = RadioField("Difficulty:",
                            choices=[(1, "Beginner"), (2, "Novice"), (3, "Intermediate"), (4, "Hard"), (5, "Expert")],
                            coerce=int,
                            validators=[DataRequired()])
    start_time = DateTimeField('Start Time:', validators=[DataRequired()], format='%d-%m-%Y %H:%M')


class SubmissionForm(Form):
    body = TextAreaField('Body:', validators=[DataRequired()])
    image = FileField('Image:', validators=[
        FileRequired(),
    ])

class SearchForm(Form):
    search = StringField('Search', validators=[DataRequired()])