from django.db import models
import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver

from wallet.models import Wallet_Model

# Create your models here.

class Generated_Amount_History(models.Model):
    gah_id = models.UUIDField(unique=True, primary_key=True, editable=False, default=uuid.uuid4, blank=False, null=False)
    amount = models.IntegerField()
    request_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('authenticate.User_Model', on_delete=models.CASCADE, blank=False, null=False)


@receiver(post_save, sender=Generated_Amount_History)
def transfer_to_wallet(sender, instance, created, **kwargs):
    if created:
        wallet = Wallet_Model.objects.get(user=instance.user)
        wallet.balance_amount += instance.amount
        wallet.save()



