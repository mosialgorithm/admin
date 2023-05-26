from app import db 
from auth.models import User
from datetime import datetime
from slugify import slugify


class NewsLike(db.Model):
    __tablename__ ='newslikes'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    news_id = db.Column(db.Integer(), db.ForeignKey('news.id'))
    created_at = db.Column(db.DateTime(), default=datetime.now())
    
    def __repr__(self):
        return f'user id : {self.user_id} & news id : {self.news_id}'
    
    def user_name(self):
        return User.query.get(self.user_id).name()



class Reply(db.Model):
    __tablename__ = 'replies'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(500))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    news_id = db.Column(db.Integer(), db.ForeignKey('news.id'))
    comment_id = db.Column(db.Integer(), db.ForeignKey('comments.id'))
    created_at = db.Column(db.DateTime(), default=datetime.now())
    show = db.Column(db.Boolean(), default=False)
    
    def __repr__(self):
        return self.title[:20]
    
    def writer(self, user_id):
        return User.query.get(user_id).name
    
    def writer_image(self, user_id):
        return User.query.get(user_id).avatar
    
    def news_title(self,news_id):
        return News.query.get(news_id).title
    
    def comment_title(self, comment_id):
        return Comment.query.get(comment_id).title
    


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(500))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    news_id = db.Column(db.Integer(), db.ForeignKey('news.id'))
    created_at = db.Column(db.DateTime(), default=datetime.now())
    replies = db.relationship('Reply', backref='comment')
    show = db.Column(db.Boolean(), default=False)
    
    def __repr__(self):
        return self.title[:20]
    
    def writer(self, user_id):
        return User.query.get(user_id).name
    
    def writer_image(self, user_id):
        return User.query.get(user_id).avatar
    
    def news_title(self, news_id):
        return News.query.get(news_id).title
    
    
news_category = db.Table('news_category',
                         db.Column('news_id', db.Integer, db.ForeignKey('news.id')),
                         db.Column('category_id', db.Integer, db.ForeignKey('categories.id')))
    
    


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(150), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    image = db.Column(db.String(100), default='/img/photo2.png')
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
    # user = db.relationship("User", backref=db.backref("users", uselist=False))
    draft = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    updated_at = db.Column(db.DateTime(), default=datetime.now())
    published_at = db.Column(db.DateTime(), default=datetime.now())
    views = db.Column(db.Integer(), default=0)
    users_like = db.relationship('NewsLike', backref='news')
    comments = db.relationship('Comment', backref='news')
    categories = db.relationship('Category', secondary=news_category, backref='news')
    
    def __repr__(self):
        return f'{self.id} --> {self.title}'
    
    def writer(self, user_id):
        return User.query.get(user_id).name
    
    def writer_image(self, user_id):
        return User.query.get(user_id).avatar
    
    @staticmethod
    def generate_slug(cls, value, oldvalue, initiator):
        if value and (not cls.slug and value != oldvalue):
            cls.slug = slugify(value, allow_unicode=True)
    



class Category(db.Model):
    __tablename__  = 'categories'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    
    def __repr__(self):
        return self.title
    


db.event.listen(News.title, 'set', News.generate_slug, retval=False)
