doctors_schedules = db.Table('clinic_doctors_schedules', db.metadata,
    db.Column('doctor_id', db.Integer(), db.ForeignKey('clinic_doctors.id' , ondelete='cascade')),
    db.Column('schedule_id', db.Integer(), db.ForeignKey('clinic_schedules.id' , ondelete='cascade'))
)


doctors_days = db.Table('clinic_doctors_days', db.metadata,
    db.Column('doctor_id', db.Integer(), db.ForeignKey('clinic_doctors.id' , ondelete='cascade')),
    db.Column('day_id', db.Integer(), db.ForeignKey('clinic_schedule_days.id' , ondelete='cascade'))
)


doctors_hours = db.Table('clinic_doctors_hours', db.metadata,
    db.Column('doctor_id', db.Integer(), db.ForeignKey('clinic_doctors.id' , ondelete='cascade')),
    db.Column('hour_id', db.Integer(), db.ForeignKey('clinic_schedule_hours.id' , ondelete='cascade'))
)


class Doctor(db.Model):
    __tablename__ = 'clinic_doctors'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    expert_id = db.Column(db.Integer(), db.ForeignKey('clinic_experts.id'))
    medical_field_id = db.Column(db.Integer(), db.ForeignKey('clinic_medical_fields.id'))
    medical_system_number = db.Column(db.String(200))
    created_at = db.Column(db.DateTime(), default=datetime.now())
    days = db.relationship('ScheduleDays', secondary=doctors_days, back_populates='doctors')
    hours = db.relationship('ScheduleHours', secondary=doctors_hours, back_populates='doctors')
    
    def __repr__(self):
        return f'{self.user_id}'
    
    def get_avatar(self):
        return User.query.get(self.user_id).avatar
    
    def get_name(self):
        return User.query.get(self.user_id).name
    
    def get_phone(self):
        return User.query.get(self.user_id).phone
    
    def get_expert(self):
        return Expert.query.get(self.expert_id).title
    
    def get_medical_field(self):
        return MedicalField.query.get(self.medical_field_id).title
 
 

class ScheduleHours(db.Model):
    __tablename__ = 'clinic_schedule_hours'
    id = db.Column(db.Integer(), primary_key=True)
    hour = db.Column(db.String(50))
    am_pm = db.Column(db.Boolean(), default=0)
    doctor_id = db.Column(db.Integer(), db.ForeignKey('clinic_doctors.id'))
    
    def __repr__(self):
        return self.hour



class ScheduleDays(db.Model):
    __tablename__ = 'clinic_schedule_days'
    id = db.Column(db.Integer(), primary_key=True)
    day = db.Column(db.String(50))
    doctor_id = db.Column(db.Integer(), db.ForeignKey('clinic_doctors.id'))
    
    def __repr__(self):
        return self.day
    
    

class Visit(db.Model):
    __tablename__ = 'clinic_visits'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(200))
    schedule_hour_id = db.Column(db.Integer(), db.ForeignKey('clinic_schedule_hours.id'))
    schedule_day_id = db.Column(db.Integer(), db.ForeignKey('clinic_schedule_days.id'))
    patient_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    doctor_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    field_id = db.Column(db.Integer(), db.ForeignKey('clinic_medical_fields.id'))
    created_at = db.Column(db.DateTime(), default=datetime.now())
    status = db.Column(db.Boolean(), default=False)
    
    def __repr__(self):
        return self.title
    
    def set_title(self):
        doctor = Doctor.query.get_or_404(self.doctor_id).get_name()
        patient = User.query.get_or_404(self.patient_id).name
        self.title = f'دکتر {doctor} - بیمار‌ : {patient} - {datetime.now().strftime("%y/%m/%d %H:%M")}'
    
    def patient_name(self):
        return User.query.get(self.patient_id).name
    
    def doctor_name(self):
        return Doctor.query.get(self.doctor_id).get_name()
    
    def schedule_hour(self):
        return ScheduleHours.query.get(self.schedule_hour_id).hour
    
    def schedule_day(self):
        return ScheduleDays.query.get(self.schedule_day_id).day
    
    
    
    
    