from django.shortcuts import render,render_to_response
from django.contrib import auth
from django import forms
import datetime
from django.contrib.auth.forms import UserCreationForm
from clients.forms import MyForm, AdminSettingsForm, AddGuestForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from clients.models import table, Record, Feedback, FeedbackService
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import json
from django.contrib.auth.models import User
from OnQueue import utils,signals
from guests.models import Guest
import datetime
import urllib2
from django.conf import settings
import requests



_MSG_CODES = {'swg': 'Sorry Wrong credentials',
			  'slo': 'Successfully Logged out',
			  'rsl': 'Registered Successfully Please Log in now',
			  'lap': 'Please login to access that page'}

MONTH = {
	'January':'01',
	'February':'02',
	'March':'03',
	'April':'04',
	'May':'05',
	'June':'06',
	'July':'07',
	'August':'08',
	'September':'09',
	'October':'10',
	'Novemebr':'11',
	'December':'12'
}


@receiver([post_save], sender=User)
def init_newuser_data(sender, **kwargs):
	'''
	Whenever a new user is created no of tables is assigned to 10
	with all tables as free
	'''
	user = kwargs.get('instance')
	try:
		rest_name = user.username+'_'+'name'
		t, t_created = table.objects.get_or_create(user=user,
            defaults={'user':user,'username':user.username,'rest_name':rest_name,'n_of_table':10,'status':{'free':[1,2,3,4,5,6,7,8,9,10],'booked':[]}})
	except table.MultipleObjectsReturned:
		pass

def index(request):
	return render(request,'index.html')

def test_view(request):
	return render(request,'clients/test_multi.html')

def api(request):
	response={"response":'An error occured'}
	if request.user.is_authenticated():
		t=table.objects.get(user=request.user)
		response=t.status
		# return HttpResponse(json.dumps(response), content_type="application/json")
	return HttpResponse(json.dumps(response), content_type="application/json") 

def get_waiting_list_of_table(request):
	response={"response":'An error occured'}
	if request.user.is_authenticated():
		t=table.objects.get(user=request.user)
		response=t.status
		# return HttpResponse(json.dumps(response), content_type="application/json")
	return HttpResponse(json.dumps(response), content_type="application/json") 





def login(request):
	if request.method == 'POST':
	    username = request.POST.get('username', '')
	    password = request.POST.get('password', '')
	    user = auth.authenticate(username=username, password=password)
	    if user is not None and user.is_active:
	        # Correct password, and the user is marked "active"
	        auth.login(request, user)
	        client = utils.user_to_client(user)
	        if client.first_login:
	        	return HttpResponseRedirect("/firstLogin/")
	        # Redirect to a success page.
	        return HttpResponseRedirect("/dashboard/")

	    else:
	        # Show an error page
	        return render(request,'clients/adminpanel/login.html',{'msg':_MSG_CODES['swg']})

	msg=request.GET.get('msg','')

	return render(request, 'clients/adminpanel/login.html',{'msg':msg})

def firstLogin(request):
	if  request.user.is_authenticated():
		client = utils.user_to_client(request.user)
		if client.first_login:
			if request.method == 'POST':
				first_name = request.POST.get('firstName','')
				last_name = request.POST.get('lastName','')
				mobile = request.POST.get('mobile','')
				email = request.POST.get('email','')
				n_of_table = int(request.POST.get('n_of_table',''))
				city = request.POST.get('city','')
				password = request.POST.get('password','')
				rest_name = request.POST.get('restName','')
				u = request.user
				u.set_password(password)
				u.save()
				print first_name, last_name, mobile, email, n_of_table, city, password,"CUSTOM"
				client = utils.user_to_client(request.user)
				client.first_name =  first_name
				client.last_name = last_name
				client.mobile = mobile
				client.n_of_table = n_of_table
				free = []
				for i in range(1,n_of_table+1): 
					free.append(i)
				free.sort()
				client.status = {'booked':[],'free':free}
				client.email = email
				client.city = city
				client.rest_name = rest_name
				client.first_login = False
				client.save(update_fields=['first_login','status','rest_name','first_name','last_name','mobile','n_of_table','email','city'])
				user = auth.authenticate(username=request.user.username, password=password)
				auth.login(request, user)
				return HttpResponseRedirect('/dashboard/')
			return render(request,'clients/adminpanel/first_login.html')
		else:
			return HttpResponseRedirect('/dashboard/')

	return HttpResponseRedirect('/login?msg=%s' %_MSG_CODES['lap'])


