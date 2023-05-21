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
    
    
    
    
    
