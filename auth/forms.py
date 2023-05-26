from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from wtforms import PasswordField, StringField, EmailField, SelectField


class RegisterForm(FlaskForm):
    name = StringField('Full Nmae')
    phone = StringField('Phone Number')
    password = PasswordField('Password', validators=[DataRequired('گذرواژه خود را وارد نمایید'), Length(min=8, message='گذرواژه نباید کمتر از 8 کاراکتر باشد')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired('تکرار گذرواژه با گذرواژه یکسان نیست'), EqualTo('password')])
    
    
    
class LoginForm(FlaskForm):
    name = StringField('Full Nmae')
    phone = StringField('Phone Number')
    password = PasswordField('Password', validators=[DataRequired('گذرواژه خود را وارد نمایید'), Length(min=8, message='گذرواژه نباید کمتر از 8 کاراکتر باشد')])


class SuperUserForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired('گذرواژه خود را وارد نمایید'), Length(min=8)])
    

    