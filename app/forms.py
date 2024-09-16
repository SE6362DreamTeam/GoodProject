from flask_wtf import FlaskForm
from wtforms import StringField, URLField
from wtforms.validators import DataRequired, URL

class URLForm(FlaskForm):
    # Search term field - Required
    search_term = StringField('Search Term', validators=[DataRequired()])

    # URL field - Required, must be a valid URL
    url = URLField('URL', validators=[DataRequired(), URL(message="Please enter a valid URL.")])
