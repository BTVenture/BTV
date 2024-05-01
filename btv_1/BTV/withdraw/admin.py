from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from .models import *

# Register your models here.
# admin.site.register(Withdraw_History)

def mark_as_pending(modeladmin, request, queryset):
    queryset.update(status='Pending')

def mark_as_approved(modeladmin, request, queryset):
    queryset.update(status='Approved')

def mark_as_rejected(modeladmin, request, queryset):
    queryset.update(status='Rejected')

class Status_Filter(admin.SimpleListFilter):
    title = 'Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'pending' :
            return queryset.filter(status='Pending')
        elif self.value() == 'approved' :
            return queryset.filter(status='Approved')
        elif self.value() == 'rejected':
            return queryset.filter(status='Rejected')

class WithdrawHistoryModelAdmin(admin.ModelAdmin):
    list_display = ['withdraw_id', 'status']
    list_filter = ['status']
    search_fields = ['status']
    actions = [mark_as_pending, mark_as_approved, mark_as_rejected]


admin.site.register(Withdraw_History, WithdrawHistoryModelAdmin)