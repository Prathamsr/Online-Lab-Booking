import json
from flask import Blueprint, Flask,render_template,request,flash,redirect,url_for
from .data import Institute_information, Lab_names, User,Institute
from werkzeug.security import generate_password_hash, check_password_hash
from . import bd,app
from .verification import verification
from flask_login import login_user,login_required,logout_user,current_user
import os
from werkzeug.utils import secure_filename
import uuid as uuid
import random
import website
views= Blueprint('views',__name__)

profile_pic=''
email=''
firstname=''
password1=''
latitude=''
longitude=''
state=''
city=''
degree_persuing=''
parent_institute=''
pic_profile=''
@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.home'))

@views.route('/login',methods=['get','POST'])
def login():
    if request.method=='POST':
        if request.method=='POST':
            given_email = request.form.get('email')
            given_password=request.form.get('password1')
            user=User.query.filter_by(email=given_email).first()
            institute=Institute.query.filter_by(email=given_email).first()
            if user:
                if check_password_hash(user.password,given_password):
                    login_user(user,remember=True)
                    return redirect(url_for(f'auth.home'))
                else:
                    flash('Incorrect password, try again', category='error')
            elif institute:
                if check_password_hash(institute.password,given_password):
                    login_user(institute,remember=True)
                    print(current_user.id)
                    return redirect(url_for(f'auth.home'))
                else:
                    flash('Incorrect password, try again', category='error')

            else:
                flash('User does not exists, sign up', category='error')
    return render_template("login.html")
@views.route('/signup', methods=['get','POST'])
def signup():
    if request.method=='POST':
        global email,firstname,password1,password2,degree_pursuing,parent_institute,pic_profile
        email = request.form.get('email')
        profile_pic=request.files['profile_pic']
        firstname= request.form.get('firstname')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        degree_pursuing=request.form.get('degree_pursuing')
        parent_institute=request.form.get('parent_institute')
        data= request.form
        print(data)
        pro=profile_pic.filename.split('.')
        pic_profile=str(uuid.uuid1())+'.'+pro[-1]
        prath=os.path.join(app.config['Upload_folder'],pic_profile)
        profile_pic.save(prath)
        user=User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists',category='error')
        if len(email)<5:
            flash("Email is not valid",category='error')
        elif len(firstname)<2:
            flash('First name is too small',category='error')
        elif len(password1)<6:
            flash('Password must be greater than 5 characters',category='error')
        elif password1!=password2:
            flash("Passwords don't match",category='error')
        else:
            return redirect(url_for('views.verification'))         
    return render_template("signup.html")
@views.route('/signupasins', methods=['GET','POST'])
def signupasins():
    if request.method=='POST':
        global email,firstname,password1,password2,latitude,longitude,state,city,pic_profile
        email = request.form.get('email')
        profile_pic=request.files['profile_pic']
        firstname= request.form.get('name')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        latitude=request.form.get('latitude')
        longitude=request.form.get('longitude')
        state=request.form.get('state')
        city=request.form.get('city')
        pro=profile_pic.filename.split('.')
        pic_profile=str(uuid.uuid1())+'.'+pro[-1]
        prath=os.path.join(app.config['Upload_folder'],pic_profile)
        profile_pic.save(prath)
        data= request.form
        print(data)
        user=Institute.query.filter_by(email=email).first()
        if user:
            flash('Email already exists',category='error')
        elif len(email)<5:
            flash("Email is not valid",category='error')
        elif len(firstname)<2:
            flash('First name is too small',category='error')
        elif len(password1)<6:
            flash('Password must be greater than 5 characters',category='error')
        elif password1!=password2:
            flash("Passwords don't match",category='error')
        else:
            return redirect(url_for('views.insverification'))
    return render_template("signupasins.html")
@views.route('/verification',methods=['GET','POST'])
def verification():
    global email,firstname,password1,password2,degree_pursuing,parent_institute,pic_profile
    otp='12345'
    if request.method=='POST':
        given_otp=request.form.get('otp')
        if otp==str(given_otp):
            a=email.split('@')
            new_user=User(id=random.randint(111111,999999), email=email, 
            firstname=firstname, 
            type='user',
            username=a[0],
            profile_pic='/static/upload/'+pic_profile,
            degree_pursuing=degree_pursuing,
            parent_institute=parent_institute,
            password=generate_password_hash(password1,method="sha256"))
            bd.session.add(new_user)
            bd.session.commit()
            login_user(new_user,remember=True)
            return redirect(url_for(f'auth.home'))
    return render_template('verification.html',mail=email)
@views.route('/insverification',methods=['GET','POST'])
def insverification():
    otp='12345'
    if request.method=='POST':
        global email,firstname,password1,password2,latitude,longitude,state,city,pic_profile
        given_otp=request.form.get('otp')
        if otp==str(given_otp):
            with open('website/static/javascript/insname.json','r') as f:
                l=json.load(f)
            l.append(firstname)
            with open('website/static/javascript/insname.json','w') as f:
                json.dump(l,f)
            new_user=Institute( id=random.randint(111111,999999),email=email,
            name=firstname,
            type='institute',
            profile_pic='/static/upload/'+pic_profile,
            password=generate_password_hash(password1,method="sha256"),
            latitude=latitude,
            longitude=longitude,
            state=state,
            city=city)
            bd.session.add(new_user)
            bd.session.commit()
            login_user(new_user,remember=True)
            return redirect(url_for('views.information'))
    return render_template('verification.html',mail=email)
@views.route('/information',methods=['GET','POST'])
@login_required
def information():
    if request.method=='POST':
        data=dict(request.form)
        print(data)
        if data['sec_off_name']=='':
            info=Institute_information(id=random.randint(111111,999999),primary_office=data['pri_off_name'],
            primary_office_city=data['pri_off_city'],
            primary_office_address=data['pri_off_add'],
            primary_address=data['Pri_address'],
            email=data['email'],
            Website=data['website'],
            Contact_no=data['contact'],
            institute_id=current_user.id,
            speciality=data['speciality'])
            bd.session.add(info)
            bd.session.commit()
        else:
            info=Institute_information(id=random.randint(111111,999999),primary_office=data['pri_off_name'],
            primary_office_city=data['pri_off_city'],
            primary_office_address=data['pri_off_add'],
            primary_address=data['Pri_address'],
            secondary_office=data['sec_off_name'],
            secondary_office_city=data['sec_off_city'],
            secondary_office_address=data['sec_off_add'],
            email=data['email'],
            Website=data['website'],
            Contact_no=data['contact'],
            institute_id=current_user.id,
            speciality=data['speciality'])
            bd.session.add(info)
            bd.session.commit()
        for i in data.keys():
            if i.startswith('lab'):
                if data[i]!='':
                    labs=Lab_names(id=random.randint(111111,9999999),name=data[i],institute_information_id=info.id)
                    bd.session.add(labs)
                    bd.session.commit()
        return redirect(url_for('auth.home'))
    return render_template('information.html')



