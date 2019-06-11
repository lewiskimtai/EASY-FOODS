from efoods import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=False, nullable=False)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.relationship('Role', backref='admin', lazy='dynamic')
    order = db.relationship('Order', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.user_name}', '{self.user_email}')"

class Restaurant(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    rest_name = db.Column(db.String(20), unique=False, nullable=False)
    tel_number = db.Column(db.Integer, unique=True, nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    admin = db.relationship('Admin', backref='restaurant', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.rest_name}', '{self.tel_number}')"

class Food(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(20), unique=False, nullable=False)
    price = db.Column(db.Integer, unique=True, nullable=False)
    restaurant = db.relationship('Restaurant', backref='food', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.food_name}', '{self.price}')"

class Orders(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

class Role(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20), unique=False, nullable=False)
  
    def __repr__(self):
        return f"User('{self.role_name}')"

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    user = db.relationship('User', backref='admin', lazy='dynamic')
    role = db.relationship('Role', backref='admin', lazy='dynamic')
    
    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"
