from EcommerceApp  import db
from flask_login import  UserMixin
from  datetime import datetime



class User( db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    def __repr__(self):
        return f'<User ={self.id} name={self.name} email={self.email}>'

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    country = db.Column(db.String(50), nullable=False)
                   
    state = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)
    invoice = db.Column(db.String(20), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)                                               
    status = db.Column(db.String(20), default='pending')
    addition_information = db.Column(db.String(300))
    payment_method = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('products', lazy=True))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('users', lazy=True))
    

    def __repr__(self):
        return '< Order %r>' % self.id





class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    product_name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer)
    description = db.Column(db.Text)
    category_name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    def __repr__(self):
        return '< Product %r>' % self.product_name


# class Category(db.Model):
#     # __tablename__ = 'categories'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)

class Order_list(db.Model):
    __tablename__ = 'order_items'   
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    image_url = db.Column(db.String(255), nullable=False)