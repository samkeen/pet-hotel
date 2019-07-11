from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, SelectField
from wtforms.validators import InputRequired


class BookingForm(FlaskForm):
    owner_id = SelectField('Owner')
    pet_id = SelectField('Pet')
    booking_check_in_date = DateField('Check In', format='%Y-%m-%d', validators=[InputRequired()])
    booking_check_out_date = DateField('Check Out', format='%Y-%m-%d', validators=[InputRequired()])
    submit = SubmitField('Book')
