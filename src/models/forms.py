from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, Email
from markupsafe import Markup
from wtforms.widgets import HiddenInput

class SearchForm(FlaskForm):
    query = StringField('search', render_kw={"placeholder": "Search beer name or style"})
    style = SelectField(u'Beer Style', choices=[('', 'Style'), ('brown', 'Brown'), ('ipa', 'IPA'), ('amber', 'Amber'), ('lager', 'Lager')])
    abv = SelectField(u'ABV', choices=[('', 'ABV'), ('0.1-4', '<4'), ('4-6', '4-6'), ('6-8', '6-8'), ('8-10', '8-10'), ('>10', '>10')])
    ibu = SelectField(u'IBU', choices=[('', 'IBU'), ('0.1-20', '<20'), ('21-40', '21-40'), ('41-60', '41-60'), ('61-80', '61-80'), ('81-100', '81-100'), ('>100', '>100')])
    submitAdvanced = SubmitField('Search')

class SimpleSearchForm(FlaskForm):
    query = StringField('search')
    submitSimple = SubmitField('Search')

class TypeForm(FlaskForm):
    query = StringField('search')
    brown = SubmitField('Brown')
    lager = SubmitField('Lager')
    ipa = SubmitField('IPA')
    belgian = SubmitField('Belgian')
    cider = SubmitField('Cider')
    amber = SubmitField('Amber')
    stout = SubmitField('Stout')

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message="invalid email")])
    user_name = StringField('User name', validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(max=50)])
    confpw = PasswordField('Confirm password', validators=[InputRequired(), Length(max=50)])
    submitSignup = SubmitField('Signup')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    submitLogin = SubmitField('Login')

