from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import shortuuid
import os
import secrets
from flask_login import logout_user, LoginManager, login_required, current_user, login_user

from EcommerceApp import app, db, bcrypt, login_manager, mail
from EcommerceApp.models import  Product, User, Order_list, Order
from EcommerceApp.forms import RegistrationForm, LoginForm, ProductForm, UpdateCartForm, OrderForm


@app.route('/')
def home():
    products = Product.query.all()
    return render_template('index.html', products=products)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register' , methods=['POST', 'GET'])
def signup():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data  

        # user = User.query.filter_by(email=email).first()
        if User.query.filter_by(email=email).first():
            flash('User already exists, please login', 'error')
            # return render_template('login.html', form=form)
            return redirect(url_for('login'))


        password_hash = generate_password_hash(password)
        try:
            new_user = User(name=name, email=email, password_hash=password_hash)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            flash('Account created successfully', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Error creating account. Please try again.', 'error')
            app.logger.error(f"Error creating account: {e}")
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)





# @app.route('/register' , methods=['POST', 'GET'])
# def signup():
#     form = RegistrationForm()
#     if request.method == 'POST' and form.validate_on_submit():
#             name = form.name.data
#             email = form.email.data
#             password = form.password.data
#             confirm_password = form.confirm_password.data
             
#             if  password != confirm_password:
#                 error_message = 'Enter matching password' 
#                 return render_template('forms.html', form=form, error_message=error_message)
            
#             user = User.query.filter_by(email=email).first()
#             # if form.errors:
#             #     for error_message in form.errors:
#             #         print(f'The errors: {error_message}')


#             # user = User.query.filter(email).first()
#             # user = User.query.get(email).all()
            
#             if user:
#                 error_message = 'user already exist, please login' 
#                 return render_template('login.html', error_message=error_message, form=form)
#             # if password and password==confirm_password:
                
#             password_hash = generate_password_hash(password)
#             new_user = User(name =name, email=email, password_hash=password_hash)
#             db.session.add(new_user)
#             db.session.commit()
#             session['email'] = email

#             # msg = Message('Email confirmation', sender='beupalways@gmail.com', recipients= [f'{email}'] )

#             # verification_link = 'http://127.0.0.1:8080/login'

            
#             # # msg.body = f'''Welcome {name.title()}, your account has been created successfuly.\nClick the following link to verify your email: {verification_link}'''
#             # msg.html = render_template('email_verification.html', verification_link=verification_link)
#             # mail.send(msg)
#             # notification_message =  f'Please confirm your account by clicking on the link sent to {email}'
#             # print('email was sent successfully')
#             return render_template('login.html', form=form)
#             # return render_template('login.html', form=form, notification_message=notification_message)
#                 # return render_template('home.html', form=form) 
#                 # notification_message = 'Enter matching password' 
#             # return render_template('forms.html', form=form, error_message=error_message)

#         # return render_template('home.html', form=form)

#     return render_template('forms.html', form=form)



@app.route('/login' , methods=['POST', 'GET'])
def login():
    form =  LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                flash(' Succesfully logged in', 'success')
                return redirect(url_for('get_products'))
            
            flash('Invalid username or password', 'info')
            return render_template('login.html', form=form)   
    return render_template('login.html', form=form)



@app.route('/product' , methods=['POST', 'GET'])
def add_product():
    form = ProductForm()
    if form and form.validate_on_submit():
        if request.method == 'POST':
            # if form.validate_on_submit:
            product_name = form.product_name.data
            price = form.price.data
            description = form.description.data
            category_name = form.category_name.data
            image_file = form.image_file.data
            if not image_file:
                flash('upload image')
            filename = secure_filename(image_file.filename)
            try:
                image_filename = f'{product_name}_{price}_' + str(shortuuid.uuid()) + os.path.splitext(filename)[-1]
                # print(image_filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                # print(image_path)
                image_file.save(image_path)
                new_product = Product( product_name =product_name,price=price, description=description, category_name=category_name, image_url=image_filename)
                db.session.add(new_product)
                db.session.commit()
                flash('product added succesfully', 'success')
                return redirect(url_for('add_product'))
            except Exception as e:
                    # print(e)
                    flash('error saving file: {e}', 'error')
                
            return render_template('home.html', form=form) 

        return render_template('products.html', form=form)

    return render_template('products.html', form=form)

