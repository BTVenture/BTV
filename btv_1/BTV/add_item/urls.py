from django.urls import path
from .views import *

urlpatterns = [
    path('item/<str:item_id>/', confirm_product),
    path('payment/<str:item_id>/', confirm_payment)
]