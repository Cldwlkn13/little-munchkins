from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Optional
from wtforms.widgets.html5 import NumberInput


class RecipeForm(FlaskForm):
    title = StringField(
        'Search recipes by name', validators=[Optional()])
    months = IntegerField(
        "Age (months)", validators=[Optional()], widget=NumberInput())
    submit = SubmitField('Submit')

