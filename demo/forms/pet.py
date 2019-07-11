from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import InputRequired, Length


class PetForm(FlaskForm):

    pet_name = StringField('Pet Name', validators=[InputRequired(), Length(max=200)])
    pet_date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[InputRequired()])

