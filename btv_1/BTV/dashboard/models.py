from django.db import models
import uuid

# Create your models here.


class Product(models.Model):
    product_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, blank=False, null=False)
    product_name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    product_price = models.IntegerField(default=0, blank=False, null=False)
    generate_per_day = models.IntegerField(default=0 , blank=False, null=False)
    product_description = models.TextField(max_length=500, blank=True, null=True)
    product_image = models.ImageField(upload_to='static/images/', blank=False, null=False)
    validity_time = models.IntegerField(default=1, blank=False, null=False)

    def __str__(self):
        return self.product_name