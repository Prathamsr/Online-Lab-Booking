import smtplib
import random
def verification(email):
    senders_email='pspsps'
    senders_password="sdkjvais"
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(senders_email,senders_password)
    otp=''
    for i in range(6):
        k=random.choice([1,2,3,4,5,6,7,8,9])
        otp=otp+str(k)
    print(otp)
    message="Your one time password for email verification is "+otp
    server.sendmail(senders_email,email,message)
    return otp
def confirmation_email(email,lab,date,time):
    senders_email='pspsps'
    senders_password="sdkjvais"
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(senders_email,senders_password)
    message=f"Your request for {lab} lab on {date} at {time} is confirm, make payment throught your account  "
    server.sendmail(senders_email,email,message)