def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/login?msg=%s' %_MSG_CODES['slo'])
    # return render(request, 'clients/login.html', {'msg':_MSG_CODES['slo']})

def register(request):
	if request.user.is_superuser:
	    if request.method == 'POST':
	        form = UserCreationForm(request.POST)
	        if form.is_valid():
	            new_user = form.save()
	            return HttpResponseRedirect('/login?msg=%s' %_MSG_CODES['rsl'])
	            # return render(request,'clients/login.html',{'msg':'Registered Successfully Please Log in now'})
	    else:
	        form = UserCreationForm()
	    return render(request, "clients/register.html", {
	        'form': form,
	    })
	else:
		return HttpResponse('Unauthorized', status=401)



def loggedin(request):
	if  request.user.is_authenticated():
		t = table.objects.get(user=request.user)
		return render(request,'clients/loggedin.html', {'n_of_tables':t.n_of_table,'status':t.status})
	else:
		# return HttpResponseRedirect('/login?msg=%s' %_MSG_CODES['lap'])
		return render(request,'clients/login.html',{'msg':'Please login to access that page'})


def process_status(request):
	post = request.POST.copy()
	no = post.get('checkout_table')
	booked = table.objects.get(user=request.user).status['booked']
	free = table.objects.get(user=request.user).status['free']
	booked.remove(int(no))
	free.append(int(no))
	booked.sort()
	free.sort()
	st={"booked":booked,"free":free}
	post['status']=st
	return post



def update_tables(request):
	if  request.user.is_authenticated():
		instance=table.objects.get(user=request.user)
		if request.method == "POST":
			post = process_status(request)
			form = MyForm(post, instance=instance)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/loggedin/')
		form = MyForm(None, instance=instance)
		return render(request, 'clients/old_templates/admin_settings.html', {'form': form})
	else:
		return render(request,'clients/login.html',{'msg':'Please login to access that page'})

def update_default(request):
	if  request.user.is_authenticated():
		instance=table.objects.get(user=request.user)
		if request.method == "POST":
			form = MyForm(request.POST, instance=instance)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/loggedin/')
		form = MyForm(None, instance=instance)
		return render(request, 'clients/old_templates/admin_settings.html', {'form': form})
	else:
		return render(request,'clients/login.html',{'msg':'Please login to access that page'})

def waitlist(request):
	if  request.user.is_authenticated():
		return render(request,'clients/waitlist.html')

	return HttpResponseRedirect('/login?msg=%s' %_MSG_CODES['lap'])

def checkout(request):
	if  request.user.is_authenticated():
		if request.method == 'POST':
			print "============CHECKOUT STARTED==============="
			print "Restuarant: ", request.user
			t_n = int(request.POST.get('checkout_table'))
			t=table.objects.get(user=request.user)
			free = t.status['free']
			booked = t.status['booked']
			seated = t.seated['seated']

			print "Currently booked tables: ", booked

			print "Checkout requested: ",t_n
			for guest in seated:
				g=Guest.objects.get(mobile=guest)
				print "------Seated guests--------"
				print 'table_no: ',g.table_no
				if str(t_n) in g.table_no:
					print "MATCHED"
					print g.table_no
					seated.remove(guest)
					tabs_seated = g.table_no.split(',')
					print tabs_seated
					for i in tabs_seated:
						print i
						booked.remove(int(i))
						free.append(int(i))
					free.sort()
					booked.sort()
					print "============ booked after remove: ", booked
					t.status={"booked":booked,"free":free}
					g.current = "null"
					g.status = 0
					table_no = '0'
					restuarant = request.user.username
					date = utils.time_now()
					g.last_visited ={'restuarant':restuarant,'date':date}
					visited = g.restuarants['visited']
					visited.append(restuarant)
					g.restuarants={'visited':visited}
					g.save(update_fields=['current','status','last_visited','restuarants'])
					signals.save_checkout(request.user,g.mobile,100) 
					t.save(update_fields=['status','seated'])
			print "-------------------------"
			a = request.META.get('HTTP_REFERER','')
			print '============CHECKOUT ENDED================='
			if a.split('/')[3]=='front':
				return HttpResponseRedirect('/front/')
			return HttpResponseRedirect('/dashboard/')

		return render(request,'clients/checkout.html')

	return HttpResponseRedirect('/login?msg=%s' %_MSG_CODES['lap'])

