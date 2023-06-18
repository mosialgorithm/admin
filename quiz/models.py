from app import db
from datetime import datetime
from auth.models import User

grades_fields = db.Table('grades_fields', db.metadata,
    db.Column('grade_id', db.Integer, db.ForeignKey('grades.id', ondelete='cascade')),
    db.Column('field_id', db.Integer, db.ForeignKey('fields.id', ondelete='cascade'))
)


class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    fields = db.relationship('Field', secondary=grades_fields, back_populates='grades')
    created_at = db.Column(db.DateTime(), default=datetime.now())
    
    def __repr__(self):
        return f'{self.id} : {self.title}'
    
       
   
class Field(db.Model):
    __tablename__ = 'fields'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    fanni = db.Column(db.Boolean(), default=True)
    grades = db.relationship('Grade', secondary=grades_fields, back_populates='fields')
    created_at = db.Column(db.DateTime(), default=datetime.now())
    
    def __repr__(self):
        return f'{self.id} : {self.title}'



class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    grade = db.Column(db.Integer(), db.ForeignKey('grades.id'))
    field = db.Column(db.Integer(), db.ForeignKey('fields.id'))
    teacher = db.Column(db.Integer(), db.ForeignKey('users.id'))
    classroom = db.Column(db.Integer(), db.ForeignKey('classrooms.id'))
    course_credit = db.Column(db.Integer())
    created_at = db.Column(db.DateTime(), default=datetime.now())
    
    def __repr__(self):
        return f'{self.id} : {self.title}'
    
    def teacher_name(self):
        return User.query.get(self.teacher).name
    
    

class ExamStudents(db.Model):
    __tablename__ = 'exam_students'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    exam_id = db.Column(db.Integer(), db.ForeignKey('exams.id'))
    score = db.Column(db.String(10))
    created_at = db.Column(db.DateTime(), default=datetime.now())
    
    def __repr__(self):
        return f'student by ID {self.user_id} Exams {self.exam_id} by score : {self.score}'
    
    def exam_title(self):
        return Exam.query.get(self.exam_id).title
    
    def exam_type(self):
        return Exam.query.get(self.exam_id).exam_type()



class Exam(db.Model):
    __tablename__ = 'exams'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    # classroom = db.Column(db.Integer(), db.ForeignKey('classrooms.id'))
    writer = db.Column(db.Integer(), db.ForeignKey('users.id'))
    course = db.Column(db.Integer(), db.ForeignKey('courses.id'))
    created_at = db.Column(db.DateTime(), default=datetime.now())
    exam_time_long = db.Column(db.Integer())
    exam_date = db.Column(db.DateTime())
    exam_time_start = db.Column(db.String(100))
    modular_semester = db.Column(db.Integer())
    questions = db.relationship('Question')
    confirm = db.Column(db.Boolean(), default=False)
    
    def __repr__(self):
        return f'{self.id} : {self.title}'
    
    def get_writer(self, user_id):
        return User.query.get(user_id).name
    
    def get_course(self, course_id):
        return Course.query.get(course_id).title
    
    def exam_type(self):
        if self.modular_semester == 1:
            return "پودمان اول"
        elif self.modular_semester == 2:
            return "پودمان دوم"
        elif self.modular_semester == 3:
            return "پودمان سوم"
        elif self.modular_semester == 4:
            return "پودمان چهارم"
        elif self.modular_semester == 5:
            return "پودمان پنجم"
        elif self.modular_semester == 6:
            return "ترم اول"
        elif self.modular_semester == 7:
            return "ترم دوم"
        elif self.modular_semester == 8:
            return "ترم شهریور"
        elif self.modular_semester == 9:
            return "تجدیدی ها"

 
 
class AcademicYear(db.Model):
    __tablename__ = "academic_years"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    
    def __repr__(self):
        return self.title
     
        

class ClassRoom(db.Model):
    __tablename__ = 'classrooms'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    academic_year = db.Column(db.String(100))
    grade = db.Column(db.Integer(), db.ForeignKey('grades.id'))
    field = db.Column(db.Integer(), db.ForeignKey('fields.id'))
    academic_year = db.Column(db.Integer(), db.ForeignKey('academic_years.id'))
    # students = db.relationship('User', secondary=students_classrooms, back_populates='classrooms')
    # teacher = db.Column(db.Integer(), db.ForeignKey('users.id'))
    students = db.relationship('User')
    courses = db.relationship('Course')
    created_at = db.Column(db.DateTime(), default=datetime.now())
    # exams = db.relationship('Exam')
    
    def __repr__(self):
        return f'{self.id} : {self.title}'
    
    def grade_title(self):
        return Grade.query.get(self.grade).title
    
    def field_title(self):
        return Field.query.get(self.field).title
    
    def academic_year_title(self):
        return AcademicYear.query.get(self.academic_year).title
    
    # def teacher_name(self):
    #     return User.query.get(self.teacher).name
    
    

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=True)
    option_1 = db.Column(db.String(100), nullable=False)
    option_2 = db.Column(db.String(100), nullable=False)
    option_3 = db.Column(db.String(100), nullable=False)
    option_4 = db.Column(db.String(100), nullable=False)
    correct_option = db.Column(db.Integer())
    exam = db.Column(db.Integer(), db.ForeignKey('exams.id'))
    
    def __repr__(self):
        return self.title[:20]
    


class EnrollStudent(db.Model):
    __tablename__ = "enrol_students"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    # class_id = db.Column(db.Integer(), db.ForeignKey('classrooms.id'))
    grade_id = db.Column(db.Integer(), db.ForeignKey('grades.id'))
    field_id = db.Column(db.Integer(), db.ForeignKey('fields.id'))
    academic_year_id = db.Column(db.Integer(), db.ForeignKey('academic_years.id'))
    created_at = db.Column(db.DateTime(), default=datetime.now())
    
    def __repr__(self):
        return f'user : {self.user_id} in class : {self.class_id}'
    
    def student_name(self):
        return User.query.get_or_404(self.user_id).name
    
    def grade_title(self):
        return Grade.query.get_or_404(self.grade_id).title
    
    def field_title(self):
        return Field.query.get_or_404(self.field_id).title
    
    def academic_year_title(self):
        return AcademicYear.query.get_or_404(self.academic_year_id).title
    



class EnrollGroupStudents(db.Model):
    __tablename__ = 'students_group_enrolls'
    id = db.Column(db.Integer(), primary_key=True)
    filepath = db.Column(db.String(200))
    
    def __repr__(self):
        return self.filepath




# ============================================================================================================
# students_classrooms = db.Table('students_classrooms', db.metadata,
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='cascade')),
#     db.Column('classroom_id', db.Integer, db.ForeignKey('classrooms.id', ondelete='cascade'))
# )
    

    


