import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from efoods import app, db, bcrypt
from efoods.forms import UserRegistrationForm, LoginForm, RestaurantRegistrationForm, FoodRegistrationForm
from efoods.models import User, Restaurant, Food, Orders, Admin, Role
from flask_login import login_user, current_user, logout_user, login_required
from flask_user import roles_required
from flask_mail import Message



@app.route('/')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = UserRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if not User.query.filter(User.user_email=='lewis.kimtai@gmail.com').first():
            user1 = User(user_name='Lewis', user_email='lewis.kimtai.com', password=hashed_password)
            user1.roles.append(Role(role_name='admin'))
            db.session.add(user1)
            db.session.commit()
        else:
            user = User(user_name=form.user_name.data, user_email=form.user_email.data, password=hashed_password)
            user.role.append(Role(role='customer'))
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)

@app.route('/login', methods=['GET', 'POST']) 
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.user_email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

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
