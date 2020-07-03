from django.db import models


from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE) 
	profile_pic =  models.FileField(upload_to='images/')
	user_role = models.CharField(max_length=30)

	def __str__(self):
		return self.user.username

class Astro_Profile(models.Model):
	profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
	skill = models.CharField(max_length=50)
	experience = models.IntegerField()
	origin = models.CharField(max_length=50)

	def __str__(self):
		return self.profile.user.username


class Wallet(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE) 
	balance = models.IntegerField(default=100)
	def __str__(self):
		return self.user.username