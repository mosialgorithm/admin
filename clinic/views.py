from persiantools.jdatetime import JalaliDateTime, digits
from datetime import datetime
from flask import redirect, render_template, request, url_for, session, flash
from app import db
from . import clinic
from .forms import (MedicalFieldNewForm, MedicalExpertsForm, DoctorNewForm, SecretaryNewForm, DoctorHoursForm,
                    ClinicScheduleForm, ScheduleForm, VisitStepOneForm,VisitStepTwoForm, VisitStepThreeForm, VisitStepFourForm,
                    EmptyForm, ScheduleHourNewForm, ScheduleDayForm)
from .models import MedicalField, Expert, Doctor, ScheduleHours, Visit, ScheduleDays
from auth.models import User
from flask_login import current_user






@clinic.route('/')
def index():
    return render_template('clinic/index.html')


@clinic.route('medical-field-new', methods=['POST', 'GET'])
def medical_field_new():
    form = MedicalFieldNewForm()
    all_fields = MedicalField.query.all()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('your form is not valid, please try again', 'danger')
            return redirect(url_for('clinic.medical_field_new', form=form, all_fields=all_fields))
        field = MedicalField()
        field.title = request.form.get('title')
        try:
            db.session.add(field)
            db.session.commit()
            flash('your new medical field is added successfully', 'success')
        except Exception as ex:
            db.session.rollback()
            flash(f'{ex}', 'danger')
        finally:
            return redirect(url_for('clinic.medical_field_new'))
            
    return render_template('clinic/medical-field-new.html', form=form, all_fields=all_fields)


@clinic.route('medical-field-edit/<int:field_id>', methods=['POST', 'GET'])
def medical_field_edit(field_id):
    form = MedicalFieldNewForm()
    # field = MedicalField.query.get_or_404(field_id)
    all_fields = MedicalField.query.all()
    for fld in all_fields:
        if fld.id == field_id:
            field = fld
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('your form is not valid, please try again', 'danger')
            return redirect(url_for('clinic.medical_field_new', form=form, field=field, all_fields=all_fields))
        field.title = request.form.get('title')
        try:
            db.session.add(field)
            db.session.commit()
            flash('your new medical field is added successfully', 'success')
        except Exception as ex:
            db.session.rollback()
            flash(f'{ex}', 'danger')
        finally:
            return redirect(url_for('clinic.medical_field_new', form=form, field=field, all_fields=all_fields))
            
    return render_template('clinic/medical-field-edit.html', form=form, field=field, all_fields=all_fields)


@clinic.route('mdecial-expert-new', methods=['POST', 'GET'])
def medical_expert_new():
    form = MedicalExpertsForm()
    all_fields = MedicalField.query.all()
    all_experts = Expert.query.order_by(Expert.medical_field_id).all()
    form.medical_field.choices = [(field.id, field.title) for field in all_fields]
    
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('your form is not valid, please try again', 'danger')
            return redirect(url_for('clinic.medical_expert_new', form=form, all_experts=all_experts))

        expert = Expert()
        expert.title = request.form.get('title')
        expert.medical_field_id = int(form.medical_field.data) 
        try:
            db.session.add(expert)
            db.session.commit()
            flash('your new expert is added successfully', 'success')
        except Exception as ex:
            db.session.rollback()
            flash(f'{ex}', 'warning')
        finally:
            return redirect(url_for('clinic.medical_expert_new', form=form, all_experts=all_experts))
        
    return render_template('clinic/medical-expert-new.html', form=form, all_experts=all_experts)
      
    
