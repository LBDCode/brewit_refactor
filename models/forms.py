from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from markupsafe import Markup
from wtforms.widgets import HiddenInput

class SearchForm(FlaskForm):
    query = StringField('search')
    style = SelectField(u'Beer Style', choices=[('', ''), ('brown', 'Brown'), ('ipa', 'IPA'), ('amber', 'Amber'), ('lager', 'Lager')])
    abv = SelectField(u'ABV', choices=[('', ''), ('0-4', '<4'), ('4-6', '4-6'), ('6-8', '6-8'), ('8-10', '8-10'), ('>10', '>10')])
    ibu = SelectField(u'IBU', choices=[('', ''), ('0-20', '<20'), ('21-40', '21-40'), ('41-60', '41-60'), ('61-80', '61-80'), ('81-100', '81-100'), ('>100', '>100')])
    submitAdvanced = SubmitField('Search')

class SimpleSearchForm(FlaskForm):
    query = StringField('search')
    # submit_value = Markup('<span class="input-group-text" title="Search"></span>')
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

