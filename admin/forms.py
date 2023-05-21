from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from wtforms import PasswordField, StringField, EmailField, SelectField, FileField, TextAreaField


class UserEditForm(FlaskForm):
    name = StringField('Full Name')
    username = StringField('User Name')
    email = EmailField('Email')
    address_province = StringField('Province Address')
    address_city = StringField('City Address')
    address_street = StringField('Street Address')
    address_house_number = StringField('House Number Address')
    education_degree = StringField('Education Degree')
    education_field = StringField('Education Field')
    education_area = StringField('Education Area')
    skill_one = StringField('Skill One')
    skill_two = StringField('Skill Two')
    skill_three = StringField('Skill Three')
    skill_four = StringField('Skill Four')
    skill_five = StringField('Skill Five')
    about_me = TextAreaField('About Me')
    avatar = FileField('Avatar')
    
    
class UserAddForm(FlaskForm):
    name = StringField('User Name')
    phone = StringField('User Phone', validators=[DataRequired()])
    # email = StringField('User Email', validators=[Email('email is not correct')])
    # avatar = FileField('User Avatar')
    role = SelectField('User Role', choices=[('3', 'کاربر عادی '), ('1', 'کاربر درجه 1'), ('2', 'کاربر درجه 2'), ('0', 'کاربر ادمین')])
    # password = PasswordField('User Password', validators=[DataRequired(), Length(min=8)])
    
    
