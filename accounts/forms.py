from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *
from emailsender.models import *

class MyModelChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return obj.name

class UserForm(forms.ModelForm):
	username = forms.CharField(max_length=100)
	first_name = forms.CharField(max_length=100)
	is_staff = forms.BooleanField(required=False)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'is_staff')

class EditUserForm(forms.ModelForm):
	first_name = forms.CharField(max_length=100)
	is_staff = forms.BooleanField(required=False)

	class Meta:
		model = User
		fields = ('first_name', 'is_staff')

class UserInfoForm(forms.ModelForm):
	email_to = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "5", }), required=True)

	class Meta:
		model = UserInfo
		fields = ('email_to',)

class EmailForm(forms.Form):
	campaign = forms.ModelChoiceField(queryset=Campaign.objects.all().order_by('-created'), to_field_name="name", initial=-1)
	sponsor = forms.CharField(max_length=100)
	email_to = forms.CharField(max_length=1000, required=True)
	subject = forms.CharField(max_length=100, required=True)
	body = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "25", }), required=True)
	attachment = forms.BooleanField(required=False)
	newsletter = forms.BooleanField(required=False)
	picture = forms.BooleanField(required=False)