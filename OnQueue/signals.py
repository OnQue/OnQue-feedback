from guests.models import Guest, PersonalRecord
from clients.models import table,Record
import datetime
from math import floor
from OnQueue.utils import time_now
import utils
from utils import send_sms
from django.conf import settings


def save_waiting(user,mobile,waitingtime):
    print "Save_waiting"
    guest = Guest.objects.get(mobile=mobile)
    rest_name = table.objects.get(user=user).rest_name
    record = Record(user=user,rest_name=rest_name,date=time_now(),mobile=mobile,age=guest.age,name=guest.name)
    record.save()
    pr = PersonalRecord(guest=guest,restuarant=rest_name,date=time_now())
    pr.save() 
    message="Hello, Welcome to %s, your estimated waiting time is %s mins. You will be informed when your table is ready." %(rest_name,str(waitingtime))
    send_sms(mobile,message)


def save_seated(user,mobile,table_num,flag=0):
    print "save_seated"
    if flag==0:
        record = Record.objects.get(user=user,mobile=mobile,waiting=True,take_away=False,directly_seated=False)
        record.conversion = True
        record.waiting= False
        record.seated = True
        record.table_num = table_num[1:-1]
        record.save(update_fields=['conversion','waiting','seated','table_num'])
    elif flag==1: #Visitor directly seated
        guest = Guest.objects.get(mobile=mobile)
        rest_name = table.objects.get(user=user).rest_name
        record = Record(user=user,seated=True,rest_name=rest_name,date=time_now(),mobile=mobile,age=guest.age,name=guest.name,directly_seated=True,table_num=table_num[1:-1])
        record.save()

def save_checkout(user,mobile,bill,flag=0):
    print "save_checkout"
    if flag==0:
        record = Record.objects.get(user=user,mobile=mobile,seated=True,take_away=False)
        record.seated = False
        record.bill = bill
        record.save(update_fields=['seated','bill'])
    elif flag==1: #Checkout directly seated
        record = Record.objects.get(user=user,mobile=mobile,seated=True,directly_seated=True,take_away=False)
        record.seated = False
        record.bill = bill
        record.save()
    feed_url = '%s/f/%d/%d' %(settings.HOST,record.id,record.feed_match)
    message = "Thank you for visiting %s, your valuable feedback will be appreciated %s" %(record.rest_name,feed_url)
    send_sms(mobile,message)

def save_takeaway(user,mobile,date):
    print "save_takeaway"
    guest = Guest.objects.get(mobile=mobile)
    rest_name = table.objects.get(user=user).rest_name
    record = Record(user=user,rest_name=rest_name,date=date,mobile=mobile,age=guest.age,name=guest.name,take_away=True)
    record.save()
    feed_url = '%s/f/%d/%d' %(settings.HOST,record.id,record.feed_match)
    message = "Thank you for visiting %s, your valuable feedback will be appreciated %s" %(record.rest_name,feed_url)
    send_sms(mobile,message)

def save_noshow(user,mobile):
    client = utils.user_to_client(user)
    record = Record.objects.get(user=user,mobile=mobile,waiting=True,take_away=False,directly_seated=False)
    record.conversion = False
    record.waiting= False
    record.seated = False
    record.no_show = True
    record.save(update_fields=['conversion','waiting','seated','no_show'])
    message = "We're sorry to infrom that you have been removed from the Que at %s. If any issues contact %s" %(client.rest_name, client.mobile)
    send_sms(mobile,message)