def admin_settings(request):
	if  request.user.is_authenticated():

		if request.method == "POST":
			ChangePassword = request.POST.get('ChangePassword','')
			ChangeTables = request.POST.get('ChangeTables','')
			Other = request.POST.get('Other','')
			first_name = request.POST.get('firstName','')
			last_name = request.POST.get('lastName','')
			mobile = request.POST.get('mobile','')
			n_of_table = request.POST.get('n_of_table','')
			password = request.POST.get('password','')
			rest_name = request.POST.get('restName','')

			client = utils.user_to_client(request.user)
			if n_of_table:
				print "Chaning No of tables"
				client.n_of_table = int(n_of_table)
				free = []
				for i in range(1,int(n_of_table)+1): 
					free.append(i)
				free.sort()
				client.status = {'booked':[],'free':free}
				client.seated = {'seated':[]}
				client.waiting_list = {'waiting_list':[]}
				client.save(update_fields=['n_of_table','seated','waiting_list','status'])

			if first_name:
				client.first_name = first_name
				client.save(update_fields=['first_name'])

			if last_name:
				client.last_name = last_name
				client.save(update_fields=['last_name'])

			if rest_name:
				client.rest_name = rest_name
				client.save(update_fields=['rest_name'])

			if mobile:
				client.mobile = mobile
				client.save(update_fields=['mobile'])

			if password:
				print "Changing Password"
				u = request.user
				u.set_password(password)
				u.save()
				user = auth.authenticate(username=request.user.username, password=password)
				auth.login(request, user)



			# t=table.objects.get(user=request.user)
			# n = int(request.POST.get('n_of_table'))
			# t.n_of_table = n
			
			return HttpResponseRedirect('/dashboard/')
		client = utils.user_to_client(request.user)
		return render(request, 'clients/adminpanel/settings.html',{'client':client})
		
	return HttpResponseRedirect('/login?msg=%s' %_MSG_CODES['lap'])



def dashboard(request):
	if  request.user.is_authenticated():
		client = utils.user_to_client(request.user)
		if client.first_login:
			return HttpResponseRedirect('/firstLogin/')
		n_of_tables = table.objects.get(user=request.user)
		seated=len(utils.get_seated_guests(request.user))
		waiting=len(utils.get_waiting_guests(request.user))
		total_guests = utils.get_total_visitors(request.user)
		total_no_show = utils.get_total_no_show(request.user)
		feed_stats=utils.get_feedback_stats(request.user)

		return render(request,'clients/adminpanel/index.html', {'client':client,'n_of_tables':n_of_tables.n_of_table,'status':n_of_tables.status,'seated':seated,'waiting':waiting,'total_guests':total_guests,'total_no_show':total_no_show,'feed_stats':feed_stats})
	else:
		return HttpResponseRedirect('/login?msg=%s' %_MSG_CODES['lap'])
		

