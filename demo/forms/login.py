from wtforms import StringField, PasswordField, SubmitField, Form
from wtforms.validators import InputRequired, Length


class LoginForm(Form):
    username = StringField('Username', validators=[InputRequired(), Length(max=200)])
    password = PasswordField('Password', validators=[InputRequired(), Length(max=200)])
