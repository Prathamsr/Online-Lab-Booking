from . import bd
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(bd.Model, UserMixin):
    id = bd.Column(bd.Integer, primary_key=True)
    username=bd.Column(bd.String(150), unique=True)
    type=bd.Column(bd.String(20))
    profile_pic=bd.Column(bd.String(250))
    firstname=bd.Column(bd.String(150))
    email= bd.Column(bd.String(150), unique=True)
    password=bd.Column(bd.String(500))
    degree_pursuing=bd.Column(bd.String(150))
    parent_institute=bd.Column(bd.String(150))
    upcoming_labs=bd.relationship('Userdata',backref='userref')
    pending_requests=bd.relationship('Pending_requests',backref='userref')

    confirm_payment=bd.relationship('Confirm_payment',backref='userref')

class Institute(bd.Model, UserMixin):
    id = bd.Column(bd.Integer, primary_key=True)
    email= bd.Column(bd.String(150), unique=True)
    type=bd.Column(bd.String(20))
    name=bd.Column(bd.String(300))
    profile_pic=bd.Column(bd.String(200))
    password=bd.Column(bd.String(150))
    latitude=bd.Column(bd.Float)
    longitude=bd.Column(bd.Float)
    state=bd.Column(bd.String(150))
    city=bd.Column(bd.String(150))
    posted_information=bd.relationship('Institutedata',backref="instituteref")
    posted_workshop=bd.relationship('Workshop_information',backref="instituteref")
    institute_information=bd.relationship('Pending_requests_institute',backref='instituteref')

class Institute_information(bd.Model):
    id=bd.Column(bd.Integer, primary_key=True)
    primary_office=bd.Column(bd.String(200))
    primary_office_city=bd.Column(bd.String(100))
    primary_office_address=bd.Column(bd.String(200))
    secondary_office=bd.Column(bd.String(200),nullable=True)
    secondary_office_city=bd.Column(bd.String(100),nullable=True)
    secondary_office_address=bd.Column(bd.String(200),nullable=True)
    speciality=bd.Column(bd.String(150),nullable=True)
    Contact_no=bd.Column(bd.Integer)
    primary_address=bd.Column(bd.String(200))
    email=bd.Column(bd.String(150))
    Website=bd.Column(bd.String(200),nullable=True)
    institute_id=bd.Column(bd.Integer, bd.ForeignKey('institute.id'))
    lab_name=bd.relationship('Lab_names',backref='inforef')


class Lab_names(bd.Model):
    id=bd.Column(bd.Integer, primary_key=True)
    name=bd.Column(bd.String(150))
    institute_information_id=bd.Column(bd.Integer, bd.ForeignKey('institute_information.id'))

class Workshop_information(bd.Model):
    id=bd.Column(bd.Integer,primary_key=True)
    pic=bd.column(bd.LargeBinary)
    description=bd.column(bd.String(500))
    date_of_workshop=bd.Column(bd.DateTime(timezone=True))
    date_posted=bd.Column(bd.DateTime(timezone=True) ,default=func.now())
    no_of_slots=bd.Column(bd.Integer)
    minimum_slots_to_be_filled=bd.Column(bd.Integer)
    charge_per_slot=bd.Column(bd.Integer)
    institute_id=bd.Column(bd.Integer, bd.ForeignKey('institute.id'))
    
class Institutedata(bd.Model):
    id=bd.Column(bd.Integer, primary_key=True)
    lab_name=bd.Column(bd.String(150))
    image=bd.Column(bd.String(200))
    discription=bd.Column(bd.String(500))
    date_posted=bd.Column(bd.DateTime(timezone=True) ,default=func.now())
    starting_date=bd.Column(bd.DateTime(timezone=True))
    ending_date=bd.Column(bd.DateTime(timezone=True))
    no_of_slots_per_lab=bd.Column(bd.Integer)
    charge_per_slot=bd.Column(bd.Integer)
    institute_id=bd.Column(bd.Integer, bd.ForeignKey('institute.id'))
    timmings=bd.relationship('Timming',backref='institutedataref')
    pending_requests=bd.relationship('Pending_requests',backref='insdataref')
    pending_requests_institute=bd.relationship('Pending_requests_institute',backref='insdataref')
    confirm_payment=bd.relationship('Confirm_payment',backref='insdataref')


class Userdata(bd.Model):
    id=bd.Column(bd.Integer, primary_key=True)
    name_of_institute=bd.Column(bd.String(300))
    name_of_lab=bd.Column(bd.String(150))
    date_of_practical=bd.Column(bd.DateTime(timezone=True))
    no_of_slots_booked=bd.Column(bd.Integer)
    payment_verified=bd.Column(bd.Boolean , default=False)
    user_id=bd.Column(bd.Integer,bd.ForeignKey('user.id'))

class Timming(bd.Model):
    id=bd.Column(bd.Integer,primary_key=True)
    starting_of_lab=bd.Column(bd.DateTime(timezone=True))
    duration_of_lab=bd.Column(bd.Integer)
    no_of_lab=bd.Column(bd.Integer)
    institutedata_id=bd.Column(bd.Integer,bd.ForeignKey('institutedata.id'))


class Pending_requests(bd.Model):
    id=bd.Column(bd.Integer,primary_key=True)
    date=bd.Column(bd.DateTime(timezone=True))
    time=bd.Column(bd.DateTime(timezone=True))
    verification_id=bd.Column(bd.String(200))
    institutedata_id=bd.Column(bd.Integer,bd.ForeignKey('institutedata.id'))
    user_id=bd.Column(bd.Integer,bd.ForeignKey('user.id'))

class Pending_requests_institute(bd.Model):
    id=bd.Column(bd.Integer,primary_key=True)
    date=bd.Column(bd.DateTime(timezone=True))
    time=bd.Column(bd.DateTime(timezone=True))
    no_of_slots=bd.Column(bd.Integer)
    institutedata_id=bd.Column(bd.Integer,bd.ForeignKey('institutedata.id'))
    user_id=bd.Column(bd.Integer,bd.ForeignKey('institute.id'))

class Confirm_payment(bd.Model):
    id=bd.Column(bd.Integer,primary_key=True)
    user=bd.Column(bd.String(150))
    lab=bd.Column(bd.String(150))
    date=bd.Column(bd.DateTime(timezone=True))
    time=bd.Column(bd.DateTime(timezone=True))
    institutedata_id=bd.Column(bd.Integer,bd.ForeignKey('institutedata.id'))
    user_id=bd.Column(bd.Integer,bd.ForeignKey('user.id'))