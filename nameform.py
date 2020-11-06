from wtforms import SubmitField, SelectField, PasswordField, StringField, BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


'''class NameForm creates an object inheriting from Form.
Using SelectField creates a dropdown which takes two arguments,
that make it a dropdown and SubmitField to create a save button'''
class NameForm(FlaskForm):
    select = SelectField('Select Product', choices=[
                         ('464 50lbs', '464 50lbs'),
                         ('444 50lbs', '444 50lbs'),
                         ('464 50lbs banded', '464 50lbs banded'),
                         ('464 10lbs', '464 10lbs'),
                         ('8oz Mason', '8oz Mason'),
                         ('4oz Jelly', '4oz Jelly'),
                         ('6oz Tin 120', '6oz Tin 120'),
                         ('4oz Tin 120', '4oz Tin 120'),
                         ('Soy Candle Making Kit', 'Soy Candle Making Kit'),
                         ('4oz candle tin 12pc', '4oz candle tin 12pc'),
                         ('8oz Mason MP', '8oz Mason MP')
                         ])
    submit = SubmitField('Save')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    login = SubmitField('Login')