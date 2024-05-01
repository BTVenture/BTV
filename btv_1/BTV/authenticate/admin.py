from django.contrib import admin
from .models import *

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'referal_id')

admin.site.register(User_Model ,CustomUserAdmin)





