from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from flask_ckeditor import CKEditorField




class NewPostForm(FlaskForm):
    post = CKEditorField('New Social Post')
    
    
    
class PostCommentForm(FlaskForm):
    comment = StringField("Comment For Social Post")
    
class FollowingForm(FlaskForm):
    follow_btn = SubmitField("Following Button")
    