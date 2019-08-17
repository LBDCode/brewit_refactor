from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from brewit.models.users import User
from flask_login import current_user

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
    email = StringField('Email', validators=[DataRequired(), Email(message="invalid email")])
    username = StringField('User name', validators=[DataRequired(), Length(min=2, max=20, message="please select a username between 2 and 20 characters")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20, message="please select a username between 6 and 20 characters")])
    confpw = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password', message="passwords must match")])
    submitSignup = SubmitField('Signup')
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('There is already an account associated with that email.')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That user name is already taken.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="invalid email")])
    password = PasswordField('Password', validators=[DataRequired()])
    submitLogin = SubmitField('Login')

class UpdateForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="invalid email")])
    username = StringField('User name', validators=[DataRequired(), Length(min=2, max=20, message="please select a username between 2 and 20 characters")])
    submitUpdate = SubmitField('Update')
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('There is already an account associated with that email.')
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That user name is already taken.')
class UpdateKey(FlaskForm):
    submitNewKey = SubmitField('Request new key')
