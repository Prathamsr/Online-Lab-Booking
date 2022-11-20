from flask import Blueprint,render_template,request, url_for,redirect
from flask_login import login_required,current_user
from . import app
import os
import uuid
from .data import *
import datetime
import json
import random
from .filter import Create_date, Filter
from .request import confirm_request
auth= Blueprint('auth',__name__)

@auth.route('/', methods=['GET','POST'])
def home():
    if request.method=='POST':
        data= dict(request.form)
        req_date=data['date'].split('-')
        print(data)
        req_date=datetime.datetime(int(req_date[0]),int(req_date[1]),int(req_date[2]))
        post=Filter(lab=data['labs'],latitute=float(data['latitude']),longitute=float(data['longitude']),date=req_date,distance=int(data['distance']),city=data['city'])
        post.run()
        print(post.posts)
        with open('website/lab_name_present.json','r') as f:
                l=json.load(f)
        return render_template('home.html',labs=post.posts,labnames=l)
    lab_random=[]
    all_post=Institutedata.query.all()
    for i in range(6):
        a=random.choice(all_post)
        all_post.remove(a)
        lab_random.append(a)
    with open('website/lab_name_present.json','r') as f:
                l=json.load(f)

    return render_template('home.html',labs=lab_random,labnames=l,user=current_user)

@auth.route('/requests',methods=['GET','POST'])
@login_required
def user_requests():
    pen=Pending_requests.query.filter_by(user_id=current_user.id).all()
    ilab=Pending_requests_institute.query.filter_by(user_id=current_user.id).all()
    return render_template('student.html',lab=pen,ins=ilab)


@auth.route('/upload' ,methods=['POST','GET'])
@login_required
def upload_data():
    if current_user.type=='institute':
        if request.method=='POST':
            data=dict(request.form)
            profile_pic=request.files['profile_pic']
            pro=profile_pic.filename.split('.')
            pic_profile=str(uuid.uuid1())+'.'+pro[-1]
            prath=os.path.join(app.config['Upload_folder'],pic_profile)
            profile_pic.save(prath)
            starting_date=data['starting_date'].split('-')
            starting_date=datetime.datetime(int(starting_date[0]),int(starting_date[1]),int(starting_date[2]))
            ending_date=data['ending_date'].split('-')
            ending_date=datetime.datetime(int(ending_date[0]),int(ending_date[1]),int(ending_date[2]))
            starting_of_lab=data['starting_of_lab'].split(':')
            starting_of_lab=datetime.datetime(2022,1,1,int(starting_of_lab[0]),int(starting_of_lab[1]),0)
            print(data,starting_date,ending_date,starting_of_lab)
            with open('website/lab_name_present.json','r') as f:
                l=json.load(f)
                if data['lab_name'].capitalize() not in l:
                    l.append(data['lab_name'].capitalize())
                    l.sort()
                    with open('website/lab_name_present.json','w') as f:
                        json.dump(l,f)
            post=Institutedata( lab_name=data['lab_name'].capitalize(),
            image='/static/upload/'+pic_profile,
            discription=data['discription_about_lab'],
            date_posted=datetime.datetime.now(),
            starting_date=starting_date,
            ending_date=ending_date,
            no_of_slots_per_lab=int(data['no_of_slots']),
            charge_per_slot=int(data['charge_per_slot']),
            institute_id=current_user.id)
            bd.session.add(post)
            bd.session.commit()
            time=Timming(starting_of_lab=starting_of_lab,
            duration_of_lab=int(data['duration_of_lab']),
            no_of_lab=int(data['no_of_lab_per_day']),
            institutedata_id=post.id)
            bd.session.add(time)
            bd.session.commit()
            return redirect(url_for('auth.home'))
        return render_template('postupload.html')
    else:
        return redirect(url_for('views.signupasins'))

@auth.route('/workshop')
def upload_workshop(institute):
    return render_template('workshopupload.html')

@auth.route('/search')
def search_result():
    return render_template('search.html')


@login_required
@auth.route('/setting')
def user_secting(user):
    return render_template('usersetteng')

@auth.route('/<post_id>/request',methods=['GET','POST'])
@login_required
def send_institute_request(post_id):
    lab=Institutedata.query.get(int(post_id))
    req_date=Create_date(lab)
    print(req_date.dates)
   
    if request.method=='POST':
        data=dict(request.form)
        print(data)
        if data['book_method']=='user_book':
            profile_pic=request.files['profile_pic']
            pro=profile_pic.filename.split('.')
            pic_profile=str(uuid.uuid1())+'.'+pro[-1]
            prath=os.path.join(app.config['Upload_folder'],pic_profile)
            profile_pic.save(prath)
            date=data['date'].split('-')
            date=datetime.datetime(int(date[2]),int(date[1]),int(date[0]))
            for i in range(int(data['number-of-slot-booked'])):
                hello=req_date.givetiming(date)
                obj=Pending_requests(date=date,
                time=hello,
                verification_id='/static/upload/'+pic_profile,
                institutedata_id=post_id,
                user_id=current_user.id)
                bd.session.add(obj)
                bd.session.commit()
        else:
            date=data['date'].split('-')
            date=datetime.datetime(int(date[2]),int(date[1]),int(date[0]))
            hello=req_date.givetiming(date)
            obj=Pending_requests_institute(date=date,
            time=hello,
            no_of_slots=int(data['number-of-slot-booked']),
            institutedata_id=post_id,
            user_id=current_user.id)
            bd.session.add(obj)
            bd.session.commit()

        return redirect(url_for('auth.user_requests'))
    return render_template('request.html',date=req_date.dates,post=lab)


@auth.route('/<insname>/profile')
def search_profile(insname):
    pro=Institute.query.filter_by(name=insname).first()
    if pro:
        info=Institute_information.query.filter_by(institute_id=pro.id).first()
        posts=Institutedata.query.filter_by(institute_id=pro.id).all()
        if info:
            lab_offer=Lab_names.query.filter_by(institute_information_id=info.id).all()
            return render_template('s.html',insti=pro,labs=lab_offer,data=info,post=posts)
        else:
            return render_template('s.html',insti=pro,labs=[1,2],data=[],post=posts)
    else:
        return "Institute does not provide lab on this platform"
@auth.route('/profile')
@login_required
def profile():
    
    info=Institute_information.query.filter_by(institute_id=current_user.id).first()
    posts=Institutedata.query.filter_by(institute_id=current_user.id).all()
    if info:
        lab_offer=Lab_names.query.filter_by(institute_information_id=info.id).all()
        for i in posts:
            pass
        return render_template('s.html',insti=current_user,labs=lab_offer,data=info,post=posts)
    return render_template('s.html',insti=current_user,labs=[1,2,3],data=info,post=posts)
