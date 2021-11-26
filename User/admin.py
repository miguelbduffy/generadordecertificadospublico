from django.contrib import admin
from django.conf import settings
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class ProfileAdmin(admin.ModelAdmin):
    list_display=("user","on_hold_user","confirmation_code","active")
    list_filter=("user","on_hold_user","confirmation_code","active")

    # def first_name(self):
    #     return self.first_name

    # def last_name(self):
    #     return self.user.last_name

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login','password') # Added last_login

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Profile, ProfileAdmin)
