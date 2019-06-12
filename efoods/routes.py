import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from efoods import app, db, bcrypt
from efoods.forms import UserRegistrationForm, LoginForm, RestaurantRegistrationForm, FoodRegistrationForm, OrderForm
from efoods.models import User, Restaurant, Food, Orders, Admin, Role
from flask_login import login_user, current_user, logout_user, login_required
from flask_user import roles_required
from flask_mail import Message



@app.route('/')
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = UserRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if not User.query.filter_by(User.user_email=='lewis.kimtai@gmail.com').first():
            user1 = User(user_name='Lewis', user_email='lewis.kimtai.com', password=hashed_password)
            user1.roles.append(Role(role_name='admin'))
            db.session.add(user1)
            db.session.commit()
            flash
        else:
            user = User(user_name=form.user_name.data, user_email=form.user_email.data, password=hashed_password)
            user.role.append(Role(role='customer'))
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
@roles_required('admin')
def admin():
    restaurant = RestaurantRegistrationForm()
    food = FoodRegistrationForm()
    restaurants = Restaurant.query.join(User).join(Admin).join(Role).filter_by(Role.c.role_name == 'admin' and Restaurant.c.rest_name == 'rest_name').all()
    foods = Food.query.join(Restaurant).join(Food).join(Admin).join(User).join(Role).filter_by(Role.c.role_name == 'admin'and Restaurant.c.rest_name == 'rest_name' and Food.c.food_name == 'food_name' and Food.c.price == 'price').all()
    orders = Orders.query.join(Food).join(Restaurant).join(User).join(Admin).join(Role).filter_by(Role.c.role_name == 'admin' and Food.c.food_name == 'food_name' and Food.c.price == 'price' and Orders.c.drop == 'drop' and Restaurant.c.rest_name == 'rest_name').all()
    if restaurant.validate_on_submit():
        rest = Restaurant(rest_name = restaurant.rest_name.data, tel_number = restaurant.tel_number.data)
        db.session.add(rest)
        db.session.commit()
        flash('You have created a Restaurant')
        return redirect(url_for('admin'))
    else:
        food.validate_on_submit()
        food = Food(food_name=food.food_name.data, price=food.price.data)
        db.session.add(food)
        db.session.commit()
        flash('You have successfully created a meal')
        return redirect(url_for('admin'))
    return render_template('admin.html', title='Admin', restaurant=restaurant, food=food, restaurants=restaurants, foods=foods, orders=orders)


@app.route('/home', methods=['GET', 'POST'])
@roles_required('customer')
def home():
    rest = RestaurantRegistrationForm()
    food = FoodRegistrationForm()
    restaurants = Restaurant.query.filter_by(restaurant_id = 'Restaurant.id').all()
    foods = Food.query.join(Restaurant).filter_by(Restaurant.c.restaurant_id == 'Restaurant.id', Food.c.food_name == 'food_name', Food.c.price == 'price').all()
    return render_template('home.html', restaurants=restaurants, foods=foods)

@app.route('/order', methods=['GET', 'POST'])
@roles_required('customer')
def order():
    order = OrderForm()
    if order.validate_on_submit():
        order = Orders(drop = order.order.data)
        db.session.add(order)
        db.session.commit()
        flash('You have ordered a meal')
    return render_template('home.html', order=order)


  
