from flask import Blueprint, render_template, request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user , login_required, logout_user, current_user



#we are going to define this file is a blueprint of our app 

auth = Blueprint('auth',__name__)

#login function

@auth.route('/login',methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #finding if email exists 
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in!', category = 'success')
                login_user(user, remember = True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category = 'error ')
        else:
            flash('Email does not exist.', category = 'error')

    return render_template("login.html",user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))  

#sign up function 

@auth.route('/sign-up',methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email = email).first()
        if user:
            flash('Email already exists', category = 'error')
        elif len(email) < 4:
            flash('Email must be more than 4 characters', category = 'error')
        elif len(first_name) < 2:
            flash('First Name must be more than 2 characters', category = 'error')
        elif password1 != password2:
            flash('Passwords do not match', category = 'error')
        elif len(password1)<3 :
            flash('password must be more than 3 characters', category = 'error')
        else :
            #add user to database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember = True)
            flash('Account created!',category = 'success')
            return redirect(url_for('views.home'))
 
    return render_template("sign-up.html", user = current_user) 
 