@clinic.route('mdecial-expert-edit/<int:expert_id>', methods=['POST', 'GET'])
def medical_expert_edit(expert_id):
    form = MedicalExpertsForm()
    all_fields = MedicalField.query.all()
    all_experts = Expert.query.order_by(Expert.medical_field_id).all()
    for exp in all_experts:
        if exp.id == expert_id:
            expert = exp
            
    form.medical_field.choices = [(field.id, field.title) for field in all_fields]
    
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('your form is not valid, please try again', 'danger')
            return redirect(url_for('clinic.medical_expert_edit', expert=expert, expert_id=expert_id, form=form, all_experts=all_experts))

        expert.title = request.form.get('title')
        expert.medical_field_id = int(form.medical_field.data) 
        try:
            db.session.add(expert)
            db.session.commit()
            flash('your new expert is added successfully', 'success')
        except Exception as ex:
            db.session.rollback()
            flash(f'{ex}', 'warning')
        finally:
            return redirect(url_for('clinic.medical_expert_new', form=form, all_experts=all_experts))
    
    
    form.medical_field.default = expert.medical_field_id
    form.process()
    
    return render_template('clinic/medical-expert-edit.html', expert=expert, expert_id=expert_id, form=form, all_experts=all_experts)


@clinic.route('doctor-new', methods=['POST', 'GET'])
def doctor_new():
    form = DoctorNewForm()
    experts = Expert.query.order_by(Expert.medical_field_id).all()
    fields = MedicalField.query.all()
    days = ScheduleDays.query.all()
    hours = ScheduleHours.query.all()
    # 
    form.expert.choices = [(expert.id, expert.title) for expert in experts]
    form.medical_field.choices = [(field.id, field.title) for field in fields]
    form.days.choices = [(day.id, day.day) for day in days]
    form.hours.choices = [(hour.id, hour.hour) for hour in hours]
    # 
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash(f'{form.errors}', 'danger')
            return redirect(url_for('clinic.doctor_new', form=form))
        # 
        name  = request.form.get('name')
        phone  = request.form.get('phone')
        medical_system_number  = request.form.get('medical_system_number')
        medical_field = int(form.medical_field.data)
        medical_expert = int(form.expert.data)
        days = [ScheduleDays.query.get(day) for day in form.days.data]   
        hours = [ScheduleHours.query.get(hour) for hour in form.hours.data]
        # 
        try:
            # ========= define new user =======================
            user = User()
            user.name = name
            user.phone = phone
            user.role = 11 # role of doctor is 11
            db.session.add(user)
            db.session.commit()
            # ========== define new doctor ====================
            doctor = Doctor()
            doctor.user_id = user.id
            doctor.medical_system_number = medical_system_number
            doctor.medical_field_id = medical_field
            doctor.expert_id = medical_expert
            doctor.days = days 
            doctor.hours = hours 
            db.session.add(doctor)
            db.session.commit()
            flash(f'your new doctor {user.name} is added successfully', 'success')
        except Exception as ex:
            flash(f'{ex}', 'danger')
        finally:
            return redirect(url_for('clinic.doctor_new', form=form))
        
    
    return render_template('clinic/doctor-new.html', form=form)


@clinic.route('doctor-edit/<int:doctor_id>', methods=['POST', 'GET'])
def doctor_edit(doctor_id):
    form = DoctorNewForm()
    experts = Expert.query.order_by(Expert.medical_field_id).all()
    fields = MedicalField.query.all()
    days = ScheduleDays.query.all()
    hours = ScheduleHours.query.all()
    doctor = Doctor.query.get_or_404(doctor_id)
    # 
    form.expert.choices = [(expert.id, expert.title) for expert in experts]
    form.medical_field.choices = [(field.id, field.title) for field in fields]
    form.days.choices = [(day.id, day.day) for day in days]
    form.hours.choices = [(hour.id, hour.hour) for hour in hours]
    # 
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('your form has error, please try again', 'danger')
            return redirect(url_for('clinic.doctor_new', form=form))
        # 
        name  = request.form.get('name')
        phone  = request.form.get('phone')
        medical_system_number  = request.form.get('medical_system_number')
        medical_field = int(form.medical_field.data)
        medical_expert = int(form.expert.data)
        days = [ScheduleDays.query.get(day) for day in form.days.data]   
        hours = [ScheduleHours.query.get(hour) for hour in form.hours.data]
        # 
        try:
            user = User.query.get(doctor.user_id)
            user.name = name
            user.phone = phone
            db.session.add(user)
            db.session.commit()
            # 
            doctor.medical_system_number = medical_system_number
            doctor.medical_field_id = medical_field
            doctor.expert_id = medical_expert
            doctor.days = days 
            doctor.hours = hours 
            db.session.add(doctor)
            db.session.commit()
            flash(f'your new doctor {user.name} is added successfully', 'success')
        except Exception as ex:
            flash(f'{ex}', 'danger')
        finally:
            return redirect(url_for('clinic.all_doctors_list'))
        
    form.expert.default = doctor.expert_id
    form.medical_field.default = doctor.medical_field_id
    form.days.default = [day.id for day in doctor.days]
    form.hours.default = [hour.id for hour in doctor.hours]
    form.process()
    
    return render_template('clinic/doctor-edit.html',doctor=doctor, form=form)


