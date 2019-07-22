from wtforms import StringField, SubmitField, Form
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, Regexp, Email


class OwnerForm(Form):
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=100)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=100)])
    phone_number = StringField('Phone Number', validators=[
        Regexp(regex='\\d\\d\\d-\\d\\d\\d-\\d\\d\\d\\d', message='Must be in the form: 000-000-0000')])
    email = EmailField('Email', validators=[Email(), Length(max=200)])