from tastypie.resources import ModelResource
from django.conf.urls import patterns, include, url
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication, MultiAuthentication, SessionAuthentication
from tastypie.authorization import Authorization
from guests.models import Guest
from clients.models import table,Record
from django.contrib.auth.models import User
from tastypie import fields


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get']
        detail_uri_name = 'username'

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<username>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

class GuestResource(ModelResource):
    class Meta:
        queryset = Guest.objects.all()
        resource_name = 'guest'
        excludes = ['last_visited']
        

class TableResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = table.objects.all()
        resource_name = 'table'
        detail_uri_name = 'username'

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<username>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
        
class RecordResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = Record.objects.all()
        resource_name = 'record'

        

        