@login_required
@app.route('/order_list/<int:product_id>', methods=['POST', 'GET'])
def add_to_cart(product_id):

    if not current_user.is_authenticated:
        flash('user is not signed in', 'info')
        return redirect(url_for('login'))

    product = Product.query.filter_by(id=product_id).first()
    # print(product.price)
    if not product:
        flash('Product not found')
        return redirect(url_for('get_products'))
    

    try:
        if request.method == 'GET':
            user_id = current_user.id
            print(user_id)
            existing_order_item = Order_list.query.filter_by(user_id=user_id, product_id=product_id).first()

            if existing_order_item:
                flash('Product already in cart', 'info')
                return redirect(url_for('get_products'))
            else:
                new_order_item = Order_list(
                    product_id=product_id, 
                    product_name=product.product_name, 
                    image_url=product.image_url, 
                    user_id=user_id,
                    price=product.price, 
                    quantity=1
                )

                db.session.add(new_order_item)
                db.session.commit()
                flash('Product added to cart successfully', 'success')
                return redirect(url_for('get_products', product_id=product_id))
    except Exception as e:
        flash(f'Error: {e}')
        app.logger.error(f'Error: {e}')
        return redirect(url_for('get_products'))
    return redirect(url_for('get_products'))


def calculate_total_price(user_cart_list):
    total_amount = 0
    for product in user_cart_list:
        # print(product.quantity)
        # print(product.price)
        # sub_total = (product.quantity)*(product.price)
        total_amount += (product.quantity)*(product.price)
    print(total_amount)
    return total_amount

def calculate_sub_price(user_cart_list):
    sub_amount_list = []
    sub_amount_dict = {}
    for product in user_cart_list:
        product_name = product.product_name
        product_quantity = product.quantity
        sub_amount = product.quantity * product.price
        # formatted_sub_amount = f'{product_name}: ₦{sub_amount}'
        sub_amount_dict[product_name] = sub_amount

        print(product.quantity)
        print(product.price)
        # sub_amount = (product.quantity)*(product.price)
        sub_amount_list.append(sub_amount)
    # print(sub_amount_list)
    # return sub_amount_list
    print(sub_amount_dict)
    return sub_amount_list, sub_amount_dict, product_quantity



@login_required
@app.route('/get_cart/', methods=['POST', 'GET'])
def get_cart():
    if current_user.is_authenticated:
        user_id = current_user.id
        product_id = request.args.get('product_id')
        print(product_id)
        try:
            user_cart_list = Order_list.query.filter_by(user_id=user_id).all()
            if not user_cart_list:
                flash('Your cart is empty')
                return redirect(url_for('get_product'))

            form = UpdateCartForm()
            if request.method == 'POST' and form.validate_on_submit():
                product_in_cart = Order_list.query.filter_by(user_id=user_id, product_id=product_id).first()
                product_in_cart.quantity = form.quantity.data
                db.session.commit()
                flash(f'Cart succesfully updated ', 'success') 
                sub_amount_list, sub_amount_dict, product_quantity = calculate_sub_price(user_cart_list)
                total_amount = calculate_total_price(user_cart_list)
                print(total_amount)
                # return redirect(url_for('get_cart'))
                return render_template('showcart.html',form=form, user_cart_list = user_cart_list, total_amount=total_amount, sub_amount_list=sub_amount_list) 
            sub_amount_list, sub_amount_dict, product_quantity = calculate_sub_price(user_cart_list)
            total_amount = calculate_total_price(user_cart_list)
            return render_template('showcart.html',form=form, user_cart_list = user_cart_list, total_amount=total_amount,sub_amount_dict=sub_amount_dict, sub_amount_list=sub_amount_list) 
        except Exception as e:
            flash('error in getting user id')
            app.logger.error(f'error: {e}')
            return redirect(url_for('login'))
    return redirect(url_for('login'))

@app.route('/delete_cart/<int:product_id>', methods=['POST', 'GET'])
def delete_cart(product_id):
    try:
        product_in_cart = Order_list.query.filter_by(product_id=product_id).first()
        db.session.delete(product_in_cart)
        db.session.commit()
        # return render_template('addcart.html', product_id=product_id, user_cart_list = user_cart_list)
        flash(f'Product succesfully removed from cart', 'error') 
        return redirect(url_for('get_cart', product_id=product_id))
    except Exception as e:
        flash('error in deleting product from cart', 'error')
        app.logger.error(f'error: {e}')
        return redirect(url_for('login'))

