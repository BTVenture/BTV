from django.db import models
import uuid

# Create your models here.

class account_details(models.Model):
    payment_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    user = models.OneToOneField('authenticate.User_Model', on_delete=models.CASCADE)
    account_number = models.TextField(max_length=20, blank=True, null=True)
    ifsc_code = models.TextField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} : {self.account_number}'
