from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, RadioField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired



class GradeForm(FlaskForm):
    title = StringField('Grade Title', validators=[DataRequired('عنوان خود را انتخاب نکرده اید')])



class FieldNewForm(FlaskForm):
    title = StringField('Field Title', validators=[DataRequired('عنوان خود را انتخاب نکرده اید')])
    fanny_type = RadioField('Field Fanny Type' , choices=[(0, 'کاردانش'), (1, 'فنی و حرفه ای')], default=1)
    grades = SelectMultipleField('Field Grades', coerce=int, validators=[DataRequired('حداقل یک گزینه را انتخاب کنید')])
  
    
    
class CourseForm(FlaskForm):
    title = StringField('Class Room Title', validators=[DataRequired('عنوان خود را انتخاب نکرده اید')])
    grade = SelectField('Class Room Grade', validators=[DataRequired()])
    field = SelectField('Class Room Field', validators=[DataRequired()])
    teacher = SelectField('Class Room Teacher', validators=[DataRequired()])
    course_credit = SelectField('Class Room Course Credit', validators=[DataRequired()])
 
    

class ClassRoomForm(FlaskForm):
    title = StringField('Class Room Title', validators=[DataRequired('عنوان خود را انتخاب نکرده اید')])
    grade = SelectField('Class Room Grade', validators=[DataRequired()])
    field = SelectField('Class Room Field', validators=[DataRequired()])
    students = SelectMultipleField('Class Room Students', coerce=int, validators=[DataRequired('حداقل یک گزینه را انتخاب کنید')])
    # courses = SelectMultipleField('Class Room Courses', coerce=int, validators=[DataRequired('حداقل یک گزینه را انتخاب کنید')])
    academic_year = SelectField('Class Academic Year')
    


class QuestionForm(FlaskForm):
    title = TextAreaField('Exam Title', validators=[DataRequired('عنوان خود را انتخاب نکرده اید')])
    option_1 = StringField('Option 1 Title', validators=[DataRequired('عنوان خود را انتخاب نکرده اید')])
    option_2 = StringField('Option 2 Title', validators=[DataRequired('عنوان خود را انتخاب نکرده اید')])
    option_3 = StringField('Option 3 Title', validators=[DataRequired('عنوان خود را انتخاب نکرده اید')])
    option_4 = StringField('Option 4 Title', validators=[DataRequired('عنوان خود را انتخاب نکرده اید')])
    correct_option = SelectField('Correct Option', choices=[(1, 'گزینه اول'), (2, 'گزینه دوم'), (3, 'گزینه سوم'), (4, 'گزینه چهارم')])


class ExamForm(FlaskForm):
    title = StringField('Exam Title', validators=[DataRequired('عنوان خود را انتخاب نکرده اید')])
    course = SelectField('Exam Class Room', validators=[DataRequired()])
    exam_time_long = SelectField('Exam Time Long', choices=[(1, 'یک دقیقه'), (30, '30 دقیقه'), (60, 'یک ساعت'), (90, 'یک ساعت و نیم'),
                                          (120, 'دو ساعت'), (150, 'دو ساعت و نیم'), (180, 'سه ساعت')] , validators=[DataRequired()])
    # exam_date = DateTimeLocalField('Exam Date')
    exam_time_start = SelectField('Exam Time Starting', choices=[('8','8 صبح'), ('9','9 صبح'), ('10','10 صبح'),
                                                                 ('11','11 صبح'), ('12','12 ظهر'), ('13','یک بعدازظهر'),])
    modular_semester = SelectField(choices=[(1,'پودمان اول'), 
                                            (2,'پودمان دوم'), (3,'پودمان سوم'),
                                            (4,'پودمان چهارم'), (5, 'پودمان پنجم'),
                                            (6, 'ترم اول'), (7, 'ترم دوم'), (8, 'شهریور')])
    
    

class ExamTestForm(FlaskForm):
    btn = SubmitField('ثبت تغییرات')
    
    
class AcademicYearForm(FlaskForm):
    title = StringField('Academic Year', validators=[DataRequired()])
    
    
    
class EnrollForm(FlaskForm):
    student_name = StringField("Student Name", validators=[DataRequired()])
    student_phone = StringField("Student Phone Numner", validators=[DataRequired()])
    grade = SelectField("Student Grade")
    field = SelectField("Student Field")
    academic_year = SelectField("Academic Year")
    
    
class GroupEnrollForm(FlaskForm):
    studens_file = FileField('Group Student Enroll', validators=[FileRequired(), FileAllowed(['pdf'], 'PDF File Only!')])