# @app.route('/update_cart/<int:product_id>', methods=['POST', 'GET'])
# def update_cart(product_id):
#     form = UpdateCartForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         quantity = form.quantity.data
        
#         try:
#             user_id = current_user.id
#             user_cart_list = Order_list.query.filter_by(user_id=user_id).all()
#             # product_in_cart = Order_list.query.filter_by(product_id=product_id).first()
#             # product_in_cart = Order_list.query.all()
#             for cart in user_cart_list:
#                 if cart.product_id == product_id:
#                     cart.quantity = quantity
#                     # db.session.delete(product_in_cart)
#                     db.session.commit()
#                     # return render_template('addcart.html', product_id=product_id, user_cart_list = user_cart_list)
#                     total_amount = calculate_total_price(user_cart_list)
#                     flash(f'Cart succesfully updated ', 'success') 
#                     # return render_template('showcart.html',product_id=product_id, total_amount=total_amount, user_cart_list = user_cart_list)
#                     return redirect(url_for('get_cart', product_id=product_id)) 
#         except Exception as e:
#             flash('error updating cart', 'error')   
#             app.logger.error(f'error: {e}')
#             return redirect(url_for('login'))

#     return render_template('showcart.html', form=form, product_id=product_id)




@app.route('/update_cart/<int:product_id>/<int:quantity>', methods=['POST', 'GET'])
def update_cart(product_id, quantity):
    form = UpdateCartForm()
    if request.method == 'POST' and form.validate_on_submit():
        form.quantity.data = quantity
        user_id = current_user.id
        try:
            product_in_cart = Order_list.query.filter_by(user_id=user_id, product_id=product_id).first()
            product_in_cart.quantity = form.quantity.data
                    # db.session.delete(product_in_cart)
            db.session.commit()
                    # return render_template('addcart.html', product_id=product_id, user_cart_list = user_cart_list)
            # total_amount = calculate_total_price(user_cart_list)
            flash(f'Cart succesfully updated ', 'success')
            # user_cart_list = Order_list.query.filter_by(user_id=user_id).all() 
            # return render_template('showcart.html',product_id=product_id, total_amount=total_amount, user_cart_list = user_cart_list)
            return redirect(url_for('get_cart'))
            # return redirect(url_for('update_cart', product_id=product_id)) 
        except Exception as e:
            flash('error updating cart', 'error')   
            app.logger.error(f'error: {e}')
            return redirect(url_for('get_cart'))

    return render_template('u.html', form=form, product_id=product_id)







# place_order endpoint for all products
@login_required
@app.route('/order', methods=['POST', 'GET'])
def place_order():
    form = OrderForm()
    if current_user.is_authenticated:
        # product = Product.query.all()
        user_cart_list = Order_list.query.all()
        sub_amount_list, sub_amount_dict, product_quantity = calculate_sub_price(user_cart_list)
        total_amount = calculate_total_price(user_cart_list)
        if user_cart_list: 
            
            if request.method == 'POST' and form.validate_on_submit():
                    first_name = form.first_name.data
                    last_name = form.last_name.data
                    country = form.country.data
                    state = form.state.data
                    city = form.city.data
                    street_address = form.street_address.data
                    contact_number = form.contact_number.data
                    status = form.status.data
                    addition_information = form.addition_information.data
                    payment_method = form.payment_method.data
                    print(payment_method)
                    invoice = secrets.token_hex(5)
                    user_id = current_user.id
                    user_email = current_user.email
                    product_id = [product.id  for product in Order_list.query.all()]
                    try:
                        order_info = Order(first_name=first_name, 
                        last_name=last_name, street_address=street_address, 
                        contact_number=contact_number, 
                        country=country, state=state, city=city, addition_information=addition_information,
                        invoice=invoice, user_id=user_id, payment_method=payment_method)
                        db.session.add(order_info)
                        db.session.commit()
                       
                        print(product_id)
                        flash('Order placed succesfully', 'info')

                        # return redirect(url_for('get_cart', product_id=product_id))
                        # return render_template('checkout.html')
                        return redirect(url_for('get_cart'))
                    except Exception as e:
                        flash('placing of order failed', 'error')
                        app.logger.error(f'Error placing order: {e}')
                        return render_template('showcart.html' , form=form )
            return render_template('order.html', form=form , user_cart_list = user_cart_list,
                                 sub_amount_dict=sub_amount_dict, total_amount=total_amount, 
                                 sub_amount_list=sub_amount_list, product_quantity=product_quantity)
    
        flash(' Product not in cart', 'info')
        return redirect(url_for('add_to_cart', product_id=product_id) )     

    flash('Please check order again', 'error')
    return redirect(url_for('login'))




