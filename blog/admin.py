from django.contrib import admin

# Register your models here.
from .models import Profile, Astro_Profile

admin.site.register(Profile)

admin.site.register(Astro_Profile)