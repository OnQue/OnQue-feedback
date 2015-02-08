from django.contrib import admin

# Register your models here.
from guests.models import Guest, PersonalRecord

class GuestAdmin(admin.ModelAdmin):
    list_display = ('mobile', 'name','age','created_at','last_visited','status',)
    search_fields = ('mobile',)
    list_filter = ('status',)
    fields = ('status','table_no','current',)

admin.site.register(Guest, GuestAdmin)
admin.site.register(PersonalRecord)