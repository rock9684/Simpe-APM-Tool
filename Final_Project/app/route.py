from flask import render_template, url_for, request, jsonify , flash, redirect, request,session
from app import webapp, resources,bcrypt
from app import AWS_SECRET_KEY, AWS_ACCESS_KEY
from app.forms import LoginForm,RegistrationForm, ApplicationUploadForm
import hashlib
import datetime
from app import databaseModule,database


from werkzeug.utils import secure_filename
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import requests


webapp.secret_key = r'\x8\xbeHJ:\x9f\xf0!\xb1a\xaa\x0f\xee'

@webapp.route('/', methods=['GET', 'POST'])
@webapp.route('/login', methods=['GET', 'POST'])
def login():
    session["loggedIn"] = False
    session["currentUser"] = ""
    session["access_level"]=""
    session["accountName"] =""
    form = LoginForm()
    #return render_template("login.html", form=form, error="")
    if form.validate_on_submit():
        account = str(form.account.data)
        username = str(form.username.data)
        password = str(form.password.data)

        verify_variable=database.verify_username(account,username, password)
        if verify_variable[0]==1:
            print("Successful Authentication")
            session["access_level"]= str(verify_variable[1])
            session["loggedIn"] = True
            session["currentUser"] = username
            session["accountName"] =account
            return redirect(url_for('home_page'))

        else:
            error="Failed Authentication!"
            return render_template("login.html", form=form, error=error)



    return render_template("login.html",form=form,error="")

@webapp.route('/home_page', methods=['GET', 'POST'])
def home_page():
    if 'loggedIn' in session:
        if session["loggedIn"] == True:


            form = ApplicationUploadForm()
            if form.validate_on_submit():
                if 'submit' in request.form:
                    f=form.upload.data
                    application=str(form.application.data)


                    filename = secure_filename(f.filename)

                    temp=(webapp.instance_path).split('\\')
                    temp=temp[:-1]
                    s='\\'
                    final_path=s.join(temp)
                    file_path=final_path+"\\app\\static\\Input\\"
                    file_name=session["accountName"] +'_'+application+ '_' + (str(time.time())).replace('.', '_') + '_' + filename

                    final_path = os.path.join(webapp.root_path, 'static/Applications/' + file_name)
                    f.save(final_path)

                    if os.path.isfile(final_path):
                        os.remove(final_path)
            return render_template("Home.html",form=form)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@webapp.route('/monitor_page', methods=['GET', 'POST'])
def monitor_page():
    return render_template("monitor.html")

@webapp.route('/alert_page', methods=['GET', 'POST'])
def alert_page():
    return render_template("alert.html")

@webapp.route('/dashboard_page', methods=['GET', 'POST'])
def dashboard_page():
    return render_template("dashboard.html")

@webapp.route('/administrator_page', methods=['GET', 'POST'])
def admin_page():
    return render_template("administrator.html")




@webapp.route('/register_page', methods=['GET', 'POST'])
def register_page():
    session["loggedIn"] = False
    session["currentUser"] = ""
    session["access_level"] = ""
    session["accountName"] = ""
    form2 = RegistrationForm()
    if form2.validate_on_submit():
        #print("hello")
        account = str(form2.account.data)
        password = str(form2.password.data)
        if form2.validateAccountname(account)==0:
            error="Sorry the Account already exist!"
            flash(error)
            return render_template("register.html", form=form2, error=error)
        else:

            #hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            database.create_account(account)
            database.insert_into_users(account,'root',password,'3')


            success="Congrats! New User Created!"

            return render_template("register.html", form=form2, success=success)


    return render_template("register.html", form=form2,error="")

@webapp.route('/api/register', methods=['POST'])
def add_user():
    error = []
    if ('username' in request.args) and ('password' in request.args):
        username= str(request.args['username'])
        password=str(request.args['password'])
        if len(username)>=4 and len(username)<=100:
            pass
        else:
            error.append("Error: Invalid Username (Username Length 4-100 charecters)")
        if len(password)>=4 and len(password)<=20:
            pass
        else:
            error.append("Error: Invalid Password (Password Length 4-20 charecters)")
        if len(error)==0:
            hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
            check=databaseModule.verify_username_password(username, hashed_password)
            if check == -1:
                databaseModule.insert_user_database(username, hashed_password)
            else:
                error.append("Error: Username Already Exist")
        operation_done=databaseModule.verify_username_password(username,password)
        if operation_done!=1:
            error.append("Error: User Not Added to Database")
    elif ('username' in request.form) and ('password' in request.form):
        username = str(request.form['username'])
        password = str(request.form['password'])
        if len(username) >= 4 and len(username) <= 100:
            pass
        else:
            error.append("Error: Invalid Username (Username Length 4-100 charecters)")
        if len(password) >= 4 and len(password) <= 20:
            pass
        else:
            error.append("Error: Invalid Password (Password Length 4-20 charecters)")
        if len(error) == 0:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            check = databaseModule.verify_username_password(username, hashed_password)
            if check == -1:
                databaseModule.insert_user_database(username, hashed_password)
            else:
                error.append("Error: Username Already Exist")
        operation_done = databaseModule.verify_username_password(username, password)
        if operation_done != 1:
            error.append("Error: User Not Added to Database")


    else:
        error.append("Error: Missing Parameter")


    if len(error)==0:
        statusCode=201
        error.append("Success: User created")
    else:
        if ("Error: Invalid Password (Password Length 4-100 charecters)" in error) or ("Error: Invalid Password (Password Length 4-20 charecters)" in error):
            statusCode = 406
        elif "Error: Username Already Exist" in error:
            statusCode = 406
        else:
            statusCode =500
    return jsonify(error=error),statusCode