@clinic.route('all-doctors-list', methods=['POST', 'GET'])
def all_doctors_list():
    page = request.args.get('page', default=1, type=int)
    all_doctors = Doctor.query.order_by(Doctor.created_at.desc()).paginate(page=page, per_page=7)
    
    return render_template('clinic/doctors-list.html', all_doctors=all_doctors)


@clinic.route('secretary-new', methods=['POST', 'GET'])
def secretary_new():
    form = SecretaryNewForm()
    doctors = Doctor.query.all()
    form.doctor_name.choices = [(doc.id, doc.get_name()) for doc in doctors] 
    # 
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('your form is valid, please try again', 'danger')
            return redirect(url_for('clinic.secretary_new'))
        # 
        user = User()
        user.name = request.form.get('name')
        user.phone = request.form.get('phone')
        try:
            db.session.add(user)
            db.session.commit()
            secretary = Secretary()
            secretary.user_id = user.id
            secretary.doctor_id = form.doctor_name.data
            db.session.add(secretary)
            db.session.commit()
            flash('your new secretary is added successfully', 'success')
        except Exception as ex:
            flash(f"{ex}", 'danger')
        finally:
            return redirect(url_for('clinic.secretary_new', form=form))      
    
    return render_template('clinic/secretary-new.html', form=form)


@clinic.route('secretary-edit/<int:secretary_id>', methods=['POST', 'GET'])
def secretary_edit(secretary_id):
    form = SecretaryNewForm()
    doctors = Doctor.query.all()
    form.doctor_name.choices = [(doc.id, doc.get_name()) for doc in doctors] 
    all_secretary = Secretary.query.all()
    for sec in all_secretary:
        if sec.id == secretary_id:
            secretary = sec
    # 
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('your form is valid, please try again', 'danger')
            return redirect(url_for('clinic.secretary_new', secretary_id=secretary_id))
        # 
        user = User.query.get_or_404(secretary.user_id)
        user.name = request.form.get('name')
        user.phone = request.form.get('phone')
        try:
            db.session.add(user)
            db.session.commit()
            secretary.doctor_id = form.doctor_name.data
            db.session.add(secretary)
            db.session.commit()
            flash('your new secretary is added successfully', 'success')
        except Exception as ex:
            flash(f"{ex}", 'danger')
        finally:
            return redirect(url_for('clinic.secretary_edit', secretary_id=secretary_id, form=form))      
    
    form.doctor_name.default = secretary.doctor_id
    form.process()
    
    return render_template('clinic/secretary-edit.html',secretary=secretary, form=form)


@clinic.route('secretary-list', methods=['POST', 'GET'])
def secretary_list():
    page = request.args.get('page', default=1, type=int)
    all_secretary = Secretary.query.order_by(Secretary.created_at.desc()).paginate(page=page, per_page=7)
    
    return render_template('clinic/secretary-list.html', all_secretary=all_secretary)
    
    
@clinic.route('clinic-schedule', methods=['POST', 'GET'])
def clinic_schedule():
    form = ClinicScheduleForm()
    all_schedules = Schedule.query.order_by(Schedule.created_at.desc()).all()
    if request.method == 'POST':
        schedule = Schedule()
        schedule.title = request.form.get('title')
        schedule.day = request.form.get('day')
        schedule.am_pm = request.form.get('am_pm')
        try:
            db.session.add(schedule)
            db.session.commit()
            flash('your new schedule is added successfully', 'success')
        except Exception as ex:
            flash(f'{ex}', 'danger')
        finally:
            return redirect(url_for('clinic.clinic_schedule', form=form, all_schedules=all_schedules))
    
    return render_template('clinic/clinic-schedule.html', form=form, all_schedules=all_schedules)


