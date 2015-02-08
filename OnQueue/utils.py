from guests.models import Guest
from clients.models import table, Record, Feedback, FeedbackService
import datetime
from math import floor, ceil
from twill.commands import *
from datetime import timedelta
import urllib2
import json
from django.conf import settings


def guest_exists(mobile):
    try:
        my_object = Guest.objects.get(mobile=mobile)
    except Guest.DoesNotExist:
        return False
    return True

def send_link_to_register(mobile,name):
    message = "Hello %s welcome to OnQue, please go through the following link to complete your profile #" %name
    send_sms(mobile,message)

def time_now():
    return datetime.datetime.now()

def signal_add_waiting_list(u,g):
    pass

def update_waiting_list(u,g):
    t=table.objects.get(user=u)
    w=t.waiting_list['waiting_list']
    w.append(g.mobile)
    t.waiting_list = {'waiting_list':w}
    t.save(update_fields=['waiting_list'])

def update_seated(u,g):
    t=table.objects.get(user=u)
    s=t.seated['seated']
    s.append(g.mobile)
    t.seated = {'seated':s}
    t.save(update_fields=['seated'])

def get_seated_guests(u):
    t=table.objects.get(user=u)
    s=t.seated['seated']
    return s

def get_waiting_guests(u):
    t=table.objects.get(user=u)
    w=t.waiting_list['waiting_list']
    return w

def get_waiting_detail(u):
    retVal = {}
    mobiles = get_waiting_guests(u)
    for mobile in mobiles:
        guest=Guest.objects.get(mobile=mobile)
        start_time = guest.start_time
        print start_time,time_now()
        diff = (time_now() - start_time).total_seconds()
        rem = guest.waiting_time*60 - floor(diff)
        if(rem <=0):
            retVal[mobile]=-1
        else:
            retVal[mobile]=rem
    return retVal

def get_waiting_time(guest):
    start_time = guest.start_time
    print start_time,time_now()
    diff = (time_now() - start_time).total_seconds()
    rem = guest.waiting_time*60 - floor(diff)
    if(rem <=0):
        retVal = -1
    else:
        retVal = int(ceil(rem/60.0))
    return retVal


def send_sms(number,message):
    
    print "==============SEND SMS=================="
    print "Number: ",number
    print "Message: ",message
    print "========================================"
    number = int(number)
    message=message.replace('%','%25')
    message=message.replace(' ','%20')
    response = 17011
    if settings.SEND_SMS:
        url = "http://login.bulksms360.in:8080/sendsms/bulksms?username=exp1-onquee&password=123456&type=0&dlr=1&destination=%s&source=ONQUEE&message=%s" %(number,message)
        print url
        response = urllib2.urlopen(url)
        response = response.read().split('|')[0]
    return (response)

def previous_days(n):
    l=[]
    for i in range(0,n):
        l.append(datetime.date.today()-timedelta(days=i))
    return (l)

def clean_dict_JSON(mydict):
    for key in mydict.keys():
        if type(key) is not str:
            try:
              mydict[str(key)] = mydict[key]
            except:
              try:
                mydict[repr(key)] = mydict[key]
              except:
                pass
        del mydict[key]

    return mydict

def get_last_visited_details(guest):
    date = guest.last_visited['date'].strftime("%B %d, %Y")
    place = guest.last_visited['restuarant']
    return ({'date':date,'place':place})

def get_user_details(waiting_list):
    # print waiting_list,"=================="
    a= waiting_list
    i = 0
    num = a[a.find("[")+1:a.find("]")]
    l= num.split(',')
    print l
    users = []
    if len(l)>=1 and l[0]!='':
        for num in l:
            user = {}
            print str((num.split("'")[1])),"VIKAS"
            g=Guest.objects.get(mobile=num.split("'")[1])
            user['name'] = g.name
            user['mobile'] = g.mobile
            user['age'] = g.age
            user['time_left'] = get_waiting_time(g)
            user['waiting_time'] = g.waiting_time
            user['lastVisited']=g.last_visited
            user['tablesReqd'] = 1
            users.append(user)

    print users
    return users

def user_to_client(user):
    t=table.objects.get(user=user)
    return t

def get_total_visitors(u):
    total = Record.objects.filter(user=u,date__startswith=datetime.date.today()).count()

    return total

def get_total_no_show(u):
    total = Record.objects.filter(user=u,no_show=True,date__startswith=datetime.date.today()).count()

    return total

def get_feedback_stats(u):
    dates = previous_days(7)
    retVal=[]
    for date in dates:
        r = Feedback.objects.filter(user=u,date__startswith=date)
        l=[]
        for f in r:
            l.append(float(f.service+f.ambience+f.overall_exp+f.food+f.staff_friend)/5)
        element = {}
        element['date']=str(date)
        element['count']=0

        if len(l)!= 0:   
            element['count'] = round(sum(l)/len(l),2)
        retVal.append(element)

    print '====================Feedback Stats====================='
    print retVal
    return retVal

def get_detail_feedback_stats(u):
    dates = previous_days(7)
    retVal = []
    for date in dates:
        r= Feedback.objects.filter(user=u,date__startswith=date)
        service=[]
        ambience=[]
        overall_exp=[]
        food=[]
        staff_friend=[]
        for f in r:
            service.append(f.service)
            ambience.append(f.ambience)
            overall_exp.append(f.overall_exp)
            food.append(f.food)
            staff_friend.append(f.staff_friend)

        element={}
        element['date']=str(date)
        element['service']=0
        element['ambience']=0
        element['overall_exp']=0
        element['food']=0
        element['staff_friend']=0
        if len(service)!=0:
            element['service']=round(sum(service)/len(service),2)
            element['ambience']=round(sum(ambience)/len(ambience),2)
            element['overall_exp']=round(sum(overall_exp)/len(overall_exp),2)
            element['food']=round(sum(food)/len(food),2)
            element['staff_friend']=round(sum(staff_friend)/len(staff_friend),2)
            
        retVal.append(element)

    print retVal
    return retVal

def get_detail_feedback_service(u):
    dates = previous_days(7)
    retVal = []
    for date in dates:
        r= FeedbackService.objects.filter(user=u,date__startswith=date)
        service=[]
        ambience=[]
        overall_exp=[]
        food=[]
        staff_friend=[]

        for f in r:
            service.append(f.service)
            ambience.append(f.ambience)
            overall_exp.append(f.overall_exp)
            food.append(f.food)
            staff_friend.append(f.staff_friend)

        element={}
        element['date']=str(date)
        element['service']=0
        element['ambience']=0
        element['overall_exp']=0
        element['food']=0
        element['staff_friend']=0
        if len(service)!=0:
            element['service']=round(sum(service)/len(service),2)
            element['ambience']=round(sum(ambience)/len(ambience),2)
            element['overall_exp']=round(sum(overall_exp)/len(overall_exp),2)
            element['food']=round(sum(food)/len(food),2)
            element['staff_friend']=round(sum(staff_friend)/len(staff_friend),2)
            
        retVal.append(element)

    print retVal
    return retVal

        




    








