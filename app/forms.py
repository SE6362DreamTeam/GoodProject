from flask_wtf import FlaskForm
from wtforms import StringField, URLField
from wtforms.validators import DataRequired, URL

class URLForm(FlaskForm):
    search_term = StringField('Search Term', validators=[DataRequired()])
    url = URLField('URL', validators=[DataRequired(), URL()])