# # place_order endpoint for single product 
# @login_required
# @app.route('/order/<int:product_id>', methods=['POST', 'GET'])
# def place_order(product_id):
#     form = OrderForm()
#     if current_user.is_authenticated:
#         product = Product.query.all()
#         user_cart_list = Order_list.query.filter_by(product_id=product_id).first()
#         if user_cart_list:
#             if request.method == 'POST' and form.validate_on_submit():
#                     address = form.address.data
#                     contact_number = form.contact_number.data
#                     quantity = form.quantity.data
#                     invoice = secrets.token_hex(5)
#                     user_id = current_user.id
#                     try:
#                         order_info = Order(address=address, contact_number=contact_number, quantity=quantity, 
#                         product_id=product_id, user_id=user_id, invoice=invoice)
#                         db.session.add(order_info)
#                         db.session.commit()
#                         flash('Order placed succesfully', 'info')
#                         # return redirect(url_for('get_cart', product_id=product_id))
#                         # return render_template('checkout.html')
#                         return redirect(url_for('checkout', product_id=product_id))
#                     except Exception as e:
#                         flash('placing of order failed', 'error')
#                         app.logger.error(f'Error placing order: {e}')
#                         return render_template('addcart.html', product_id=product_id, form=form )

#             flash('Check  again', 'error')
#             return render_template('order.html', product_id=product_id, form=form , product = product)
    
#         flash(' Product not in cart', 'info')
#         return redirect(url_for('add_to_cart', product_id=product_id) )     

#     flash('Please check order again', 'error')
#     return redirect(url_for('login'))



# checkout for single product 
@login_required
@app.route('/checkout/<int:product_id>', methods=['POST', 'GET'])
def checkout(product_id):
    # order = Order.query.filter_by(product_id = product_id).all() 
    product_and_order = Order.query.join(Product, Product.id==Order.product_id).filter(Product.id == product_id).first() 
    
    # product, order = product_and_order
    # for i in order:
    #     print(i)
    if product_and_order: 
        product = product_and_order.product
        order = product_and_order
        try: 
            # sub_total = 0
            quantity = (order.quantity)
            unit_price = (product.price)
            total_price = (quantity * unit_price)
            invoice = order.invoice
            address = order.address
            contact_number =order.contact_number
            product_name =  product.product_name
            user_id = current_user.id
            user =  User.query.filter_by(id = user_id).first()
            customer_name = user.name
            email = user.email

            current_order = Order_list.query.filter_by(product_id = product_id).first()
            db.session.delete(current_order)
            db.session.commit()
            flash('Order succesfully placed')
            # return redirect(url_for('checkout', product_id = product_id, 
            #                             quantity=quantity, unit_price=unit_price, 
            #                             total_price=total_price, invoice=invoice, 
            #                             customer_name=customer_name, product_name=product_name))  
            return render_template('checkout.html',  product_id = product_id, 
                                        quantity=quantity, unit_price=unit_price, 
                                        total_price=total_price, invoice=invoice, 
                                        customer_name=customer_name, product_name=product_name, 
                                        address=address, contact_number=contact_number, email=email) 
        except Exception as e:
            flash(f'Error during checkout: {e}', 'error')
            app.logger.error(f'Error during checkout: {e}')

    return redirect(url_for('checkout', product_id = product_id))

   
@app.route('/customer/get_products' , methods=['POST', 'GET'])
def get_products():
   products = Product.query.all()
   return render_template('customer_products.html', products=products )


@app.route('/admin/get_products' , methods=['POST', 'GET'])
def admin_products():
   products = Product.query.all()
   return render_template('admin_products.html', products=products )



@app.route('/delete_product/<int:product_id>' , methods=['POST', 'GET'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return redirect(url_for('home'))
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('get_products'))

@login_required
@app.route('/logout/')
def logout():
    logout_user()
    return redirect('home')