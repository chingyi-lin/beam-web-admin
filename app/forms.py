from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, FormField, TextAreaField
from wtforms.validators import DataRequired, Required, Length
from wtforms.fields.html5 import EmailField
from .models import *
from flask_material import Material 

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class SignUpForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = EmailField('Email', validators = [DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])

class NoteForm(Form):           
    noteTitle = StringField('Title', validators=[DataRequired()])
    noteContent = TextAreaField('Content', validators=[DataRequired()])
    noteCategory = SelectField(label='Category', choices = [('Other','Other'), ('Education','Education'), ('Entertainment','Entertainment'),('Finance','Finance'), \
        ('News/Reference', 'News/Reference'), ('Shopping', 'Shopping'), ('Travel','Travel')], default='Other', validators = [DataRequired()])

