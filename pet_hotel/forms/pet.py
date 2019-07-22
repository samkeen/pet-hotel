from wtforms import StringField, DateField, Form
from wtforms.validators import InputRequired, Length


class PetForm(Form):
    name = StringField('Pet Name', validators=[InputRequired(), Length(max=200)])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[InputRequired()])
