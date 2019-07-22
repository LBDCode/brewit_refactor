from flask_wtf import FlaskForm
from wtforms import StringField, SelectField

class SearchForm(FlaskForm):
    query = StringField('search')
    style = SelectField(u'Beer Style', choices=[('', ''), ('brown', 'Brown'), ('ipa', 'IPA'), ('amber', 'Amber'), ('lager', 'Lager')])
    abv = SelectField(u'ABV', choices=[('', ''), ('0-4', '<4'), ('4-6', '4-6'), ('6-8', '6-8'), ('8-10', '8-10'), ('>10', '>10')])
    ibu = SelectField(u'IBU', choices=[('', ''), ('0-20', '<20'), ('21-40', '21-40'), ('41-60', '41-60'), ('61-80', '61-80'), ('81-100', '81-100'), ('>100', '>100')])