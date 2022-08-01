#https://www.youtube.com/watch?v=dam0GPOAvVI&ab_channel=TechWithTim
# use of jinja time 49 minutes

from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User #import user to make user from signup page
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user,logout_user,login_required,current_user
#bluefprints allows to create routes for the app in multiple files
# instead of just putting @app.route() only in our main file
#we can use @views.route() once views blueprint is defined in views.py
#or @auth.route() once auth blueprint is defined still all blueprints are accessing same main [app=Flask(__name__)]

#views is just name for route & blueprint it could be anything, just for easeness we gave it same as filename

auth=Blueprint('auth',__name__)



@auth.route('/signup', methods=['GET','POST'])
def signup():
#collect element completed on website by user, POST method is by submit button and
# get is the method when we refresh or log in

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')


# flash library can be use to alert the customer about errors on page, n corrections needed
        user = User.query.filter_by(email=email).first()
        if user:
            flash('email exist',category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            #we never store the password as such and keep its original form instead we use hash
            #once this hash is generated password can't be checked for its original from
            #but this hash can be checked with other password input if the two hashes are same
            #sha256 is just a hashing algorithm

            new_user=User(email=email,first_name=first_name,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user) #create account in db
            db.session.commit()
            flash('Account created!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home')) #once accountcreated go back to homepage
    return render_template('signup.html',user=current_user)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first() #first match from User table for the email, it will pass that whole record
        if user:
            if check_password_hash(user.password,password):
                flash('Login successful',category='success')
                login_user(user,remember=True) #this user will be remembered by browser
                return redirect(url_for('views.home'))
            else:
                flash('password dosenot match',category='error')
        else:
            flash('email doesnot exist',category='error')
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required #this decorator make sures that we cannot access this function unless someone is logged in
def logout():
    logout_user()
    return redirect(url_for("auth.login"))