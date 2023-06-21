from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from wtforms import SubmitField, StringField, EmailField, SelectField, BooleanField, RadioField, SelectMultipleField




class MedicalFieldNewForm(FlaskForm):
    title = StringField('Medical Field Title')
    

class MedicalExpertsForm(FlaskForm):
    title = StringField('Medical Field Title')
    medical_field = SelectField('Select Medical Field')
    
    
class DoctorNewForm(FlaskForm):
    name = StringField("Doctor Name")
    phone = StringField("Doctor Phone")
    medical_system_number = StringField("Doctor Medical System Number")
    expert = SelectField("Doctor Experts")
    medical_field = SelectField("Doctor Medical Field")
    days = SelectMultipleField("Clinic Doctor Days", coerce=int)
    hours = SelectMultipleField("Clinic Doctor Hours", coerce=int)
    

class SecretaryNewForm(FlaskForm):
    name = StringField("Secretary Name")
    doctor_name = SelectField("Doctor Name")
    phone = StringField("Seretary Mobile Number")
    
    
class ClinicScheduleForm(FlaskForm):
    title = StringField("Schedule Title")
    day = RadioField("Schedule Day", 
                    choices=[(0,'شنبه'),(1,'یکشنبه'),(2,'دوشنبه'),(3,'سه شنبه'),(4,'چهارشنبه'),(5,'پنج شنبه'),(6,'جمعه')], default=0)
    am_pm = RadioField("Schedule Time", choices=[(0, "قبل از ظهر"), (1, "بعد از ظهر")], default=0)
    
    
class ScheduleForm(FlaskForm):
    schedules = SelectMultipleField("Schedule Items", coerce=int)
    

class VisitStepOneForm(FlaskForm):
    medical_fields = SelectField("Medical Fields List")
    
    
class VisitStepTwoForm(FlaskForm):
    clinic_experts = SelectField("Clinic Experts List")
    
    
class VisitStepThreeForm(FlaskForm):
    doctors_list = SelectField("Doctors List Visit")
    
    
class VisitStepFourForm(FlaskForm):
    doctor_days = RadioField("Schedule Doctor List")
    
    
class DoctorHoursForm(FlaskForm):
    hours = RadioField("Doctor Hours")
  

class EmptyForm(FlaskForm):
    btn = SubmitField()
    
    
class ScheduleHourNewForm(FlaskForm):
    hour = StringField("Schedule Hour Add")
    am_pm = RadioField("Am or Pm", choices=[(0, 'قبل از ظهر'), (1, 'بعد از ظهر')], default=0)
    
    
class ScheduleDayForm(FlaskForm):
    day = StringField("Schedule Day")
    
    
    
    