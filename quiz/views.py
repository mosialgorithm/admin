from datetime import datetime
from flask import redirect, render_template, request, url_for, session, flash
from app import db
from . import quiz
from .models import Field, Grade, Course, ClassRoom, Exam, Question, ExamStudents, AcademicYear, EnrollStudent
from .forms import FieldNewForm, GradeForm, CourseForm, ClassRoomForm, ExamForm, QuestionForm, ExamTestForm, AcademicYearForm, EnrollForm
from sqlalchemy.exc import IntegrityError
from auth.models import User
from flask_login import current_user
from utils import jdt_to_gregorian
from persiantools.jdatetime import JalaliDateTime




@quiz.route('/')
def index():

    return render_template('quiz/index.html')


@quiz.route('grade-new', methods=['POST', 'GET'])
def grade_new():
    form = GradeForm()
    grades = Grade.query.all()
    if request.method == 'POST' and form.validate_on_submit():
        title = request.form.get('title')
        grade = Grade()
        grade.title = title
        try:
            db.session.add(grade)
            db.session.commit()
            flash('your new grade is added successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'error {e} is happened', 'danger')
        finally:
            return redirect(url_for('quiz.grade_new', form=form, grades=grades))
    return render_template('quiz/grade-new.html', form=form, grades=grades)


@quiz.route('grade-edit/<int:grade_id>', methods=['POST', 'GET'])
def grade_edit(grade_id):
    form = GradeForm()
    grades = Grade.query.all()
    grade = Grade.query.filter_by(id=grade_id).first()
    if request.method == 'POST' and form.validate_on_submit():
        title = request.form.get('title')
        grade.title = title
        db.session.add(grade)
        db.session.commit()
        return redirect(url_for('quiz.grade_edit', grade_id=grade.id, form=form, grades=grades, grade=grade))
    return render_template('quiz/grade-edit.html', form=form, grades=grades, grade=grade)


@quiz.route('grade-delete/<int:grade_id>', methods=['POST'])
def grade_delete(grade_id):
    form = GradeForm()
    grades = Grade.query.all()
    grade = Grade.query.get_or_404(grade_id)
    db.session.delete(grade)
    db.session.commit()
    return redirect(url_for('quiz.grade_new', form=form, grades=grades))


@quiz.route('field-new', methods=['POST', 'GET'])
def field_new():
    form = FieldNewForm()
    fields_fanni = Field.query.filter_by(fanni=1).all()
    fields_kar = Field.query.filter_by(fanni=0).all()
    form.grades.choices = [(grade.id, grade.title) for grade in Grade.query.all()]
    
    if request.method == 'POST':
        if form.validate_on_submit():
            field = Field()
            field.title = request.form.get('title')
            field.fanni = int(request.form.get('fanny_type'))
            field.grades = [Grade.query.get(int(grade)) for grade in form.grades.data]
            try:
                db.session.add(field)
                db.session.commit()
                flash('your new field is added successfully', 'success')
            except Exception as er:
                db.session.rollback()
                flash(f'Error {er} is happened, please choose another name', 'danger')
            finally:
                return redirect(url_for('quiz.field_new', form=form, 
                                        fields_fanni=fields_fanni, fields_kar=fields_kar))
        else:
            flash(f'your form is not validate .error : {form.errors}, please try again', 'danger')
            return redirect(url_for('quiz.field_new', form=form,
                                    fields_fanni=fields_fanni, fields_kar=fields_kar))
    
    return render_template('quiz/field-new.html', form=form,
                                                fields_fanni=fields_fanni, fields_kar=fields_kar)


@quiz.route('field-edit/<int:field_id>', methods=['POST', 'GET'])
def field_edit(field_id):
    form = FieldNewForm()
    fields_fanni = Field.query.filter_by(fanni=1).all()
    fields_kar = Field.query.filter_by(fanni=0).all()
    field = Field.query.filter_by(id=field_id).first()
    form.grades.choices = [(grade.id, grade.title) for grade in Grade.query.all()]
    
    if request.method == 'POST':
        print('fanni type', form.fanny_type.data)
        if not form.validate_on_submit():
            flash('form is not valid', 'danger')
            return redirect(url_for('quiz.field_edit', field_id=field.id, form=form, 
                                    field=field, fields_fanni=fields_fanni, fields_kar=fields_kar))
        
        field.title = request.form.get('title')
        field.fanni =  int(request.form.get('fanny_type'))
        field.grades = [Grade.query.get(int(grade)) for grade in form.grades.data]
        try:
            db.session.add(field)
            db.session.commit()
            flash('modified successfully', 'success')
        except Exception as er:
            db.session.rollback()
            flash(f'{er}', 'danger')
        finally:
            return redirect(url_for('quiz.field_edit', field_id=field.id, form=form, 
                                    field=field, fields_fanni=fields_fanni, fields_kar=fields_kar))
    
    form.grades.data = [grade.id for grade in field.grades]
    # form.fanny_type.data = 1 if field.fanni == 1 else 0
    return render_template('quiz/field-edit.html', form=form, 
                           field=field, fields_fanni=fields_fanni, fields_kar=fields_kar)


@quiz.route('field-delete/<int:field_id>', methods=['POST'])
def field_delete(field_id):
    form = FieldNewForm()
    fields = Field.query.all()
    if request.method == 'POST':
        field = Field.query.get_or_404(field_id)
        db.session.delete(field)
        db.session.commit()
        return redirect(url_for('quiz.field_new', form=form, fields=fields))
    
    return redirect(url_for(request.referrer))


@quiz.route('course-new', methods=['POST', 'GET'])
def course_new():
    form = CourseForm()
    grades = Grade.query.all()
    fields = Field.query.all()
    users = User.query.all()
    
    form.grade.choices = [(grade.id, grade.title) for grade in grades]
    form.field.choices = [(field.id, field.title) for field in fields]
    form.teacher.choices = [(user.id, user.name) for user in users]
    form.course_credit.choices = [(index, index) for index in [1,2,3,4,5,6,7,8,9,10]]
    
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('your form is not valid', 'danger')
            return redirect(url_for('quiz.course_new', form=form))
        course = Course()
        course.title = request.form.get('title')
        course.grade = int(request.form.get('grade'))
        course.field = int(request.form.get('field'))
        course.teacher = int(request.form.get('teacher'))
        course.course_credit = int(request.form.get('course_credit'))
        try:
            db.session.add(course)
            db.session.commit()
            flash(f'your course {course.title} is added successfully', 'success')
        except Exception as ex:
            db.session.rollback()
            flash(f'{ex}', 'danger')
        finally:
            return redirect(url_for('quiz.course_new', form=form))
    
    return render_template('quiz/course-new.html', form=form)


@quiz.route('academic-year-new', methods=['POST', 'GET'])
def academic_year_new():
    form = AcademicYearForm()
    years = AcademicYear.query.all()
    if request.method == 'POST' and form.validate_on_submit():
        year = AcademicYear()
        year.title = request.form.get('title')
        try:
            db.session.add(year)
            db.session.commit()
            flash(f'New Academic Year {year.title} is created successfully', 'success')
        except Exception:
            db.session.rollback()
            flash('your entered New Academic Year is Duplicated', 'danger')
        finally:
            return redirect(url_for('quiz.academic_year_new', form=form, years=years))
    
    return render_template('quiz/academic-year-new.html', form=form, years=years)
    

@quiz.route('academic-year-edit/<int:year_id>', methods=['POST', 'GET'])
def academic_year_edit(year_id):
    form = AcademicYearForm()
    years = AcademicYear.query.all()
    year = AcademicYear.query.get_or_404(year_id)
    
    return render_template('quiz/academic-year-edit.html', year=year, years=years, form=form)
    
    
@quiz.route('academic-year-delete/<int:year_id>') 
def academic_year_delete(year_id):
    year = AcademicYear.query.get_or_404(year_id)
    db.session.delete(year)  
    db.session.commit()
    flash(f'academic year {year.title} hsa been deleted', 'warning')
    return redirect(url_for('quiz.academic_year_new'))
    

@quiz.route('classroom-edit/<int:class_id>', methods=['POST', 'GET'])
def classroom_edit(class_id):
    form = ClassRoomForm()
    classroom = ClassRoom.query.get_or_404(class_id)
    grades = Grade.query.all()
    fields = Field.query.all()
    students = User.students()
    academic_years = AcademicYear.query.all()
    
    form.grade.choices = [(grade.id, grade.title) for grade in grades]
    form.field.choices = [(field.id, field.title) for field in fields]
    form.students.choices = [(user.id, user.name) for user in students]
    form.academic_year.choices = [(year.id, year.title) for year in academic_years]
    
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('your form is not valid', 'danger')
            return redirect(url_for('quiz.classroom_new', form=form))
        
        _grade = int(request.form.get('grade'))
        _field = int(request.form.get('field'))
        classroom.title = request.form.get('title')
        classroom.grade = _grade
        classroom.field = _field
        classroom.students = [User.query.get(int(std)) for std in form.students.data]
        classroom.courses = [Course.query.get(course.id) for course in Course.query.filter_by(grade=_grade, field=_field).all()]
        classroom.academic_year = int(request.form.get('academic_year'))
        
        try:
            db.session.add(classroom)
            db.session.commit()
            flash(f'your new class room {classroom.title} is added successfully', 'success')
        except Exception as ex:
            db.session.rollback()
            flash(f'{ex}', 'danger')
        finally:
            return redirect(url_for('quiz.classroom_edit', class_id=class_id, classroom=classroom, form=form))
    
    form.grade.default = classroom.grade
    form.field.default = classroom.field
    form.academic_year.default = classroom.academic_year
    form.process()
    form.students.data = [std.id for std in classroom.students]
    
    return render_template('quiz/classroom-edit.html', form=form, classroom=classroom)


@quiz.route('classroom-new', methods=['POST', 'GET'])
def classroom_new():
    form = ClassRoomForm()
    grades = Grade.query.all()
    fields = Field.query.all()
    students = User.students()
    academic_years = AcademicYear.query.all()
    
    form.grade.choices = [(grade.id, grade.title) for grade in grades]
    form.field.choices = [(field.id, field.title) for field in fields]
    form.students.choices = [(user.id, user.name) for user in students]
    form.academic_year.choices = [(year.id, year.title) for year in academic_years]
    
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('your form is not valid', 'danger')
            return redirect(url_for('quiz.classroom_new', form=form))
        
        classroom = ClassRoom()
        _grade = int(request.form.get('grade'))
        _field = int(request.form.get('field'))
        classroom.title = request.form.get('title')
        classroom.grade = _grade
        classroom.field = _field
        classroom.students = [User.query.get(int(std)) for std in form.students.data]
        print('students in form are : ', form.students.data)
        print('students are : ', classroom.students)
        classroom.courses = [Course.query.get(course.id) for course in Course.query.filter_by(grade=_grade, field=_field).all()]
        classroom.academic_year = int(request.form.get('academic_year'))
        
        try:
            db.session.add(classroom)
            db.session.commit()
            flash(f'your new class room {classroom.title} is added successfully', 'success')
        except Exception as ex:
            db.session.rollback()
            flash(f'{ex}', 'danger')
        finally:
            return redirect(url_for('quiz.classroom_new', form=form))
    
    return render_template('quiz/classroom-new.html', form=form)


@quiz.route('exam-new', methods=['POST', 'GET'])
def exam_new():
    form = ExamForm()
    courses = Course.query.all()
    form.course.choices = [(course.id, course.title) for course in courses]
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash(f'form is not valid, {form.errors}', 'warning')
            return redirect(url_for('quiz.exam_new'))
        # 
        dt = jdt_to_gregorian(request.form.get('exam_date'))
        exam = Exam()
        exam.title = request.form.get('title')
        exam.writer = current_user.id
        course = Course.query.get(int(request.form.get('course')))
        exam.course = course.id
        exam.exam_time_long = int(request.form.get('exam_time_long'))
        exam.exam_date = dt
        exam.exam_time_start = int(request.form.get('exam_time_start'))
        exam.modular_semester = int(request.form.get('modular_semester'))
        # 
        try:
            db.session.add(exam)
            db.session.commit()
            flash('your exam is created successfully', 'success')
        except Exception as ex:
            db.session.rollback()
            flash(f'{ex}', 'warning')
        finally:
            return redirect(url_for('quiz.question', exam_id=exam.id, form=form))
                  
        
    return render_template('quiz/exam-new.html', form=form)


@quiz.route('exam-edit/<int:exam_id>', methods=['POST', 'GET'])
def exam_edit(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    form = ExamForm()
    courses = Course.query.all()
    form.course.choices = [(course.id, course.title) for course in courses]
    
    if request.method == 'POST':
        print('date is : ', request.form.get('exam_date'))
        if not form.validate_on_submit():
            flash(f'form is not valid, {form.errors}', 'warning')
            return redirect(url_for('quiz.exam_edit', exam_id=exam.id, form=form))
        # ===================================================================
        dt = jdt_to_gregorian(request.form.get('exam_date'))
        exam.title = request.form.get('title')
        exam.writer = current_user.id
        course = Course.query.get(int(request.form.get('course')))
        exam.course = course.id
        exam.exam_time_long = int(request.form.get('exam_time_long'))
        exam.exam_date = dt
        exam.exam_time_start = int(request.form.get('exam_time_start'))
        exam.modular_semester = int(request.form.get('modular_semester'))
        # ====================================================================
        try:
            db.session.add(exam)
            db.session.commit()
            flash('your exam is ediited successfully', 'success')
        except Exception as ex:
            db.session.rollback()
            flash(f'{ex}', 'warning')
        finally:
            return redirect(url_for('quiz.exam_edit', exam_id=exam.id, form=form))
    
    form.course.default = exam.course
    form.exam_time_long.default = exam.exam_time_long
    form.modular_semester.default = exam.modular_semester
    form.exam_time_start.default = exam.exam_time_start
    form.process()
    
    return render_template('quiz/exam-edit.html', exam=exam, form=form)


@quiz.route('exam-delete/<int:exam_id>', methods=['POST', 'GET'])
def exam_delete(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    form = ExamTestForm()
    if request.method == 'POST':
        db.session.delete(exam)
        db.session.commit()
        return redirect(url_for('quiz.exam_list'))
    return render_template('quiz/exam-delete.html', exam=exam, form=form)


@quiz.route('question/<int:exam_id>', methods=['POST', 'GET'])
def question(exam_id):
    form = QuestionForm()
    exam = Exam.query.get_or_404(exam_id)
    questions = Question.query.filter_by(exam=exam_id).all()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash(f'form is not valid, {form.errors}', 'warning')
            return redirect(url_for('quiz.question', form=form, exam_id=exam_id, questions=questions))

        question = Question()
        question.title = request.form.get('title')
        question.option_1 = request.form.get('option_1')
        question.option_2 = request.form.get('option_2')
        question.option_3 = request.form.get('option_3')
        question.option_4 = request.form.get('option_4')
        question.correct_option = request.form.get('correct_option')
        question.exam = exam_id
        
        try:
            db.session.add(question)
            db.session.commit()
            flash(f'your question is saved for {exam.title}', 'success')
        except Exception as ex:
            db.session.rollback()
            flash(f'{ex}', 'danger')
        finally:
            return redirect(url_for('quiz.question',form=form, exam_id=exam_id, questions=questions))
            
        
    return render_template('quiz/question.html', form=form, exam=exam, questions=questions)


@quiz.route('question-edit/<int:exam_id>/<int:question_id>', methods=['POST', 'GET'])
def question_edit(exam_id, question_id):
    form = QuestionForm()
    question = Question.query.get_or_404(question_id)
    questions = Question.query.filter_by(exam=exam_id).all()
    
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash(f'form is not valid, {form.errors}', 'warning')
            return redirect(url_for('quiz.question_edit', form=form, exam_id=exam_id, question=question, questions=questions, question_id=question_id))
        question.title = request.form.get('title')
        question.option_1 = request.form.get('option_1')
        question.option_2 = request.form.get('option_2')
        question.option_3 = request.form.get('option_3')
        question.option_4 = request.form.get('option_4')
        question.correct_option = request.form.get('correct_option')
        
        try:
            db.session.add(question)
            db.session.commit()
            flash(f'your question is editted for {question.title}', 'success')
        except Exception as ex:
            db.session.rollback()
            flash(f'question title is duplicate, please choose another title', 'danger')
        finally:
            return redirect(url_for('quiz.question_edit', exam_id=exam_id, question_id=question_id,
                                    form=form, question=question, questions=questions))
    
    
    form.correct_option.default = question.correct_option
    form.process()
    form.title.data = question.title

    print('question default value : ', question.correct_option)
    return render_template('quiz/question-edit.html', form=form, exam_id=exam_id,
                           question_id=question_id, question=question, questions=questions)


@quiz.route('question-end/<int:exam_id>', methods=["POST", "GET"])
def question_end(exam_id):
    form = ExamTestForm()
    exam = Exam.query.get_or_404(exam_id)
    if request.method == 'POST':
        exam.confirm = True
        db.session.add(exam)
        db.session.commit()
        flash('Your Question is Confirmmed', 'success')
        return redirect(url_for('quiz.exam_new'))
    
    
    return render_template('quiz/question-end.html', exam=exam, form=form)


@quiz.route('exam-list', methods=['POST', 'GET'])
def exam_list():
    form = ExamTestForm()
    page = request.args.get('page', default=1, type=int)
    all_exam = Exam.query.order_by(Exam.created_at.desc()).paginate(page=page, per_page=7)
    if request.method == 'POST':
        exam = Exam.query.get_or_404(int(request.form.get("exam_id")))
        if exam.confirm == False:
            if len(exam.questions) < 1:
                flash('your exam can not be zero question !!', 'danger')
                return redirect(request.referrer)
            exam.confirm = True
        else:
            exam.confirm = False
        db.session.add(exam)
        db.session.commit()
        return redirect(request.referrer)
    
    return render_template('quiz/exam-list.html', all_exam=all_exam, JalaliDateTime=JalaliDateTime, form=form)


@quiz.route('exam-mylist', methods=['POST', 'GET'])
def exam_mylist():
    form = ExamTestForm()
    page = request.args.get('page', default=1, type=int)
    all_exam = Exam.query.filter_by(confirm=True).order_by(Exam.created_at.desc()).paginate(page=page, per_page=7)
    user_exams = [user.exam_id for user in ExamStudents.query.filter_by(user_id=current_user.id).all()]
    
    if request.method == 'POST':
        session["exam_id"] = request.form.get("exam_id")
        session["user_id"] = current_user.id
        return redirect(url_for('quiz.exam_test'))
    
    return render_template('quiz/exam-mylist.html', all_exam=all_exam,
                           form=form, JalaliDateTime=JalaliDateTime, user_exams=user_exams)


@quiz.route('exam-test', methods=['POST', 'GET'])
def exam_test():
    if session["exam_id"] == None or session["user_id"] == None:
        return redirect(request.referrer)
    
    form = ExamTestForm()
    exam_id = session.get("exam_id")
    exam = Exam.query.get_or_404(exam_id)
    # ============= exam not be zer questions !! =============================
    if len(exam.questions) < 4 :
        flash('this exam is not valid, please add question to this exam', 'danger')
        return redirect(url_for('quiz.exam_mylist'))
    # ===========================================================================
    key = [question.correct_option for question in exam.questions]
    answer = []
    score = 0
    
    if request.method == 'POST':
        for question in exam.questions:
            answer.append(int(request.form.get(f'{question.id}') or '5'))
                
        # 
        for i in range(len(key)):
            if key[i] == answer[i]:
                score += 1
                
        try:
            your_score = (score / len(key)) * 20
        except:
            your_score = 0
            
        session["exam_id"] = None
        session["user_id"] = None
        # 
        exam_std = ExamStudents()
        exam_std.user_id = current_user.id
        exam_std.exam_id = exam_id
        exam_std.score = your_score
        db.session.add(exam_std)
        db.session.commit()
        # 
        session["exam_title"] = exam.title
        session['your_score'] = your_score
        return redirect(url_for('quiz.exam_end'))
    
    
    return render_template('quiz/exam-test.html', exam=exam, form=form)


@quiz.route('exam-preview/<int:exam_id>')
def exam_preview(exam_id):
    form = ExamTestForm()
    exam = Exam.query.get_or_404(exam_id)
    
    return render_template('quiz/exam-preview.html', exam=exam, form=form)

@quiz.route('exam-end')
def exam_end():
    if request.referrer == None:
        return redirect(url_for('quiz.exam_mylist'))
    exam_title = session['exam_title']
    your_score = session['your_score']
    return render_template('quiz/exam-end.html', exam_title=exam_title, your_score=your_score)


@quiz.route('exam-report-card')
def exam_report_card():
    all_exam = ExamStudents.query.filter_by(user_id=current_user.id).all()
    print('all exams : ', all_exam)
    
    return render_template('quiz/exam-report-card.html', all_exam=all_exam, JalaliDateTime=JalaliDateTime)


@quiz.route('class-info/<int:class_id>')
def class_info(class_id):
    classroom = ClassRoom.query.get_or_404(class_id)
    # courses = Course.query.filter_by(classroom=classroom.field).all()
    
    return render_template('quiz/class-info.html', classroom=classroom)


@quiz.route('classes-list')
def classes_list():
    page = request.args.get('page', default=1, type=int)
    all_class = ClassRoom.query.order_by(ClassRoom.academic_year.desc()).paginate(page=page, per_page=7)
    
    return render_template('quiz/classes-list.html', all_class=all_class)


@quiz.route('exam-student-list')
def exam_student_list():
    page = request.args.get('page', default=1, type=int)
    # all_exam = Exam.query.filter_by(confirm=True).order_by(Exam.created_at.desc()).paginate(page=page, per_page=7)
    all_user = User.query.filter_by(User.role > 0).paginate(page=page, per_page=7)
    
    return render_template('quiz/exam-student-list', all_user=all_user)


@quiz.route('student-enroll', methods=['POST', 'GET'])
def student_enroll():
    form = EnrollForm()
    grades = Grade.query.all()
    fields = Field.query.all()
    academic_years = AcademicYear.query.order_by(AcademicYear.created_at.desc()).all()
    
    form.grade.choices = [(grade.id, grade.title) for grade in grades]
    form.field.choices = [(field.id, field.title) for field in fields]
    form.academic_year.choices = [(academic_year.id, academic_year.title) for academic_year in academic_years]
    
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        student_phone = request.form.get('student_phone')
        grade = int(request.form.get('grade'))
        field = int(request.form.get('field'))
        academic_year = int(request.form.get('academic_year'))
        print('grade is : ', grade)
        print('field is : ', field)
        # 
        user = User()
        user.name = student_name
        user.phone = student_phone
        user.role = 4
        try:
            db.session.add(user)
            db.session.commit()
            # 
            new_student = EnrollStudent() 
            new_student.user_id = user.id
            new_student.grade_id = grade
            new_student.field_id = field
            new_student.academic_year_id = academic_year
            try:
                db.session.add(new_student)
                db.session.commit()
                flash('your new student is enrolled successfully', 'success')
            except Exception:
                db.session.rollback()
                # 
        except Exception:
            db.session.rollback()
            flash('your new student information is duplicated', 'danger')
        finally:
            return redirect(url_for('quiz.student_enroll', form=form))
        # 
        
    
    
    return render_template('quiz/student-enroll.html', form=form)
