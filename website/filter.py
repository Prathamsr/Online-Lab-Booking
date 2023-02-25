from . import bd
import haversine
from .data import *
import datetime
class Filter:
    def __init__(self,lab,latitute,longitute,date,distance,city):
        self.lab=lab
        self.latitude=latitute
        self.longitude=longitute
        self.date=date
        self.distance=distance
        self.city=city
        self.posts=Institutedata.query.filter_by(lab_name=self.lab).all()
    def run(self):
        self.date_required()
    def date_required(self):
        for i in self.posts:
            print(i.starting_date,self.date,i.ending_date)
            if i.starting_date<self.date<i.ending_date:
                print('pkay')
                print(self.posts)
                pass
            else:
                print('not okay')
                self.posts.remove(i)
                print(self.posts)
        if self.distance!='':
            print('dis')
            self.required_distance()
        if self.city!='':
            print('city')
            self.find_city()
    def find_city(self):
        print(self.posts)
        print('hello')
        for i in self.posts:
            print('hellllllll')
            print(i.instituteref.city,'6363636336')
            if str(i.instituteref.city).lower()==str(self.city).lower():
                pass
            else:
                print(self.city)
                self.posts.remove(i)
    def required_distance(self):
        for i in self.posts:
            user=(self.latitude,self.longitude)
            ins=(i.instituteref.latitude,i.instituteref.longitude)
            dis=haversine.haversine(user,ins)
            print(self.posts)
            
            if self.distance<dis:
                print(dis)
                self.posts.remove(i)
        
class Create_date:
    def __init__(self,object):
        self.object=object
        self.find_date()
        self.timing=Timming.query.filter_by(institutedata_id=self.object.id).first()
    def find_date(self):
        pending_requests_total=Pending_requests.query.filter_by(institutedata_id=self.object.id)
        confirm_requests=Confirm_payment.query.filter_by(institutedata_id=self.object.id).all()
        start=self.object.starting_date
        try:
            length=len(pending_requests_total)+len(confirm_requests)
        except:
            length=0
        if length>0:
            no_of_slots=self.object.no_of_slots_per_lab
            no_of_labs_per_day=self.timing.no_of_labs
            total_slots=no_of_labs_per_day*no_of_slots
            while True:
                if length>total_slots:
                    start=start+datetime.timedelta(days=1)
                    length=length-total_slots
                else:
                    break
        dates=[]
        while start<=self.object.ending_date:
            da=str(start).split(" ")
            da=da[0].split("-")
            dates.append(da)
            start=start+datetime.timedelta(days=1)
        print("hell",dates)
        self.dates=dates
    def givetiming(self,date):
        pending_requests_total=Pending_requests.query.filter_by(institutedata_id=self.object.id).all()
        confirm_requests=Confirm_payment.query.filter_by(institutedata_id=self.object.id).all()
        start=self.object.starting_date
        starting_time=self.timing.starting_of_lab
        length=len(pending_requests_total)+len(confirm_requests)
        if length>0:
            no_of_slots=self.object.no_of_slots_per_lab
            no_of_labs_per_day=self.timing.no_of_lab
            total_slots=no_of_labs_per_day+no_of_slots
            while True:
                if length>total_slots:
                    start=start+datetime.timedelta(days=1)
                    length=length-total_slots
                else:
                    while True:
                        if length>no_of_slots:
                            length=length-no_of_slots
                            starting_time=starting_time+datetime.timedelta(hours=self.y.duration_of_lab)
                        else:
                            break
                    break    
        return starting_time
        
    
    