from django.db import models
from dashboard.models import Product

# Create your models here.
class Comission_History(models.Model):
    username_get_commission = models.CharField(max_length=100)
    email_get_commission = models.CharField(max_length=100)
    comission_amount = models.IntegerField(blank=False, null=False)
    purchased_product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey('authenticate.User_Model', on_delete=models.CASCADE, blank=False, null=False)
    date = models.DateField(auto_now_add=True)

