import os
from flask import redirect, render_template, request, url_for, session, flash
from app import db, app
from . import admin
from flask_login import login_required, current_user
from utils import admin_required
from auth.models import User, UserLogs
from jdatetime import datetime, timedelta, date
from .forms import UserEditForm, UserAddForm
from werkzeug.utils import secure_filename
from utils import allow_extension, save_avatar
from sqlalchemy.exc import IntegrityError




@admin.route('/')
@login_required
def index():
    return render_template('admin/dashboard.html')


@admin.route('/users-list')
def users_list():
    page = request.args.get('page', default=1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=5)
    
    return render_template('admin/users/user-list.html', users=users)


@admin.route('/change-role/<int:user_id>/<int:user_role>')
def change_role(user_id, user_role):
    user = User.query.get_or_404(user_id)
    if user_role == 1:
        user.role = 2
    else:
        user.role = 1
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.users_list'))


@admin.route('/change-activity/<int:user_id>')
def change_activity(user_id):
    user = User.query.get_or_404(user_id)
    if user.active == 1:
        user.active = 0
    else:
        user.active = 1
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.users_list'))

   
@admin.route('/user-edit/<int:user_id>', methods=['POST', 'GET'])
def user_edit(user_id):
    form = UserEditForm()
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        if form.validate_on_submit():
            user.name = request.form.get('name')
            user.email = request.form.get('email')
            avatar = request.files.get('avatar')
            if avatar:
                filename = avatar.filename
                file_secure = secure_filename(filename)
                if not allow_extension(filename):
                    flash('your image file is not allowed', 'warning')
                    return redirect(url_for('admin.user_edit', user=user, form=form))
                today = datetime.today().strftime('%Y-%m-%d')
                folder = os.path.join(app.config['UPLOAD_DIR'], f'{user.name}', f'{today}')
                try:
                    os.makedirs(folder)
                except:
                    flash('your image file is not saved, properly', 'warning')
                
                file = os.path.join(folder, file_secure)
                avatar.save(file)
                user.avatar = f'uploads/{user.name}/{today}/{filename}'
                
            try:
                db.session.add(user)
                db.session.commit()
                flash(f'user {user.name} is editted successfully', 'success')
                return redirect(url_for('admin.users_list'))
            except IntegrityError as er:
                db.session.rollback()
                flash(f'Unfortunatly, user does not edit, error {er} is happened', 'warning')
                return redirect(url_for('admin.user_edit', user_id=user.id, form=form))
            except Exception as e:
                flash(f'error {e} is happened, please try again', 'warning')
                return redirect(url_for('admin.user_edit', user_id=user.id, form=form))
            
        flash('your form is not validate', 'danger')
        return redirect(url_for('admin.user_edit', user_id=user.id, form=form))
            
    return render_template('/admin/users/user-edit.html', user=user, form=form)


@admin.route('user-delete/<int:user_id>', methods=['GET'])
def user_delete(user_id):
    user = User.query.get_or_404(user_id)
    user.deleted = True
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.users_list'))


@admin.route('user-add', methods=['POST', 'GET'])
def user_add():
    form = UserAddForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User()
            user.name = request.form.get('name')
            user.phone = request.form.get('phone')
            user.role = int(request.form.get('role'))
            user.set_password('123456789')
            try:
                db.session.add(user)
                db.session.commit()
                flash(f'user {user.name} is created successfully', 'success')
            except IntegrityError():
                db.session.rollback()
                flash('Unfortunatly, user does not addedd', 'warning')
            finally:
                return redirect(url_for('admin.user_add', form=form))
            
        flash('your form is not validate', 'danger')
        return redirect(url_for('admin.user_add',form=form))
    
    return render_template('/admin/users/user-add.html', form=form)


@admin.route('user-profile', methods=['POST', 'GET'])
def user_profile():
    form = UserEditForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.name = request.form.get('name')
            current_user.username = request.form.get('username')
            # address
            province = request.form.get('address_province')
            city = request.form.get('address_city')
            street = request.form.get('address_street')
            house_number = request.form.get('address_house_number')
            current_user.address = f"{province}###{city}###{street}###{house_number}"
            #  education
            degree = request.form.get('education_degree')
            field = request.form.get('education_field')
            area = request.form.get('education_area')
            current_user.education = f"{degree}###{field}###{area}"
            #  skills
            skill_one = request.form.get('skill_one')
            skill_two = request.form.get('skill_two')
            skill_three = request.form.get('skill_three')
            skill_four = request.form.get('skill_four')
            skill_five = request.form.get('skill_five')
            current_user.skills = f"{skill_one}###{skill_two}###{skill_three}###{skill_four}###{skill_five}"
            #  about me
            current_user.about_me = request.form.get('about_me')
            #  upload image
            avatar = request.files.get('avatar')
            if avatar:
                if save_avatar(avatar, current_user):
                    pass
                else:
                    flash('your image file is not saved correctly', 'warning')
                    return redirect(url_for('admin.user_profile'))
            else:
                flash('you dont select image correctly, please try again', 'warning')    
            #  trying to saved data to database
            try:
                db.session.add(current_user)
                db.session.commit()
                flash('your data is saved successfully', 'success')
            except IntegrityError as er:
                db.session.rollback()
                flash(f'error {er} is happened, please try again', 'danger')
            except Exception as e:
                flash(f'error {e} is happened, please try again', 'warning')
            finally:
                return redirect(url_for('admin.user_profile', form=form))
            
    form.about_me.data = current_user.about_me
    return render_template('/admin/users/user-profile.html', form=form)


@admin.route('set-time/<int:user_id>')
def set_time(user_id):
    user = User.query.get_or_404(user_id)
    user.last_login = datetime.now()
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.users_list?page=3'))


@admin.route('users-info')
def users_info():
    online_users = '???????'
    users_today = User.query.filter(User.created_at >= datetime.today().strftime('%Y-%m-%d')).all()
    last_users = User.query.order_by(User.created_at.desc()).all()
    for user in last_users:
        pass
        # user.created_at = date(user.created_at.year, user.created_at.month, user.created_at.day).togregorian()

    return render_template('admin/users/user-info.html', users_today=users_today, last_users=last_users[-8:], date=date)


@admin.route('user-calendar')
def user_calendar():
    return render_template('/admin/users/user-calendar.html')


@admin.route('user-log')
def user_log():
    user_logs = UserLogs.query.filter_by(user_id=current_user.id).order_by(UserLogs.created_at).all()
    for log in user_logs:
        log.created_at = log.created_at.strftime('%Y-%m-%d')
    print('-*-'*50)
    for log in user_logs:
        print(log.title)
    print('-*-'*50)
    return render_template('admin/users/user-log.html', user_logs=user_logs)