def add(request):
	errors = []
	if  request.user.is_authenticated():
		if request.method == 'POST':
			mobile = request.POST.get('mobile', '')
			errors = []
			print mobile,"-------------------------------"
			waiting_list = utils.get_waiting_guests(request.user)
			if not mobile in waiting_list:  #Check if he's not already in waiting list
				if utils.guest_exists(mobile):
					g = Guest.objects.get(mobile=mobile)
					g.waiting_time = 5
					g.start_time = utils.time_now()
					g.status = 1  #Waiting list
					g.current = request.user.username
					g.save(update_fields=['waiting_time','start_time','status','current'])
				else:
					g=Guest(mobile=mobile,created_at=utils.time_now(),start_time = utils.time_now(),status=1,current = request.user.username,waiting_time = 5)
					g.save()
					# utils.send_link_to_register(mobile)
				##Add user to the waiting list
				u=User.objects.get(username=request.user.username)
				utils.update_waiting_list(u,g)
				signals.save_waiting(request.user,mobile)
			else:
				errors.append("%d already  in waiting list" %mobile)
			print errors,"========ERROR================"
		form = AddGuestForm()
		waiting = utils.get_waiting_detail(request.user)

		return render(request, 'clients/add.html', {'form':form,'waiting':waiting,'errors':errors})
	else:
		return HttpResponseRedirect('/login?msg=%s' %_MSG_CODES['lap'])

def adduser(request):
	error = []
	if  request.user.is_authenticated():
		if request.method == 'POST':
			seat = request.POST.get('seat', '')
			if seat:#Visitor has to be seated directly
				return seatDirectly(request)
			takeaway = request.POST.get('takeaway', '')
			if takeaway: #Visitor came for takeaway
				return takeAway(request)
			mobile = request.POST.get('mobile', '')
			name = request.POST.get('name', '')
			waitingtime = request.POST.get('waitingtime', '')
			partysize = request.POST.get('partysize', '')
			add_to_waiting = request.POST.get('add_to_waiting', '')
			print mobile,name,waitingtime,partysize,add_to_waiting,"-------------->>>>>>>"
			
			waiting_list = utils.get_waiting_guests(request.user)
			seated_list = utils.get_seated_guests(request.user)
			if (not mobile in waiting_list) and (not mobile in seated_list):  #Check if he's not already in waiting list or seated
				if utils.guest_exists(mobile):
					g = Guest.objects.get(mobile=mobile)
					g.waiting_time = waitingtime
					g.start_time = utils.time_now()
					g.status = 1  #Waiting list
					g.current = request.user.username
					g.save(update_fields=['waiting_time','start_time','status','current'])
				else:
					g=Guest(mobile=mobile,created_at=utils.time_now(),start_time = utils.time_now(),status=1,current = request.user.username,waiting_time = waitingtime,name=name)
					g.save()
				##Add user to the waiting list
				u=User.objects.get(username=request.user.username)
				utils.update_waiting_list(u,g)
				signals.save_waiting(request.user,mobile,waitingtime)
			elif (not mobile in waiting_list) and (mobile in seated_list):
				error = "User already seated"
			elif (not mobile in seated_list) and (mobile in waiting_list):
				error = "User already in waiting list"
			print "========ERROR================"
			print error
			print "============================="
			if(len(error)!=0):
				return HttpResponseRedirect('/front?error=%s' %(error))
			else:
				return HttpResponseRedirect('/front/')
			
		return HttpResponseRedirect('/front/')

		# return render(request, 'clients/front.html')
	else:
		return HttpResponseRedirect('/login?msg=%s' %_MSG_CODES['lap'])



def countdown(request):
	time = 30
	return render(request,'clients/countdown.html',{'time':time})

