from flask import render_template, url_for, request, jsonify , flash, redirect, request,session
from app import webapp
from app import AWS_SECRET_KEY, AWS_ACCESS_KEY
from app.forms import LoginForm,RegistrationForm, ApplicationUploadForm, ApplicationSelection, addUser
from app.forms import ResourceSelection
import hashlib
import datetime
from app import database


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
            form2 = ApplicationSelection()
            form2.application.choices = [('1', 'Omo'),('2', 'Omo2')]
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
                    file_path=final_path+"\\app\\static\\Applications\\"
                    file_name=session["accountName"] +'_'+application+ '_' + (str(time.time())).replace('.', '_') + '_' + filename

                    final_paths = file_path + file_name
                    print(final_paths)
                    f.save(final_paths)
                    node_data=resources.parse_applictaion_properties(final_paths)
                    node_list=node_data["Node list"]
                    for node in node_list:
                        database.insert_into_nodes(str(session["accountName"]), int(node["Node ID"]), node["Node Type"], application)
                        database.insert_into_applications(str(session["accountName"]),application,final_paths)

            return render_template("Home.html",form=form,form2=form2)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@webapp.route('/monitor_page', methods=['GET', 'POST'])
def monitor_page():
    if 'loggedIn' in session:
        if session["loggedIn"] == True:
            form = ResourceSelection()
            form.application.choices = [('1', 'Omo'),('2', 'Omo2')]
            form.node.choices = [('1', 'Omo'), ('2', 'Omo2')]
            form.metric.choices = [('1', 'Omo'), ('2', 'Omo2')]



            if form.validate_on_submit():
                if 'submit' in request.form:
                    a=0

            return  render_template("monitor.html",form=form)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@webapp.route('/alert_page', methods=['GET', 'POST'])
def alert_page():
    if 'loggedIn' in session:
        if session["loggedIn"] == True:
            form = ResourceSelection()
            form.application.choices = [('1', 'Omo'),('2', 'Omo2')]
            form.node.choices = [('1', 'Omo'), ('2', 'Omo2')]
            form.metric.choices = [('1', 'Omo'), ('2', 'Omo2')]



            if form.validate_on_submit():
                if 'submit' in request.form:
                    a=0

            return  render_template("alert.html",form=form)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    return render_template("alert.html")

@webapp.route('/dashboard_page', methods=['GET', 'POST'])
def dashboard_page():
    return render_template("dashboard.html")

@webapp.route('/administrator_page', methods=['GET', 'POST'])
def admin_page():
    form=addUser()
    list_user=[{'name':'Pranav Naidu','username':'pranav.naidu','password':'hello', 'access_level':'3'},
               {'name':'Badriveer Thota','username':'badri','password':'hello', 'access_level':'1'},
               {'name':'Kratagya Dixit','username':'kayD','password':'hello', 'access_level':'2'},
               {'name':'Jenny Li','username':'jenny.li','password':'hello', 'access_level':'1'},
               {'name':'Andy Birla','username':'andy.birla','password':'hello', 'access_level':'2'}]

    return render_template("administrator.html",form=form,user_list=list_user)




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

            database.create_account(account)
            database.insert_into_users(account,'root',password,'3')


            success="Congrats! New User Created!"

            return render_template("register.html", form=form2, success=success)


    return render_template("register.html", form=form2,error="")

