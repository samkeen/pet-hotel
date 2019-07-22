from wtforms import SubmitField, DateField, SelectField, Form
from wtforms.validators import InputRequired


class BookingForm(Form):
    owner_id = SelectField('Owner')
    pet_id = SelectField('Pet')
    check_in_date = DateField('Check In', format='%Y-%m-%d', validators=[InputRequired()])
    check_out_date = DateField('Check Out', format='%Y-%m-%d', validators=[InputRequired()])