def seated(request):
	if  request.user.is_authenticated():
		if request.method == 'POST':
			guest_num = request.POST.get('guest_num')
			table_num = int(request.POST.get('table_num'))
			t=table.objects.get(user=request.user)
			free = t.status['free']
			booked = t.status['booked']
			booked.append(int(table_num))
			print table_num,"----------------------------------------"
			free.remove(int(table_num))
			booked.sort()
			free.sort()
			seated = t.seated['seated']
			waiting = t.waiting_list['waiting_list']
			seated.append(guest_num)
			waiting.remove(guest_num)
			t.seated = {'seated':seated}
			t.waiting_list = {'waiting_list':waiting}

			t.status={"booked":booked,"free":free}
			t.save(update_fields=['status','waiting_list','seated'])
			g=Guest.objects.get(mobile=guest_num)
			g.current=request.user.username
			g.table_no = table_num
			g.status = 2
			signals.save_seated(request.user,guest_num,table_num)
			g.save(update_fields=['current','table_no','status'])
			return HttpResponseRedirect('/dashboard/')
			
		waiting_list = utils.get_waiting_guests(request.user)
		return render(request,'clients/seated.html',{'waiting_list':waiting_list})

	return HttpResponseRedirect('/login?msg=%s' %_MSG_CODES['lap'])

def seatUser(request):
	if  request.user.is_authenticated():
		if request.method == 'POST':
			mydict = request.POST
			mobile = request.POST.get('mobile')
			print "===============seatUser=================="
			tables = []
			for key, value in mydict.iteritems():
				if key.startswith('table'):
					tables.append(int(value))
			print 'tables selected by user: ',tables
			t=table.objects.get(user=request.user)
			free = t.status['free']
			booked = t.status['booked']
			for tab in tables:
				booked.append(tab)
				free.remove(tab)
			booked.sort()
			free.sort()
			seated = t.seated['seated']
			waiting = t.waiting_list['waiting_list']
			seated.append(mobile)
			waiting.remove(mobile)
			t.seated = {'seated':seated}
			t.waiting_list = {'waiting_list':waiting}
			t.status={"booked":booked,"free":free}
			g=Guest.objects.get(mobile=mobile)
			g.current=request.user.username
			print "-----==========+++++++++++", str(tables)[1:-1]
			g.table_no = str(tables)[1:-1]
			g.status = 2
			t.save(update_fields=['status','waiting_list','seated'])
			g.save(update_fields=['current','table_no','status'])
			signals.save_seated(request.user,mobile,tables)



			return HttpResponseRedirect('/front/')

	return HttpResponseRedirect('/login?msg=%s' %_MSG_CODES['lap'])

def seatDirectly(request):
	print "============Reached seatDirectly=============="
	mydict = request.POST
	mobile = request.POST.get('mobile', '')
	name = request.POST.get('name', '')
	waitingtime = request.POST.get('waitingtime', '')
	partysize = request.POST.get('partysize', '')
	tables = []
	for key, value in mydict.iteritems():
		if key.startswith('table'):
			tables.append(int(value))
	print 'tables selected by user: ',tables
	if len(tables)==0:
		return HttpResponseRedirect('/front/?error=Please select a table')
	waiting_list = utils.get_waiting_guests(request.user)
	seated_list = utils.get_seated_guests(request.user)
	if (not mobile in waiting_list) and (not mobile in seated_list):  #Check if he's not already in waiting list or seated
		if utils.guest_exists(mobile):
			g = Guest.objects.get(mobile=mobile)
			g.status = 2  #Seated
			g.current = request.user.username
			g.table_no = str(tables)[1:-1]
			print "Saving direct user with: table_no: "
			g.save(update_fields=['status','current','table_no'])
			signals.save_seated(request.user,mobile,tables,1)
		else:
			print "Creating and Saving direct user with: table_no: ", 
			g=Guest(mobile=mobile,created_at=utils.time_now(),status=2,current = request.user.username,name=name,table_no = str(tables)[1:-1])
			g.save()
			signals.save_seated(request.user,mobile,tables,1)
			# utils.send_link_to_register(mobile,name)
	else:
		return HttpResponseRedirect('/front/?error=%s' %'User already in waiting list or seated')

	#Update table info
	t=table.objects.get(user=request.user)
	free = t.status['free']
	booked = t.status['booked']
	for tab in tables:
		booked.append(tab)
		free.remove(tab)
	booked.sort()
	free.sort()
	seated = t.seated['seated']
	seated.append(mobile)
	t.seated = {'seated':seated}
	t.status={"booked":booked,"free":free}
	t.save(update_fields=['status','seated'])
	print "===============FINISHED seatDirectly================="
	return HttpResponseRedirect('/front/')

