from django.urls import  path
from .views import *

urlpatterns = [
    path('', recharge, name='recharge'),
    path('add-payment', recharge, name='add-payment'),
    path('recharge-history', recharge_history)
]