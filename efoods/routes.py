import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from efoods import app, db, bcrypt
from efoods.forms import UserRegistrationForm, LoginForm, RestaurantRegistrationForm, FoodRegistrationForm
from efoods.models import User, Restaurant, Food, Orders, Admin, Role
from flask_login import login_user, current_user, logout_user, login_required
from flask_user import roles_required, UserManager, EmailManager

user_manager = UserManager(app, db, Role)
email_manager = EmailManager(app)


@app.route('/')
@app.route('/index') 
def index():
    return render_template('index.html')


@app.route('/student_register', methods=['GET', 'POST'])
def student_register():
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        student_hashed_password = bcrypt.generate_password_hash(form.student_password.data).decode('utf-8')
        student = User(user_name=form.student_name.data, user_email=form.student_email.data, user_password=student_hashed_password)
        student.role.append(Role(role='student'))
        db.session.add(student)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('student_register.html', title='Student Registration', form=form)

@app.route('/login', methods=['GET', 'POST']) 
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.user_email.data).first()
        if user and bcrypt.check_password_hash(user.user_password, form.user_password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('student_home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('student_login.html', title='Student Login', form=form)

@app.route('/lecturer_register', methods=['GET', 'POST']) 
def lecturer_register():
    form = LecturerRegistrationForm()
    if form.validate_on_submit():
        lecturer_hashed_password = bcrypt.generate_password_hash(form.lecturer_password.data).decode('utf-8')
        lecturer = Lecturer(lecturer_name=form.lecturer_name.data, lecturer_email=form.lecturer_email.data, lecturer_password=lecturer_hashed_password)
        lecturer.role.append(Role(role='lecturer'))
        db.session.add(lecturer)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('lecturer_login'))
    return render_template('lecturer_register.html', title='Lecturer Register', form=form)

    
#@app.route('/lecturer_login', methods=['GET', 'POST']) 
#def lecturer_login():
#    form = LecturerLoginForm()
#    if form.validate_on_submit():
#        lecturer = Lecturer.query.filter_by(lecturer_email=form.lecturer_email.data).first()
#        if lecturer and bcrypt.check_password_hash(lecturer.lecturer_password, form.lecturer_password.data):
#            login_user(lecturer, remember=form.remember.data)
#            next_page = request.args.get('next')
#            return redirect(next_page) if next_page else redirect(url_for('lecturer_home'))
#        else:
#            flash('Login Unsuccessful. Please check email and password', 'danger')
#    return render_template('lecturer_login.html', title='Lecturer Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/student_home', methods=['GET', 'POST'])
@roles_required('student')
def student_home():
    return render_template('student_home.html')
  
        
   

@app.route('/student_account', methods=['GET', 'POST'])
@login_required
def student_account():
    return render_template('index.html')

@app.route('/lecture_account', methods=['GET', 'POST'])
@login_required
def lecturer_account():
    return render_template('index.html')


@app.route('/lecturer_home')
@roles_required('lecturer')
def lecturer_home():
    return render_template('lecturer_home.html')
    
@app.route('/classmates')
@login_required
def classmates():
    return render_template('classmates.html')

@app.route('/lecturers')
def lecturers():
    return render_template('lecturers.html')

@app.route('/courseunits') 
def courseunits():
    return render_template('courseunits.html')

@app.route('/timetable') 
def timetable():
    return render_template('timetable.html')

@app.route('/notes') 
def notes():
    return render_template('notes.html')

@app.route('/tutorials') 
def tutorials():
    return render_template('tutorials.html')

@app.route('/discussions') 
def discussions():
    return render_template('discussions.html')

@app.route('/courseworks') 
def courseworks():
    return render_template('courseworks.html')

@app.route('/tests') 
def tests():
    return render_template('tests.html')

@app.route('/exams') 
def exams():
    return render_template('exams.html')

@app.route('/results') 
def results():
    return render_template('results.html')
