from jdatetime import datetime
from flask import redirect, render_template, request, url_for, session, flash
from app import db
from . import auth
from .forms import RegisterForm, LoginForm, SuperUserForm
from .models import User, UserLogs
from flask_login import login_user, logout_user, current_user



@auth.route('/register', methods=['POST', 'GET'])
def register():
    """register user"""
    login_form = LoginForm()
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            flash('form is validate', 'success')
            user = User()
            user.name = request.form.get('name')
            user.phone = request.form.get('phone')
            user.username = user.name + user.phone[-4:]
            if request.form.get('password') != request.form.get('confirm_password'):
                flash('your password and confirm password is not equal', 'danger')
            user.set_password(request.form.get('password'))
            user.last_login = datetime.now()
            user.last_ip = request.remote_addr
            try:
                db.session.add(user)
                db.session.commit()
                # ========= event logging =====================
                event = UserLogs()
                event.save_log(user.id,register.__doc__,user)
                # event.user_id = user.id
                # event.title = f'{register.__doc__}'
                # event.model_id = user.id
                # event.model_name = f'{type(user)}'
                # db.session.add(event)
                # db.session.commit()
                # ========= end of event logging ==============
                flash('your data is registered successfully', 'success')
                print('data is correct :)')
                return redirect(url_for('auth.login', form=login_form))
            except:
                db.session.rollback()
                flash('your data is not valid, please try again', 'danger')
                return redirect(url_for('auth.register'), form=form)
        else:
            flash('form is not validate', 'danger')
        
    return render_template('/auth/register.html', form=form)
 
 
@auth.route('/login', methods=['POST', 'GET'])
def login():
    """loggin user"""
    form = LoginForm()
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')
        user = User.query.filter_by(phone=phone).first()
        if not user:
            flash('this phone is not registered yet', 'warning')
            return redirect(url_for('auth.register'))
        if user.check_password(password) != True:
            flash('your password is incorrect', 'warning')    
            return redirect(url_for('auth.login'))
        # user.last_login = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        # user.last_login = datetime.today()
        user.last_ip = request.remote_addr
        user.user_agent = request.headers.get('User-Agent')
        db.session.add(user)
        db.session.commit()
        # ========= event logging ==============
        event = UserLogs()
        event.save_log(user.id,login.__doc__,user)
        # ========= end of event logging========
        login_user(user)
        flash('you are logged in successfully', 'success')
        return redirect(url_for('admin.index'))
            
    return render_template('/auth/login.html', form=form)


@auth.route('/logout')
def logout():
    """logout user"""
    flash('your are logged out', 'danger')
    # ========= event logging ==============
    event = UserLogs()
    event.save_log(current_user.id,logout.__doc__,current_user)
    # ========= end of event logging========
    logout_user()
    return redirect(url_for('auth.login'))
    
    
@auth.route('/createsuperuser', methods=['POST', 'GET'])
def superuser():
    """create superuser"""
    form = SuperUserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            usr = User.query.filter_by(name='root').first()
            if usr:
                if current_user:
                    return redirect(url_for('auth.logout'))
                return redirect(url_for('auth.login'))
            if request.form.get('password') == 'iamsuperuser@123456789!':
                user = User()
                user.name = 'root'
                user.set_password('iamsuperuser@123456789!')
                user.phone = '01234567890'
                user.role = 0
                user.username = user.name + user.phone[-4:]
                db.session.add(user)
                db.session.commit()
                # ========= event logging ==============
                event = UserLogs()
                event.save_log(current_user.id,superuser.__doc__,current_user)
                # ========= end of event logging========
                if current_user:
                    return redirect(url_for('auth.logout'))
                return redirect(url_for('auth.login'))
            
    return render_template('/auth/superuser.html', form=form)


