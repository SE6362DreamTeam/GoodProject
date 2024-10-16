from flask_wtf import FlaskForm
from wtforms import StringField, URLField, SubmitField, RadioField
from wtforms.validators import DataRequired, URL

class URLForm(FlaskForm):
    search_term = StringField('Search Term', validators=[DataRequired()])
    url = URLField('URL', validators=[DataRequired(), URL()])


class SearchForm(FlaskForm):
    keyword = StringField('Enter keyword', validators=[DataRequired()])
    search_type = RadioField('Search Type', choices=[('and', 'AND'), ('or', 'OR'), ('not', 'NOT')], validators=[DataRequired()])
    submit = SubmitField('Search')
