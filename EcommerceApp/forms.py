from flask_wtf import FlaskForm, CSRFProtect
from wtforms import (StringField, SubmitField, 
                    PasswordField, StringField, 
                    TextAreaField, SelectMultipleField, 
                    FloatField, TelField, DateField, 
                    IntegerField, SelectField, TextAreaField, RadioField)

from flask_wtf.file import FileField, FileRequired, FileAllowed, DataRequired
from wtforms.validators import DataRequired, Length, Email, EqualTo

from EcommerceApp import ALLOWED_EXTENSIONS

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),  Length(min=2, max=49) ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8) , EqualTo('confirm_password', message='Passwords do not match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UpdateCartForm(FlaskForm):
    quantity =  IntegerField('Quantity', render_kw={'min': 1}, default=1)
    submit = SubmitField('Update Cart')

class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    price =  FloatField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category_name = SelectMultipleField('Select Category Name', choices=[('shoe', 'women'), ('cloth','men')], validators=[DataRequired()])
    image_file = FileField('Photo',validators=[FileRequired(FileAllowed(ALLOWED_EXTENSIONS))])
    submit = SubmitField('Add Product')


class OrderForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min = 2, max = 30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min = 2, max = 30)])
    country = StringField('Country/Region', validators=[DataRequired(), Length(min=2, max = 40)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max = 40)])
    city = StringField('City/Town', validators=[DataRequired(), Length(min=2, max = 40)])
    street_address = StringField(' Address', validators=[DataRequired(), Length(min=2, max = 100)])
    contact_number = TelField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    # quantity = IntegerField('Quantity', validators=[DataRequired()])
    status = SelectField('Status', choices=[('pending','pending'), ('delivered', 'delivered')])
    addition_information =  TextAreaField('Addition Information'  )
    payment_method = RadioField('Payment Method', validators=[DataRequired()], 
    choices=[('Pay through direct transfer') , ('Pay cash on delivery')])

    # date =  DateField('date',validators=[DataRequired()])
    submit = SubmitField('Send Order')
