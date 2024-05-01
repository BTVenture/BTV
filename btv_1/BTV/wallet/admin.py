from django.contrib import admin
from .models import Admin_Payment_Id
from django.utils.translation import gettext_lazy as _
from .models import Payment_Details
from .models import Wallet_Model

# Register your models here.

admin.site.register(Admin_Payment_Id)

def mark_as_pending(modeladmin, request, queryset):
    queryset.update(payment_completed='PENDING')

def mark_as_approved(modeladmin, request, queryset):
    queryset.update(payment_completed='APPROVED')

def mark_as_rejected(modeladmin, request, queryset):
    queryset.update(payment_completed='REJECTED')

class PaymentStatusFilter(admin.SimpleListFilter):
    title = _('Payment Status')
    parameter_name = 'payment_status'

    def lookups(self, request, model_admin):
        return (
            ('pending', _('Pending')),
            ('approved', _('Approved')),
            ('rejected', _('Rejected')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'pending':
            return queryset.filter(payment_completed='PENDING')
        elif self.value() == 'approved':
            return queryset.filter(payment_completed='APPROVED')
        elif self.value() == 'rejected':
            return queryset.filter(payment_completed='REJECTED')

class PaymentDetailsModelAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'payment_completed']
    list_filter = [PaymentStatusFilter]
    search_fields = ['payment_completed']
    actions = [mark_as_pending, mark_as_approved, mark_as_rejected]

    def save_model(self, request, obj, form, change):
        if obj.payment_completed == 'APPROVED' and change:

            # Assuming there's a one-to-one relationship between user and wallet
            user_wallet = Wallet_Model.objects.get(user=obj.user)
            user_wallet.balance_amount += obj.payment_amount
            user_wallet.save()

        super().save_model(request, obj, form, change)

admin.site.register(Payment_Details, PaymentDetailsModelAdmin)
