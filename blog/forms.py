from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from wtforms import StringField, SelectField, TextAreaField, FileField, BooleanField, DateTimeField, SelectFieldBase, SelectMultipleField
from flask_ckeditor import CKEditorField
from .models import Category



class NewPostForm(FlaskForm):
    # categories = Category.query.all() # I using @app.context_processor insted this
    title = StringField('New Title')
    body = CKEditorField('News Body')
    image = FileField('News Image')
    # choices = [(cat.title, cat.title) for cat in categories]
    # category = SelectMultipleField('Category Select', choices=choices, id='news-category')
    category = SelectMultipleField('Category Select',coerce=int, id='news-category')
    draft = BooleanField('News Draft')
    # published_at = DateTimeField('News Publish')
    
    
class NewsEditForm(FlaskForm):
    body = TextAreaField('News Editted Body')
    image = FileField('News Editted Image')
    category = SelectMultipleField('Category Select',coerce=int, id='news-category')
    draft = BooleanField('News Editted Draft')
    # published_at = DateTimeField('News Editted Publish')
    
    
class CommentForm(FlaskForm):
    title = StringField('News Comment')
    
    
class SerachNewsForm(FlaskForm):
    title = StringField("Sreach By Title")
    body = StringField("Search By Body")
    writer = StringField("Search By Writer")
    draft = SelectField("Search By Draft", choices=[(0,"منتشر شده"), (1,"پیش نویس") ])
    # datetime_from = DateTimeField("Search From DateTime")
    # datetime_to = DateTimeField("Search To DateTime")