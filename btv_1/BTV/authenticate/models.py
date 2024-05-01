import decimal

from django.db import models
from django.contrib.auth.models import AbstractUser
from .UserModelManager import CustomUserManager
import uuid
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.
from comission.models import Comission_History

from wallet.models import Wallet_Model
from recharge.models import account_details
from wallet.models import Buyed_Products


class User_Model(AbstractUser):
    id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, primary_key=True)
    email_token = models.UUIDField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, editable=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    referal_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    refered_by = models.UUIDField(null=True, blank=True, unique=False)
    date_time = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

@receiver(post_save, sender=User_Model)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet_Model.objects.create(user=instance)
        account_details.objects.create(user=instance)

@receiver(post_save, sender=Buyed_Products)
def add_commission_to_account(sender, instance, created, **kwargs):
    if created:
        try:
            user = User_Model.objects.get(referal_id=instance.user.refered_by)
            print(user)
            print(instance.user.refered_by)
            print(instance.user)
            if user != None :
                price = instance.product.product_price
                wallet = Wallet_Model.objects.get(user=user)
                amount_to_be_credited = price * 0.10
                wallet.balance_amount = wallet.balance_amount + amount_to_be_credited

                """
                    get the first procut and save the entire data 
                    adding the data for the commission history
                """
                commison = Comission_History(
                    user=user,
                    username_get_commission=instance.user.username,
                    email_get_commission=instance.user.email,
                    comission_amount=amount_to_be_credited,
                    purchased_product=instance.product
                )
                commison.save()
                wallet.save()
                print('save data')

        except Exception as e:
            print(e)