def takeAway(request):
	print "============Reached takeAway=============="
	mobile = request.POST.get('mobile', '')
	name = request.POST.get('name', '')
	date = utils.time_now()
	if utils.guest_exists(mobile):
		g = Guest.objects.get(mobile=mobile)
		g.last_visited ={'restuarant':request.user.username,'date':date}
		print "Saving direct user with: table_no: "
		g.save(update_fields=['last_visited'])
	else:
		print "Creating and Saving takeAway user", 
		g=Guest(mobile=mobile,created_at=date,status=0,name=name,last_visited ={'restuarant':request.user.username,'date':date})
		g.save()
		# utils.send_link_to_register(mobile,name)
	signals.save_takeaway(request.user,mobile,date)
	print "============ENDING takeAway=============="
	return HttpResponseRedirect('/front/')

def noShow(request):
	print "===========REACHED noShow===================="
	if  request.user.is_authenticated():
		if request.method == 'POST':
			mobile = request.POST.get('mobile', '')
			print mobile
			t=table.objects.get(user=request.user)
			waiting = t.waiting_list['waiting_list']
			if mobile not in waiting:
				return HttpResponseRedirect('/front/?error=%s not i waiting list' %mobile)
			waiting.remove(mobile)
			t.waiting_list = {'waiting_list':waiting}
			g=Guest.objects.get(mobile=mobile)
			g.current="null"
			g.status = 0
			g.last_visited ={'restuarant':request.user.username,'date':utils.time_now()}
			t.save(update_fields=['waiting_list'])
			g.save(update_fields=['current','status','last_visited'])
			signals.save_noshow(request.user,mobile)

		return HttpResponseRedirect('/front/')
	return HttpResponseRedirect('/login?msg=%s' %_MSG_CODES['lap'])			






def analytics(request):
	dates=utils.previous_days(5)
	records_converted=[]
	# for date in dates:
	# 	element = {}
	# 	element['year'] = str(date)
	# 	element['value'] = Record.objects.filter(user=request.user,conversion=True,date__startswith=date).count()
	# 	records_converted.append(element)
	# print "============================"
	# for i in records_converted:
	# 	print i
	# print "============================"
	client = utils.user_to_client(request.user)

	count={}
	count['no_show']=Record.objects.filter(user=request.user,no_show=True).count()
	count['take_away']=Record.objects.filter(user=request.user,take_away=True).count()
	count['conversion']=Record.objects.filter(user=request.user,conversion=True).count()

	

	return render(request,'clients/adminpanel/charts/morris.html',{'records_converted':records_converted,'client':client,'count':count})
	

def ShowRecords(request):
	records_converted = Record.objects.filter(user=request.user,conversion=True)
	records_total = Record.objects.filter(user=request.user)
	client = utils.user_to_client(request.user)
	return render(request,"clients/adminpanel/tables/data.html",{'records_converted':records_converted,'records_total':records_total,'client':client})

def JSON_records(request):
	'''
	Using as an API for analytics page

	'''
	response={"response":'An error occured'}
	if request.user.is_authenticated():
		records = {}
		dates=utils.previous_days(5)
		#------------start records_converted
		records_converted=[]
		for date in dates:
			element = {}
			element['date'] = str(date)
			element['count'] = Record.objects.filter(user=request.user,conversion=True,date__startswith=date).count()
			records_converted.append(element)
		#------end records_converted
		records['records_converted'] = records_converted

		#----start total records
		records_total = []
		for date in dates:
			element = {}
			element['date'] = str(date)
			element['count'] = Record.objects.filter(user=request.user,date__startswith=date).count()
			records_total.append(element)
		#--- end total records

		records['records_total'] = records_total

		#---Start Donut data
		for date in dates:
			element={}

		#---Start Feedback stats
		records['feed_stats']=utils.get_feedback_stats(request.user)

		#--Start Detail feed stats
		records['detail_feed_stats']=utils.get_detail_feedback_stats(request.user)

		#-- Start feedback service
		records['feedback_service'] = utils.get_detail_feedback_service(request.user)

	return HttpResponse(json.dumps(records), content_type="application/json")


