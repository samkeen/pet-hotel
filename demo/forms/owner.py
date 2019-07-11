from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, Regexp, Email


class OwnerForm(FlaskForm):
    owner_first_name = StringField('First Name', validators=[InputRequired(), Length(max=100)])
    owner_last_name = StringField('Last Name', validators=[InputRequired(), Length(max=100)])
    owner_phone_number = StringField('Phone Number', validators=[
        Regexp(regex='\\d\\d\\d-\\d\\d\\d-\\d\\d\\d\\d', message='Must be in the form: 000-000-0000')])
    owner_email = EmailField('Email', validators=[Email(), Length(max=200)])
