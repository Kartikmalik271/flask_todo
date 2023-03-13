from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from . import db
from flask_login import login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash,check_password_hash


auth = Blueprint('auth',__name__)


#route for login 
@auth.route('/login',methods=['GET','POST'])
def login():
    # get form data
    if request.method=='POST':
        email=request.form.get("email")
        password=request.form.get("password")
        user=User.query.filter_by(email=email).first()

        # check if user exists 
        if user:
            if check_password_hash(user.password,password):
                flash('logged In',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.homepage'))
            else:
                flash('Incorrect Password',category='error')
        else:
            flash('User does not exist',category='error')
            return redirect(url_for('auth.signup'))
    return render_template("login.html",user=current_user)

#route for logout button
@login_required
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#route for signup 
@auth.route('/signup',methods=['GET','POST'])
def signup():
    # extract form data
    if request.method=='POST':
        email=request.form.get('email')
        username=request.form.get('username')
        password=request.form.get('password')
        repassword=request.form.get('repassword')

        #check and verify the credentials before registering user
        user=User.query.filter_by(email=email).first()
        if user:
            flash('User Already exist',category='error')
        elif len(email)<4:
            flash('Email too short',category='error')
        elif len(username)<2:
            flash('Username too short',category='error')
        elif password!=repassword:
            flash('password mismatched',category='error')
        elif len(password)<6:
            flash('Password must be greater than 6 digits',category='error')
        else:
            #add user to database
            new_user=User(email=email,username=username,password=generate_password_hash(password,method='sha256'))
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Account Created',category='success')
                return redirect(url_for('auth.login'))
            except:
                 flash('Error Occured while creating user, try again',category='error') 
    return render_template("signup.html",user=current_user)
