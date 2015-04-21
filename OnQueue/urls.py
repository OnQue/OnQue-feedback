from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from OnQueue.api import GuestResource, TableResource, UserResource,RecordResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(GuestResource())
v1_api.register(TableResource())
v1_api.register(RecordResource())
handler404 = 'clients.views.handler404'

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'clients.views.index',),
    url(r'^test_view/$', 'clients.views.test_view',),
    url(r'^login/$', 'clients.views.login'),
    url(r'^logout/$', 'clients.views.logout'),
    url(r'^register/$', 'clients.views.register'),
    url(r'^loggedin/$', 'clients.views.dashboard'),
    url(r'^update/$', 'clients.views.update_default'),
    url(r'^api_old/$', 'clients.views.api'),
    url(r'^waitlist/$', 'clients.views.waitlist'),
    url(r'^checkout/$', 'clients.views.checkout'),
    url(r'^settings/$', 'clients.views.admin_settings'),
    url(r'^dashboard/$', 'clients.views.dashboard'),
    url(r'^add/$', 'clients.views.add'),
    url(r'^countdown/$', 'clients.views.countdown'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^seated/$', 'clients.views.seated'),
    url(r'^get_waiting_list_of_table/', 'clients.views.get_waiting_list_of_table'),
    url(r'^analytics/$', 'clients.views.analytics'),    
    url(r'^records/$', 'clients.views.ShowRecords'),
    url(r'^JSON_records/$', 'clients.views.JSON_records'),
    url(r'^permission_denied/$', 'clients.views.permission_denied'),
    url(r'^front/$', 'clients.views.front'),
    url(r'^sendsms/$', 'clients.views.sendsms'),
    url(r'^adduser/$', 'clients.views.adduser'),
    url(r'^seatUser/$', 'clients.views.seatUser'),
    url(r'^noShow/$', 'clients.views.noShow'),
    url(r'^notifyGuest/$', 'clients.views.notifyGuest'),
    url(r'^firstLogin/$', 'clients.views.firstLogin'),
    url(r'^f/(\d+)/(\d+)/$', 'clients.views.feedback'),
    url(r'^feedbacks/$', 'clients.views.feedback_display'),
    url(r'^core/$', 'clients.views.core_function'),
    url(r'^dev/$', 'clients.views.dev'),
    url(r'^feedback/$', 'clients.views.feedback_service'),
    url(r'^feedbackManager/$', 'clients.views.feedbackManager'),
    url(r'^change_rating_texts/$', 'clients.views.change_rating_texts'),
    url(r'^create_questions/$', 'clients.views.create_questions'),
    url(r'^questions_to_show/$', 'clients.views.questions_to_show'),
    



    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()