def permission_denied(request):
	if request.user.is_authenticated():
		a = request.META.get('HTTP_REFERER')
		if a:
			a = request.META['HTTP_REFERER']
			if a.split('/')[3]=='records':
				msg = 'We respect Our users privacy and if you are seeing this page it means he/she has not allowed us to make this info public.'
				return render(request,"clients/permission_denied.html",{'msg':msg})
			else:
				return HttpResponseRedirect(request.META['HTTP_REFERER'])

		else:
			return HttpResponseRedirect('/')

	return HttpResponseRedirect('/login?msg=%s' %_MSG_CODES['lap'])

def front(request):
	if request.user.is_authenticated():
		client = utils.user_to_client(request.user)
		if client.first_login:
			return HttpResponseRedirect('/firstLogin/')
		rest_name = table.objects.get(user=request.user).rest_name
		url = '%s/api/v1/table/%s/?format=json' %(settings.HOST,request.user.username)
		print url
		# response = '{"city": "Lucknow", "email": "vikasmishra95@gmail.com", "first_login": "false", "first_name": "Vikas", "last_name": "Mishra", "mobile": "234", "n_of_table": 13, "resource_uri": "/api/v1/table/onque/", "rest_name": "Fake", "seated": "{useated": []}", "status": "{u"booked": [], u"free": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}", "user": "/api/v1/user/onque/", "username": "onque", "waiting_list": "{u"waiting_list": []}"}'
		response = urllib2.urlopen(url) 
		# r = requests.get('http://localhost:8001/api/v1/table/onque/?format=json')
		# waiting_list = r.json()

		print response
		waiting_list = json.load(response)
		users = utils.get_user_details(waiting_list['waiting_list'])
		parties_waiting = len(users)
		
		#--table checkout starts
		t = table.objects.get(user=request.user)
		client = t
		seated = t.seated['seated']
		parties_seated = len(seated)
		checkout_table_nums = t.status['booked']
		free_tables = t.status['free']
		#--table checkout ends

		return render(request,'clients/front.html',{'users':users,'client':client,'checkout_table_nums':checkout_table_nums,'free_tables':free_tables,'parties_seated':parties_seated,'parties_waiting':parties_waiting})
	return HttpResponseRedirect('/login?msg=%s' %_MSG_CODES['lap'])

def sendsms(request):
	if request.user.is_authenticated():
		number = request.GET.get('number')
		message = request.GET.get('message')
		if number and message:
			response = utils.send_sms(number,message)
		else:
			response = "Invalid Number or message"
		return HttpResponse(response)
	else:
		return render(request,'clients/permission_denied.html',{'msg':'Not authorized'})

def notifyGuest(request):
	if request.user.is_authenticated():
		number = request.POST.get('number')
		message = request.POST.get('message')
		if number and message:
			response = utils.send_sms(number,message)
			return HttpResponseRedirect('/front/')
		else:
			response = "Invalid Number or message"
			return HttpResponseRedirect('/front/?error=Please enter both number and message')
	return render(request,'clients/permission_denied.html',{'msg':'Not authorized'})

