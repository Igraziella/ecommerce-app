from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os 



app = Flask(__name__)

# SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

# print(SQLALCHEMY_DATABASE_URI)




# python run.py

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'info'
login_manager.init_app(app)
csrf = CSRFProtect(app)


# os.getenv('SECRET_KEY')

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# load_dotenv()
# app.config['SQLALCHEMY_DATABASE_URI'] =  os.getenv('SQLALCHEMY_DATABASE_URI')


app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] =  os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'bf3e1fa624133c7b254c2dacda42c30793198d9524c9b99aaad0be40cb7b1ca2'
app.config['UPLOAD_FOLDER'] = 'C:/Users/HamadaSalimGTrd/Desktop/ecommerce-app/EcommerceApp/static/IMAGE'
app.config['ALLOWED_EXTENSIONS'] = {'png','PNG', 'jpg','JPG','jpeg','JPEG','gif','GIF'}


ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS'],'Images only!'

from EcommerceApp import routes
from EcommerceApp import models
