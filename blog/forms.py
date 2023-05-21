from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from wtforms import StringField, SelectField, TextAreaField, FileField, BooleanField, DateTimeField


class NewPostForm(FlaskForm):
    title = StringField('New Title')
    body = TextAreaField('News Body')
    image = FileField('News Image')
    draft = BooleanField('News Draft')
    # published_at = DateTimeField('News Publish')
    
    
class NewsEditForm(FlaskForm):
    body = TextAreaField('News Editted Body')
    image = FileField('News Editted Image')
    draft = BooleanField('News Editted Draft')
    # published_at = DateTimeField('News Editted Publish')
    
    
class CommentForm(FlaskForm):
    title = StringField('News Comment')
    