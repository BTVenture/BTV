from django.db import models
from uuid import uuid4
from dashboard.models import Product

from django.db.models.signals import post_save
from django.dispatch import receiver



class Wallet_Model(models.Model):
    wallet_id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    user = models.OneToOneField('authenticate.User_Model', on_delete=models.CASCADE)
    balance_amount = models.IntegerField(default=50.00)

    def __str__(self):
        return f'{self.user.username} : {self.wallet_id}'


class Admin_Payment_Id(models.Model):
    upi_id = models.TextField(max_length=100)

    def __str__(self):
        return f'Admin UPI ID : {self.upi_id}'


class Payment_Details(models.Model):
    payment_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey('authenticate.User_Model', on_delete=models.CASCADE)
    payment_amount = models.IntegerField(default=0.00)
    upi_id = models.CharField(max_length=100)
    utr_id = models.CharField(max_length=100, unique=True)
    payment_request_time = models.DateTimeField(auto_now_add=True)
    payment_choices = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    payment_completed = models.CharField(max_length=10, choices=payment_choices, default='PENDING')

    def __str__(self):
        return f'{self.user.username} - Payment ID : {self.payment_id}'


class Buyed_Products(models.Model):
     user = models.ForeignKey('authenticate.User_Model', on_delete=models.CASCADE, blank=False, null=False)
     product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)
     purchased_date = models.DateTimeField(auto_now_add=True)




