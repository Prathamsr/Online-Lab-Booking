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
    def find_date(self):
        self.dates=[]
        a=self.object.starting_date
        while a<=self.object.ending_date:
            x=Pending_requests.query.filter_by(date=a).all()
            k=Pending_requests_institute.query.filter_by(date=a).all()
            add=0
            if len(k)>0:
                for i in k:
                    add=add+i.no_of_slots
            self.y=Timming.query.filter_by(institutedata_id=self.object.id).first()
            try:
                if (len(x)+add)>(self.y.insdataref.no_of_slots_per_lab)*(self.y.no_of_lab):
                    self.dates.append([a,1])
                else:
                    self.dates.append([a,0])
            except:
                self.dates.append([a,0])
            a=a+datetime.timedelta(days=1)

    def givetiming(self,date):
        x=Pending_requests.query.filter_by(date=date).all()
        k=Pending_requests_institute.query.filter_by(date=date).all()
        add=0
        if len(k)>0:
            for i in k:
                add=add+i.no_of_slots
        print(x)
        if len(x)>0:

            no_of_booked=len(x)+add
            no_of_slots_per_lab=(self.y.institutedataref.no_of_slots_per_lab)
            if no_of_booked<self.y.institutedataref.no_of_slots_per_lab:
                times=self.y.starting_of_lab
                for i in range(self.y.no_of_lab):
                    hell=Pending_requests.query.filter_by(time=times).all()
                    if hell[0]:
                        z=len(hell)
                        if z<no_of_slots_per_lab:
                            return times
                times=times+datetime.timedelta(hours=self.y.duration_of_lab)
        else:
            times=self.y.starting_of_lab
            return times
