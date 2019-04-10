from flask_wtf import FlaskForm
from wtforms import StringField

class SearchForm(FlaskForm):
	student = StringField('Student')
	course = StringField('Course')