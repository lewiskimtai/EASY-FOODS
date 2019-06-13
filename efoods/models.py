from efoods import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

meals = db.Table('meals',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurant.id')),
    db.Column('food_id', db.Integer, db.ForeignKey('food.id'))
)

orders = db.Table('orders',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('meals_id', db.Integer, db.ForeignKey('meals.id'))
)

class Role(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), unique=False, nullable=False)
    user = db.relationship('User', backref='role')
    
    def __repr__(self):
        return f"User('{self.role}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    restaurant = db.relationship('Restaurant', backref='user')
    food = db.relationship('Food', backref='user')
    order = db.relationship('meals', secondary=orders, backref=db.backref('customer', lazy='dynamic'))
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Restaurant(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    rest_name = db.Column(db.String(20), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    dishes = db.relationship('Food', secondary=meals, backref=db.backref('meals', lazy='dynamic'))
    
    def __repr__(self):
        return f"User('{self.rest_name}')"

class Food(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(20), unique=False, nullable=False)
    price = db.Column(db.String(20), unique=False, nullable=False)
    food = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f"User('{self.food_name}', '{self.price}')"
