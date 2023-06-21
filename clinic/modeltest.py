from app import db 
from auth.models import User
from datetime import datetime
from sqlalchemy import orm



class Calendar(db.Model):
    __tablename__ = 'clinic_calendar'
    id = db.Column(db.Integer(), primary_key=True)
    year = db.Column(db.String('200'), nullable=False, unique=True)
    month = db.Column(db.Integer(), db.CheckConstraint('month > 0 AND month < 13'))
    week = db.Column(db.Integer(), db.CheckConstraint('month > 0 AND month < 53'))
    day = db.Column(db.Integer(), db.CheckConstraint('day > 0 AND day < 366'))
    hour = db.Column(db.Integer(), db.CheckConstraint('hour > 0 AND hour < 25'))
    
    
    @orm.validates('month')
    def validate_month(self, key, value):
        if not 0 < value < 13:
            raise ValueError(f'Invalid month {value}')
        return value
    
    @orm.validates('day')
    def validate_day(self, key, value):
        if not 0 < value < 366:
            raise ValueError(f'Invalid day {value}')
        return value
    
    @orm.validates('week')
    def validate_week(self, key, value):
        if not 0 < value < 53:
            raise ValueError(f'Invalid week {value}')
        return value
    
    @orm.validates('hour')
    def validate_hour(self, key, value):
        if not 0 < value < 25:
            raise ValueError(f'Invalid hour {value}')
        return value