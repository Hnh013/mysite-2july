from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Astro_Profile, Wallet


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    first_name = forms.CharField(max_length=200, required=True)
    last_name = forms.CharField(max_length=200, required=True)
   
   
    class Meta:
    	model = User
    	fields = ('first_name','last_name','email', 'username', 'password1', 'password2')

    

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('user_role',) 


class AstroProfileForm(forms.ModelForm):
	
	class Meta:
		model = Astro_Profile
		fields = ('skill','experience','origin') 

class RechargeForm(forms.ModelForm):
	class Meta:
		model = Wallet
		fields = ('balance',)
