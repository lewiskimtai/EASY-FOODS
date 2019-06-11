from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import Required, Email, EqualTo, Length, ValidationError
from efoods.models import User, Restaurant

class UserRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[Required(), Length(min=2, max=20)])
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    confirm_password = PasswordField('Confirm Password', validators=[Required(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RestaurantRegistrationForm(FlaskForm):
    restaurant_name = StringField('Restaurant_Name', validators=[Required(), Length(min=2, max=20)])
    tel_number = IntegerField('Telephone_Number', validators=[Required(), Length(max=10)])
    submit = SubmitField('Create Restaurant')

    def validate_restaurant(self, name):
        restaurant = Restaurant.query.filter_by(name=rest_name.data).first()
        if restaurant:
            raise ValidationError('That Restaurant Name is taken. Please choose a different one.')

class FoodRegistrationForm(FlaskForm):
    food_name = StringField('Food_Name', validators=[Required(), Length(min=2, max=20)])
    price = IntegerField('Price', validators=[Required(), Length(max=10)])
    submit = SubmitField('Create Food')


