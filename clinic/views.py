from persiantools.jdatetime import JalaliDateTime, digits
from datetime import datetime
from flask import redirect, render_template, request, url_for, session, flash
from app import db
from . import clinic







@clinic.route('/')
def index():
    return render_template('clinic/index.html')