from flask import Blueprint,render_template,request, url_for,redirect,flash
from flask_login import login_required,current_user
from . import app
import os
import uuid
from .data import *
import datetime
import json
import random
from .filter import Create_date, Filter
#from .request import confirm_request
auth= Blueprint('auth',__name__)

@auth.route('/', methods=['GET','POST'])
def home():
    insti=Institute.query.all()
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
        return render_template('home.html',labs=post.posts,labnames=l,user=current_user,institutes=insti)
    lab_random=[]
    all_post=Institutedata.query.all()
    for i in range(10):
        a=random.choice(all_post)
        all_post.remove(a)
        lab_random.append(a)
    with open('website/lab_name_present.json','r') as f:
                l=json.load(f)
                
    
    return render_template('home.html',labs=lab_random,labnames=l,user=current_user ,institutes=insti)

@auth.route('/requests',methods=['GET','POST'])
@login_required
def user_requests():
    pen=Pending_requests.query.filter_by(user_id=current_user.id).all()
    ilab=Confirm_payment.query.filter_by(user_id=current_user.id).all()
    for i in range(len(pen)):
        a=str(pen[i].time).split(' ')
        dd=str(pen[i].date).split(' ')
        a=a[1].split(":")
        dd=dd[0].split("-")
        date=datetime.datetime(int(dd[0]),int(dd[1]),int(dd[2]),int(a[0]),int(a[1]),int(a[2]))
        pen[i].time=date
    for i in range(len(ilab)):
        a=str(ilab[i].time).split(' ')
        dd=str(ilab[i].date).split(' ')
        a=a[1].split(":")
        dd=dd[0].split("-")
        date=datetime.datetime(int(dd[0]),int(dd[1]),int(dd[2]),int(a[0]),int(a[1]),int(a[2]))
        ilab[i].time=date
    
    return render_template('student.html',lab=ilab,ins=pen)


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
            post=Institutedata( id=random.randint(111111,999999),lab_name=data['lab_name'].capitalize(),
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
            time=Timming(id=random.randint(111111,999999),starting_of_lab=starting_of_lab,
            duration_of_lab=int(data['duration_of_lab']),
            no_of_lab=int(data['no_of_lab_per_day']),
            institutedata_id=post.id)
            bd.session.add(time)
            bd.session.commit()
            return redirect(url_for('auth.home'))
        return render_template('postupload.html')
    else:
        return redirect(url_for('views.signupasins'))
@auth.route('/<post_id>/delete_post')
@login_required
def delete_post(post_id):
    post=Institutedata.query.get(int(post_id))
    if post.institute_id==current_user.id:
        pend=Pending_requests.query.filter_by(institutedata_id=int(post_id)).all()
        conf=Confirm_payment.query.filter_by(institutedata_id=int(post_id)).all()
        for i in pend:
            bd.session.delete(i)
        for i in conf:
            bd.session.delete(i)
        bd.session.delete(post)
        bd.session.commit()
    return redirect(url_for("auth.profile"))

@auth.route('/<post_id>/delete_post_user',methods=['POST'])
@login_required
def delete_post_user(post_id):
    post=Pending_requests.query.get(int(post_id))
    if post.user_id==current_user.id:
        bd.session.delete(post)
        bd.session.commit()
    return redirect(url_for("auth.user_requests"))

@auth.route('/<post_id>/conformation')
@login_required
def conformation(post_id):
    post=Institutedata.query.get(int(post_id))
    lab=Pending_requests.query.filter_by(institutedata_id=int(post_id)).all()
    return render_template('conformation.html',labs=lab,posts=post)

@auth.route("/<post_id>/confirmed")
@login_required
def confirmed(post_id):
    post=Institutedata.query.get(int(post_id))
    lab=Confirm_payment.query.filter_by(institutedata_id=int(post_id)).all()
    return render_template('conformed.html',labs=lab,posts=post)

@auth.route('/<req_id>/confirm',methods=['GET','POST'])
@login_required
def confirm_req(req_id):
    if request.method=='POST':
        lab=Pending_requests.query.get(int(req_id))
        if lab.insdataref.institute_id==current_user.id:
            new_con_req=Confirm_payment(id=random.randint(111111,999999),
            user=lab.userref.username,
            lab=lab.insdataref.lab_name,
            verification_id=lab.verification_id,
            date=lab.date,
            time=lab.time,
            institutedata_id=lab.institutedata_id,
            user_id=lab.user_id
            )
            bd.session.add(new_con_req)
            bd.session.delete(lab)
            bd.session.commit()
    return redirect(f"/{lab.institutedata_id}/conformation")

@auth.route("/<post_id>/confirm_all",methods=['post'])
@login_required
def confirm_all(post_id):
    post=Institutedata.query.get(int(post_id))
    if current_user.id==post.institute_id:
        request=Pending_requests.query.filter_by(institutedata_id=post.id).all()
        for i in request:
            lab=i
            new_con_req=Confirm_payment(id=random.randint(111111,999999),
            user=lab.userref.username,
            lab=lab.insdataref.lab_name,
            verification_id=lab.verification_id,
            date=lab.date,
            time=lab.time,
            institutedata_id=lab.institutedata_id,
            user_id=lab.user_id
            )
            bd.session.add(new_con_req)
            bd.session.delete(lab)
            bd.session.commit()
    return redirect(f"/{post_id}/confirmed")


@auth.route('/<req_id>/delete',methods=['GET','POST'])
@login_required
def delete_req(req_id):
    if request.method=='POST':
        lab=Pending_requests.query.get(int(req_id))
        if current_user.type=='user':
            if lab.user_id==current_user.id:
                bd.session.delete(lab)
                bd.session.commit()
            return redirect(url_for('auth.user_requests'))
        else:
            if lab.insdataref.institute_id==current_user.id:
                bd.session.delete(lab)
                bd.session.commit()
            return redirect(f"/{lab.institutedata_id}/confirmed")
    return redirect("/")

@auth.route('/<post_id>/request',methods=['GET','POST'])
@login_required
def send_institute_request(post_id):
    if current_user.type=="user":
        lab=Institutedata.query.get(int(post_id))
        req_date=Create_date(lab)
        print(req_date.dates)
   
        if request.method=='POST':
            data=dict(request.form)
            print(data)
            profile_pic=request.files['profile_pic']
            pro=profile_pic.filename.split('.')
            pic_profile=str(uuid.uuid1())+'.'+pro[-1]
            prath=os.path.join(app.config['Upload_folder'],pic_profile)
            profile_pic.save(prath)
            date=data['date'].split('-')
            date=datetime.datetime(int(date[2]),int(date[1]),int(date[0]))
            for i in range(int(data['number-of-slot-booked'])):
                hello=req_date.givetiming(date)
                obj=Pending_requests(id=random.randint(111111,999999),date=date,
                time=hello,
                verification_id='/static/upload/'+pic_profile,
                institutedata_id=post_id,
                user_id=current_user.id)
                bd.session.add(obj)
                bd.session.commit()
            return redirect(url_for('auth.user_requests'))
        return render_template('request.html',date=req_date.dates[:5],post=lab)
    else:
        flash('SignUp as Student', category='warning')
        return redirect (url_for("views.signup"))
            

@auth.route('/search')
def search_result():
    return render_template('search.html')

@auth.route('/<insname>/profile')
def search_profile(insname):
    pro=Institute.query.filter_by(name=insname).first()
    if pro:
        info=Institute_information.query.filter_by(institute_id=pro.id).first()
        posts=Institutedata.query.filter_by(institute_id=pro.id).all()
        if info:
            lab_offer=Lab_names.query.filter_by(institute_information_id=info.id).all()
            return render_template('searchprofile.html',insti=pro,labs=lab_offer,data=info,post=posts)
        else:
            return render_template('searchprofile.html',insti=pro,labs=[1,2],data=[],post=posts)
    else:
        return "Institute does not provide lab on this platform"

@auth.route('/<name>/user')
def user_profile(name):
    user=User.query.filter_by(username=name).first()
    if user:
        posts=Pending_requests.query.filter_by(user_id=user.id).all()
        posts_con=Confirm_payment.query.filter_by(user_id=user.id).all()
        posts=posts+posts_con
        print(posts)
        lab=[]
        for i in posts:
            curr=i.insdataref.lab_name
            if curr not in lab:
                lab.append(curr)
        print(lab)
        return render_template("userprofile.html",insti=user,labs=lab)
    else:
        return "User does not exist"

@auth.route('/profile')
@login_required
def profile():
    if current_user.type=="user":
        posts=Pending_requests.query.filter_by(user_id=current_user.id).all()
        posts_con=Confirm_payment.query.filter_by(user_id=current_user.id).all()
        posts=posts+posts_con
        print(posts)
        lab=[]
        for i in posts:
            curr=i.insdataref.lab_name
            if curr not in lab:
                lab.append(curr)
        print(lab)
        return render_template("userprofile.html",insti=current_user,labs=lab)
    else:    
        info=Institute_information.query.filter_by(institute_id=current_user.id).first()
        posts=Institutedata.query.filter_by(institute_id=current_user.id).all()
        if info:
            lab_offer=Lab_names.query.filter_by(institute_information_id=info.id).all()
            return render_template('s.html',insti=current_user,labs=lab_offer,data=info,post=posts)
        return render_template('s.html',insti=current_user,labs=[1,2,3],data=info,post=posts)
