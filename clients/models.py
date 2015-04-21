from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from jsonfield import JSONField
from django.core.validators import MaxValueValidator, MinValueValidator
from random import randint


def generate_feed_match():
    return randint(100,999)


class table(models.Model):
    user = models.ForeignKey(User,primary_key=True)
    username = models.CharField(null=True,blank=True,max_length=32)
    first_name = models.CharField(null=True,blank=True,max_length=32)
    last_name = models.CharField(null=True,blank=True,max_length=32)
    email = models.EmailField(null=True,blank=True,max_length=60)
    city = models.CharField(null=True,blank=True,max_length=32)
    mobile = models.CharField(null=True,blank=True,max_length=10)
    rest_name = models.CharField(null=True,blank=True,max_length=32)
    n_of_table = models.IntegerField(default=0)
    status = JSONField()
    waiting_list = JSONField(default={'waiting_list':[]},null=True)
    seated = JSONField(default={'seated':[]},null=True)
    first_login = models.BooleanField(default=True)
    
    def __unicode__(self):
        return u'%s' % (self.user.username)

    
class Record(models.Model):
    user = models.ForeignKey(User)
    rest_name = models.CharField(null=True,blank=True,max_length=32)
    date = models.DateTimeField(auto_now_add=True, blank=False)
    mobile = models.CharField(blank=False,max_length=10)
    name = models.CharField(null=True,blank=True,max_length=32)
    age = models.IntegerField(blank=False,max_length=2)
    conversion = models.BooleanField(default=False)
    bill = models.IntegerField(blank=True,max_length=10,null=True)
    table_num = models.CharField(default='0',max_length =32)  #Table no in which he is seated
    waiting = models.BooleanField(default=True)
    seated = models.BooleanField(default=False)
    directly_seated = models.BooleanField(default=False)
    take_away = models.BooleanField(default=False)
    no_show = models.BooleanField(default=False)
    feed_match = models.IntegerField(default=generate_feed_match(),max_length=4,editable=False,null=True)

    def __unicode__(self):
        return u'%s' % (self.mobile)

class Feedback(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True, blank=False)
    mobile = models.CharField(blank=False,max_length=10)
    service = models.IntegerField(blank=True,null=True)
    ambience = models.IntegerField(blank=True,null=True)
    food = models.IntegerField(blank=True,null=True)
    overall_exp = models.IntegerField(blank=True,null=True)
    staff_friend = models.IntegerField(blank=True,null=True)
    record = models.ForeignKey(Record,null=True)

class FeedbackService(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True, blank=False)
    mobile = models.CharField(blank=False,max_length=10)
    service = models.IntegerField(blank=True,null=True)
    ambience = models.IntegerField(blank=True,null=True)
    food = models.IntegerField(blank=True,null=True)
    overall_exp = models.IntegerField(blank=True,null=True)
    staff_friend = models.IntegerField(blank=True,null=True)
    name = models.CharField(null=True,blank=True,max_length=32)
    dob = models.CharField(blank=True,max_length=10, null=True)
    comments = models.CharField(blank=True,max_length=200, null=True)
    table_num = models.CharField(default='0',max_length =32)

class Questions(models.Model):
    user = models.ForeignKey(User)
    question_type = models.IntegerField(blank=False,null=True) #1 for text 2 for date
    question_text = models.CharField(blank=False,max_length=1024,null=True)
    show = models.IntegerField(blank=False,default=1,null=True)

class Answers(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Questions)
    answer = models.CharField(blank=True,null=True,max_length=1024)

class RatingTexts(models.Model):
    user = models.ForeignKey(User)
    service_text = models.CharField(default='Quality of Service',blank=False,null=True,max_length=64)
    ambience_text = models.CharField(default='Ambience',blank=False,null=True,max_length=64)
    food_text = models.CharField(default='Quality of Food',blank=False,null=True,max_length=64)
    overall_exp_text = models.CharField(default='Overall Experience',blank=False,null=True,max_length=64)
    staff_friend_text = models.CharField(default='Staff Friendliness',blank=False,null=True,max_length=64)








