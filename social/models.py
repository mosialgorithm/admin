from app import db 
from datetime import datetime
from auth.models import User




class Following(db.Model):
    __tablename__ = 'following'
    id = db.Column(db.Integer(), primary_key=True)
    follow_from = db.Column(db.Integer(), db.ForeignKey('users.id'))
    follow_to = db.Column(db.Integer(), db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f"{self.follow_from} follows {self.follow_to}"
    


class CommentLike(db.Model):
    __tablename__ = 'social_comment_likes'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    comment_id = db.Column(db.Integer(), db.ForeignKey('social_post_comment.id'))
    created_at = db.Column(db.DateTime(), default=datetime.now())
    
    def __repr__(self):
        return f'{self.user_id} comments on post {self.post_id}'



class PostLike(db.Model):
    __tablename__ = 'social_post_likes'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer(), db.ForeignKey('social_posts.id'))
    created_at = db.Column(db.DateTime(), default=datetime.now())
    
    def __repr__(self):
        return f'{self.user_id} likes {self.post_id}'
    
    

class PostComment(db.Model):
    __tablename__ = 'social_post_comment'
    id = db.Column(db.Integer(), primary_key=True)
    comment = db.Column(db.String(200))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer(), db.ForeignKey('social_posts.id'))
    created_at = db.Column(db.DateTime(), default=datetime.now())
    likes = db.relationship('CommentLike')
    
    def __repr__(self):
        return f'{self.user_id} comments {self.comment}'
    
    def writer(self, user_id):
        return User.query.get(user_id).name
    
    def writer_image(self, user_id):
        return User.query.get(user_id).avatar 
    
    def user_like_comment(self, user_id):
        return True if user_id in [user.user_id for user in self.likes] else False
    
    


class Post(db.Model):
    __tablename__ = 'social_posts'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    content = db.Column(db.Text(), nullable=False)
    image = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    updated_at = db.Column(db.DateTime(), default=datetime.now())
    likes = db.relationship('PostLike', backref='posts')
    comments = db.relationship('PostComment', backref='posts')
    # views = db.Column(db.Integer(), db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'{self.user_id} : {self.content[:20]}'
    
    def writer(self, user_id):
        return User.query.get(user_id).name
    
    def writer_image(self, user_id):
        return User.query.get(user_id).avatar 
    
    def user_like_post(self, user_id):
        for user in self.likes:
            if user_id == user.user_id:
                return True
        return False
        
    
        
    
    
    
    
    