@clinic.route('clinic-schedule-edit/<int:schedule_id>', methods=['POST', 'GET'])
def clinic_schedule_edit(schedule_id):
    form = ClinicScheduleForm()
    all_schedules = Schedule.query.order_by(Schedule.created_at.desc()).all()
    for schdl in all_schedules:
        if schdl.id == schedule_id:
            schedule = schdl
    
    if request.method == 'POST':
        schedule.title = request.form.get('title')
        schedule.day = request.form.get('day')
        schedule.am_pm = request.form.get('am_pm')
        # 
        try:
            db.session.add(schedule)
            db.session.commit()
            flash('your schedule is editted successfully', 'success')
        except Exception as ex:
            flash(f'{ex}', 'danger')
        finally:
            return redirect(url_for('clinic.clinic_schedule_edit', schedule_id=schedule_id, form=form, all_schedules=all_schedules))
    
    form.day.default = schedule.day
    form.am_pm.default = schedule.am_pm
    form.process()
    
    return render_template('clinic/clinic-schedule-edit.html', schedule=schedule, form=form, all_schedules=all_schedules)


@clinic.route('visit-step-one', methods=['POST', 'GET'])
def visit_step_one():
    form = VisitStepOneForm()
    all_fields = MedicalField.query.all()
    form.medical_fields.choices = [(field.id, field.title) for field in all_fields]
    # 
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash(f'{form.errors}', 'danger')
            return redirect(url_for('clinic.visit_step_one', form=form))
        # 
        session['field_id'] = form.medical_fields.data 
        return redirect(url_for('clinic.visit_step_two'))
    # 
    return render_template('clinic/visit-step-one.html', form=form)


@clinic.route('visit-step-two', methods=['POST', 'GET'])
def visit_step_two():
    if 'field_id' not in session.keys():
        flash('you must select one item','warning')
        return redirect(url_for('clinic.visit_step_one'))
    # 
    form = VisitStepTwoForm()
    user_field_id = session['field_id']
    all_experts = Expert.query.filter_by(medical_field_id=user_field_id).all()
    form.clinic_experts.choices = [(expert.id, expert.title) for expert in all_experts]
    # 
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash(f'{form.errors}', 'danger')
            return redirect(url_for('clinic.visit_step_two', form=form))
        # 
        session['expert_id'] = form.clinic_experts.data
        return redirect(url_for('clinic.visit_step_three'))
    
    return render_template('clinic/visit-step-two.html', form=form)


@clinic.route('visit-step-three', methods=['POST', 'GET'])
def visit_step_three():
    if 'expert_id' not in session.keys():
        flash('you must select one item','warning')
        return redirect(url_for('clinic.visit_step_two'))
    # 
    form = VisitStepThreeForm()
    user_field_id = session['field_id']
    user_expert_id = session['expert_id']
    all_doctors = Doctor.query.filter_by(medical_field_id=user_field_id, expert_id=user_expert_id).all()
    form.doctors_list.choices = [(doctor.id, doctor.get_name()) for doctor in all_doctors]
    # 
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash(f'{form.errors}', 'danger')
            return redirect(url_for('clinic.visit_step_three', form=form))
        # 
        doctor_id = int(form.doctors_list.data)
        session['doctor_id'] = doctor_id
        doctor_days = [day.id for day in Doctor.query.get(doctor_id).days]
        session['doctor_days'] = doctor_days
        print('doctor days : ', doctor_days)
        # 
        return redirect(url_for('clinic.visit_step_four'))
    
    return render_template('clinic/visit-step-three.html', form=form)


