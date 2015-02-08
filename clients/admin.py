from django.contrib import admin

# Register your models here.
from clients.models import Record, table, Feedback

class RecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile', 'date','directly_seated','take_away','no_show','id','feed_match')
    search_fields = ('mobile','user__username')
    list_filter = ('date','take_away','no_show','user',)

class tableAdmin(admin.ModelAdmin):
    list_display = ('user','mobile', 'rest_name', 'n_of_table','status','waiting_list','seated','first_login')
    search_fields = ('user__username','rest_name')
    fields = ('rest_name','n_of_table','first_login','status','waiting_list','seated')

class FeedbackAdmin(admin.ModelAdmin):
	list_display = ('user','mobile','date','service','ambience','food','overall_exp','staff_friend')

admin.site.register(Record,RecordAdmin)
admin.site.register(table,tableAdmin)
admin.site.register(Feedback,FeedbackAdmin)