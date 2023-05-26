from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from wtforms import StringField, SelectField, TextAreaField, FileField, BooleanField, DateTimeField, SelectFieldBase
from flask_ckeditor import CKEditorField
from .models import Category



class NewPostForm(FlaskForm):
    categories = Category.query.all()
    title = StringField('New Title')
    body = CKEditorField('News Body')
    image = FileField('News Image')
    choices = [(cat.title, cat.title) for cat in categories]
    category = SelectFieldBase('Category Select', choices=choices, id='news-category')
    draft = BooleanField('News Draft')
    # published_at = DateTimeField('News Publish')
    
    
class NewsEditForm(FlaskForm):
    body = TextAreaField('News Editted Body')
    image = FileField('News Editted Image')
    draft = BooleanField('News Editted Draft')
    # published_at = DateTimeField('News Editted Publish')
    
    
class CommentForm(FlaskForm):
    title = StringField('News Comment')
    