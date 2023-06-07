import secrets
import string
from app import db 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime




 
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(150), nullable=True)
    username = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(50), default='')
    password = db.Column(db.String(200))
    phone = db.Column(db.String(200), unique=True)
    avatar = db.Column(db.String(100), default='img/avatar.png')
    role = db.Column(db.Integer(), default=2)
    active = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    last_login = db.Column(db.DateTime())
    last_ip = db.Column(db.String(150))
    address = db.Column(db.String(200))
    education = db.Column(db.String(200))
    skills = db.Column(db.String(200))
    about_me = db.Column(db.Text())
    user_agent = db.Column(db.String(200))
    deleted = db.Column(db.Boolean(), default=False)
    
    def __init__(self):
        self.username = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(20))
    
    def __repr__(self):
        return f'{self.id} --> {self.name}'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def user_following(self):
        from social.models import Following
        following = Following.query.filter_by(follow_from=self.id).all()
        return [user.follow_to for user in following]
    
    def user_followed(self):
        from social.models import Following
        followed = Following.query.filter_by(follow_to=self.id).all()
        return [user.follow_from for user in followed]
    
    
    
class UserLogs(db.Model):
    __tablename__ = 'users_logs'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))    
    created_at = db.Column(db.DateTime(), default=datetime.now())
    title = db.Column(db.String(200))
    model_name = db.Column(db.String(200))
    model_id = db.Column(db.Integer())
    
    def __repr__(self):
        return f'{self.title} at {self.created_at}'

    def save_log(self, user_id, title, obj):
        """saving event log by any user"""
        self.user_id = user_id
        self.title = title
        self.model_id = obj.id
        self.model_name = f'{type(obj)}'
        
        db.session.add(self)
        db.session.commit()
    
    
    
    
