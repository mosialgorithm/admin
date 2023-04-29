import os
import jdatetime
import re
from app import app
from flask import redirect, url_for, flash
from flask_login import current_user
from functools import wraps
from werkzeug.utils import secure_filename




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
            # flash("You need to be an admin to view this page.", 'danger')
            return redirect(url_for('admin.index'))
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
        folder = os.path.join(app.config['UPLOAD_DIR'], app_name, str(jdatetime.date.today()))
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