def feedback(request, fid, feed_match):
	print fid, feed_match
	feed_match = int(feed_match)
	if request.method == 'POST':
		print "REACHED POST"
		rating_qof = request.POST.get('rating_qof','')
		rating_qos= int(request.POST.get('rating_qos',''))
		rating_sf = int(request.POST.get('rating_sf',''))
		rating_ab = int(request.POST.get('rating_ab',''))
		rating_oe = int(request.POST.get('rating_oe',''))
		print rating_qof,rating_qos,rating_sf,rating_ab, rating_oe
		r=Record.objects.get(id=fid,feed_match=feed_match)
		f=Feedback(record=r,user=r.user,mobile=r.mobile,date=utils.time_now(),service=rating_qos,ambience=rating_ab,food=rating_qof,staff_friend = rating_sf,overall_exp=rating_oe)
		f.save()
		# utils.send_sms(r.mobile,'Thankyou for Filling the feedback form')
		return HttpResponseRedirect('/')
	try:
		r=Record.objects.get(id=fid)
		try:
			f=Feedback.objects.get(record=r)
			return HttpResponseRedirect('/?msg=Already filled')
		except Feedback.DoesNotExist:
			pass
		if feed_match == r.feed_match:
			return render(request,'clients/feedback2.html',{'place':r.rest_name,'date':r.date,'name':r.name})
	except Record.DoesNotExist:
		# return render(request,'clients/feedback2.html')
		print "Does not exist"

	return HttpResponseRedirect('/404/')

def handler404(request):
	return render(request,'404.html',status='404')

def feedback_display(request):
	feedbacks = FeedbackService.objects.filter(user=request.user).exclude(service__isnull=True)
	client = utils.user_to_client(request.user)
	return render(request,'clients/adminpanel/tables/feedback_display.html',{'feedbacks':feedbacks,'client':client})

def core_function(request):
	token=request.GET.get('token')
	if token==settings.TOKEN:
		number = request.GET.get('number')
		message = request.GET.get('message')
		if number and message:
			response = utils.send_sms(number,message)
		else:
			response = "Invalid Number or message"
	else:
		response = "Unauthorized"

	return HttpResponse(response)

def dev(request):
	return render(request,'clients/adminpanel/base.html')

def feedback_service(request):
	if request.method == 'POST':
		print "POST-------------------"
		table_num = request.POST.get('tableno','')
		rating_qof = request.POST.get('rating_qof','')
		rating_qos= int(request.POST.get('rating_qos',''))
		rating_sf = int(request.POST.get('rating_sf',''))
		rating_ab = int(request.POST.get('rating_ab',''))
		rating_oe = int(request.POST.get('rating_oe',''))
		info_name = request.POST.get('info_name','')
		dob_date = request.POST.get('dob_date','')
		dob_month = request.POST.get('dob_month','')
		dob_year = request.POST.get('dob_year','')
		ann_date = request.POST.get('ann_date','')
		ann_month = request.POST.get('ann_month','')
		ann_year = request.POST.get('ann_year','')
		info_contact = request.POST.get('info_contact','')
		comments = request.POST.get('comments','')
		dob = dob_date + "/" + MONTH[dob_month] + "/" + dob_year
		anniversary = ann_date + "/" + MONTH[ann_month] + "/" + ann_year
		if (info_contact and info_name):
			try:
				if utils.guest_exists(info_contact):
					pass
				else:
					g = Guest(name=info_name,mobile=info_contact,dob=datetime.datetime.strptime(dob,"%d/%m/%Y"),created_at=utils.time_now())
					g.save()
				print rating_qof,rating_qos,rating_sf,rating_ab, rating_oe,table_num, info_name, dob,info_contact,comments, anniversary
				fs = FeedbackService(user=request.user, date=utils.time_now(),mobile=info_contact,name=info_name,table_num=table_num,food=rating_qof,service=rating_qos,staff_friend=rating_sf,ambience=rating_ab,overall_exp=rating_oe,dob=dob,anniversary=anniversary,comments=comments)
				fs.save()
				print "SAVED"
			except:
				return HttpResponseRedirect('/feedback?msg=Invalid Input')

			return HttpResponseRedirect('/feedback?msg=thanks')
		return HttpResponseRedirect('/feedback?msg=required')
	client = utils.user_to_client(request.user)
	return render(request, 'clients/feedback_service.html',{'client':client})






	
	