@clinic.route('visit-step-four', methods=['POST', 'GET'])
def visit_step_four():
    if 'doctor_days' not in session.keys():
        flash('you must select one item','warning')
        return redirect(url_for('clinic.visit_step_three'))
    # 
    form = VisitStepFourForm()
    doctor_days = session['doctor_days']
    doctor_all_days = [ScheduleDays.query.get(int(day)) for day in doctor_days]
    form.doctor_days.choices = [(day.id, day.day) for day in doctor_all_days]
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash(f'{form.errors}', 'danger')
            return redirect(url_for('clinic.visit_step_four', form=form))
        # 
        doctor_day = form.doctor_days.data 
        print('doctor day : ', doctor_day)
        session['doctor_day'] = doctor_day
        # 
        return redirect(url_for('clinic.visit_step_five'))
    
    return render_template('clinic/visit-step-four.html', form=form)
    


@clinic.route('visit-step-five', methods=['POST', 'GET'])
def visit_step_five():
    if 'doctor_day' not in session.keys():
        flash('you must select one item','warning')
        return redirect(url_for('clinic.visit_step_four'))
    # 
    doctor_day = int(session['doctor_day'])
    print('doctor day : ', doctor_day)
    # ===============================
    doctor_id = int(session['doctor_id'])
    print('doctor id : ', doctor_id)
    doctor = Doctor.query.get_or_404(doctor_id)
    print('doctor name : ', doctor.get_name())
    print('doctor id : ', doctor.id)
    # =====================================================================
    # all_hours = [ScheduleHours.query.get(hour.id) for  hour in doctor.hours]
    # print('all hours : ', all_hours)
    reserved_hours = [visit.schedule_hour_id for visit in Visit.query.filter_by(schedule_day_id=doctor_day, doctor_id=doctor_id).all()]
    print('reserved hours : ', reserved_hours)
    free_hours = []
    form = DoctorHoursForm()
    for hour in doctor.hours:
        if hour.id not in reserved_hours:
            free_hours.append(hour)
    form.hours.choices = [(hour.id, hour.hour) for hour in free_hours]
    # ====================================================================
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash(f'{form.errors}', 'danger')
            return redirect(url_for('clinic.visit_step_five'))
        # 
        hour = ScheduleHours.query.get(int(form.hours.data))
        # print('query is : ', hour.hour) 
        session['hour_id'] = hour.id 
        return redirect(url_for('clinic.visit_step_six'))
    
    return render_template('clinic/visit-step-five.html', form=form)


@clinic.route('visit-step-six', methods=['POST', 'GET'])
def visit_step_six():
    if 'hour_id' not in session.keys():
        return redirect(url_for('clinic.visit_step_one'))
    # print(session.keys())
    form = EmptyForm()
    field_id = int(session['field_id'])
    hour_id = int(session['hour_id'])
    doctor_day = int(session['doctor_day'])
    doctor_id = int(session['doctor_id'])
    # schedule_id = int(session['schedule_id'])
    # 
    doctor = Doctor.query.get_or_404(doctor_id)
    # schedule = Schedule.query.get_or_404(schedule_id)
    hour = ScheduleHours.query.get_or_404(hour_id)
    day = ScheduleDays.query.get_or_404(doctor_day).day
    # 
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash(f'{form.errors}', 'warning')
            return redirect(url_for('clinic.visit_step_six'))
        # 
        try:
            visit = Visit()
            visit.schedule_hour_id = hour_id
            visit.schedule_day_id = doctor_day
            visit.patient_id = current_user.id 
            visit.doctor_id = doctor_id
            visit.field_id = field_id
            # visit.schedule_id = schedule_id
            visit.set_title()
            # 
            db.session.add(visit)
            db.session.commit() 
        except Exception as ex:
            db.session.rollback()
            flash(f'{ex}', 'danger')
            return redirect(url_for('clinic.visit_step_six'))
        # ==================== clear session ===========================
        session.pop('doctor_id', None)
        session.pop('schedule_id', None)
        session.pop('doctor_shcedules', None)
        # session.pop('schedule_doctor', None)
        session.pop('expert_id', None)
        session.pop('hour_id', None)
        session.pop('doctor_id', None)
        session.pop('field_id', None)
        session.pop('session_id', None)
        # print(session.keys())
        # ==================== end of session clear ====================
        return redirect(url_for('clinic.my_visits'))   
    # end if 
    
    return render_template('clinic/visit-step-six.html', doctor_name=doctor.get_name(), 
                           hour=hour, day=day, form=form)



