from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(max=200)])
    password = PasswordField('Password', validators=[InputRequired(), Length(max=200)])
    submit = SubmitField('Sign In')
