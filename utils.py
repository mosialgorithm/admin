import os
from jdatetime import datetime, date
import re
from app import app
from flask import redirect, url_for, flash
from flask_login import current_user
from functools import wraps
from werkzeug.utils import secure_filename
from persiantools.jdatetime import JalaliDateTime



#=================================== CREATE EMAIL ADMIN VALID ===============================================
# regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
regex = re.compile(r"admin@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

def isvalid_email_admin(email):
    return False if re.fullmatch(regex, email) else True

#========================================== END =============================================================



#====================================== CREATE ADMIN REQUIRED ===============================================
def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role == 0:
            return f(*args, **kwargs)
        else:
            flash("You need to be an admin to view this page.", 'danger')
            return redirect(url_for('auth.logout'))
    return wrap

#========================================== END =============================================================


def allow_extension(filename):
    ext = filename[-3:]
    extension = {'png', 'jpg'}
    if not ext in extension:
        return False
    return True


#====================================== UPLOADING IMAGE ===============================================

def save_image(image, app_name, url, form):
    if image.filename == '':
        flash('you not select a image properly, please try again', 'warning')
        return redirect(url_for(url, form=form))
    if image:
        print('image is -----> ', image)
        filename = image.filename
        file_secure = secure_filename(filename)
        if not allow_extension(file_secure):
            flash('this extension for image file is not allowed', 'warning')
            return redirect(url_for(url, form=form))
        folder = os.path.join(app.config['UPLOAD_DIR'], app_name, str(date.today()))
        print('folder is -----> ', folder)
        try:
            os.makedirs(folder)
        except Exception as e:
            # flash(f'error {e} is happened, please try again', 'warning')
            pass
        finally:
            file = os.path.join(folder, file_secure)
            print('file is ----> ', file)
            image.save(file)
            flash('your image is uploaded successfully', 'success')
            return True
    return False


def save_avatar(avatar, obj):
    if avatar:
        filename = avatar.filename
        file_secure = secure_filename(filename)
        if not allow_extension(filename):
            flash('your image file is not allowed', 'warning')
            return False
        folder = os.path.join(app.config['UPLOAD_DIR'], f'{current_user.id}')
        try:
            os.makedirs(folder)
        except FileExistsError:
            pass
        # os.makedirs(folder, exist_ok=True)
        file = os.path.join(folder, file_secure)
        avatar.save(file)
        obj.avatar = f'uploads/{current_user.id}/{filename}'
        return True
    return False



def jdt_from_pdp(strdt):
    publish_date = strdt.split(' ')[0]
    publish_time = strdt.split(' ')[1]
    year = int(publish_date.split('-')[0])
    month = int(publish_date.split('-')[1])
    day = int(publish_date.split('-')[2])
    hour = int(publish_time.split(':')[0])
    minute = int(publish_time.split(':')[1])
    second = int(publish_time.split(':')[2])
    fa_datetime = datetime(year,month,day,hour,minute,second, locale='fa_IR')
    return fa_datetime


def jdt_to_gregorian(strdt):
    date = strdt.split(' ')[0] if strdt != None else ''
    try:
        time = strdt.split(' ')[1] if strdt != (None or '') else ''
    except:
        time = ''
    year = int(date.split('-')[0])
    month = int(date.split('-')[1])
    day = int(date.split('-')[2])
    if time != '':
        hour = int(time.split(':')[0])
        minute = int(time.split(':')[1])
        second = int(time.split(':')[2])
        en_datetime = JalaliDateTime(year,month,day,hour,minute,second).to_gregorian()
    else:
        en_datetime = JalaliDateTime(year,month,day).to_gregorian()
    return en_datetime