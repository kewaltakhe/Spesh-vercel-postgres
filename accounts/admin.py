from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'is_staff', ] 
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('userbio','profile_pic')}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('userbio','profile_pic')}),)


admin.site.register(CustomUser,CustomUserAdmin)
