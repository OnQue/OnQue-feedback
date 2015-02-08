from clients.models import table
from guests.models import Guest
from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext as _

# class MyForm(forms.Form):
# 	n_of_table = forms.IntegerField(required=True)
# 	status = forms.BooleanField(required=True)

class MyForm(forms.ModelForm):
    class Meta:
            model=table
            fields = ['status']

class AdminSettingsForm(forms.ModelForm):
    class Meta:
        model = table
        fields = ['n_of_table','status']

class AddGuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['mobile']



