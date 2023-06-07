from persiantools.jdatetime import JalaliDateTime, digits
from datetime import datetime
from flask import redirect, render_template, request, url_for, session, flash
from app import db
from . import quiz




@quiz.route('/')
def index():
    return 'online quiz is started'