@clinic.route('my-visits')
def my_visits():
    all_visits = Visit.query.filter_by(patient_id=current_user.id).order_by(Visit.created_at.desc()).all()
    return render_template('clinic/my-visits.html', all_visits=all_visits)



@clinic.route('schedule-hour-new', methods=['POST', 'GET'])
def schedule_hour_new():
    form = ScheduleHourNewForm()
    all_hours = ScheduleHours.query.order_by(ScheduleHours.id.desc()).all()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash(f'{form.errors}', 'danger')
            return redirect(url_for('clinic.schedule_hour_new'))
        # 
        hour = request.form.get('hour')
        am_pm = int(request.form.get('am_pm'))
        new_hour = ScheduleHours()
        new_hour.hour = hour
        new_hour.am_pm = am_pm
        try:
            db.session.add(new_hour)
            db.session.commit()
            flash('new hour is added', 'success')
        except Exception as ex:
            flash(f'{ex}', 'danger')
        finally:
            return redirect(url_for('clinic.schedule_hour_new'))
        
    return render_template('clinic/schedule-hour-new.html', form=form, all_hours=all_hours)


@clinic.route('schedule-hour-edit/<int:hour_id>', methods=['POST', 'GET'])
def schedule_hour_edit(hour_id):
    form = ScheduleHourNewForm()
    all_hours = ScheduleHours.query.order_by(ScheduleHours.id.desc()).all()
    for hrs in all_hours:
        if hrs.id == hour_id:
            edit_hour = hrs
    # 
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash(f'{form.errors}', 'danger')
            return redirect(url_for('clinic.schedule_hour_edit', hour_id=hour_id))
        # 
        hour = request.form.get('hour')
        am_pm = int(request.form.get('am_pm'))
        edit_hour.hour = hour
        edit_hour.am_pm = am_pm
        try:
            db.session.add(edit_hour)
            db.session.commit()
            flash('new hour is added', 'success')
        except Exception as ex:
            flash(f'{ex}', 'danger')
        finally:
            return redirect(url_for('clinic.schedule_hour_new'))
    
    form.am_pm.default = int(edit_hour.am_pm)
    form.process()
    
    return render_template('clinic/schedule-hour-edit.html', form=form, all_hours=all_hours, edit_hour=edit_hour)


@clinic.route('schedule-hour-delete/<int:hour_id>', methods=['POST', 'GET'])
def schedule_hour_delete(hour_id):
    hour = ScheduleHours.query.get_or_404(hour_id)
    db.session.delete(hour)
    db.session.commit()
    return redirect(url_for('clinic.schedule_hour_new'))



@clinic.route('schedule-day-new', methods=['POST', 'GET'])
def schedule_day_new():
    form = ScheduleDayForm()
    all_days = ScheduleDays.query.order_by(ScheduleDays.id.desc()).all()
    if request.method == 'POST':
        day = request.form.get('day')
        new_day = ScheduleDays()
        new_day.day = day
        db.session.add(new_day)
        db.session.commit()
        flash('new day is added', 'success')
        return redirect(url_for('clinic.schedule_day_new'))
    
    return render_template('clinic/schedule-day-new.html', form=form, all_days=all_days)



@clinic.route('schedule-day-edit/<int:day_id>', methods=['POST', 'GET'])
def schedule_day_edit(day_id):
    form = ScheduleDayForm()
    all_days = ScheduleDays.query.order_by(ScheduleDays.id.desc()).all()
    for dy in all_days:
        if dy.id == day_id:
            day = dy
    # 
    if request.method == 'POST':
        day = request.form.get('day')
        new_day = ScheduleDays()
        new_day.day = day
        db.session.add(new_day)
        db.session.commit()
        flash('new day is editted', 'success')
        return redirect(url_for('clinic.schedule_day_new'))
    
    return render_template('clinic/schedule-day-edit.html', form=form, day=day, all_days=all_days)

    
@clinic.route('schedule-day-delete/<int:day_id>')
def schedule_day_delete(day_id):
    day = ScheduleDays.query.get(day_id)
    db.session.delete(day)
    db.session.commit()
    
    return redirect(url_for('clinic.schedule_day_new'))
    