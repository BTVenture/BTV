from django.urls import path
from .views import *


urlpatterns = [
    path('', income_page),
    path('add-to-wallet/<int:transfer_amount>', transfer_amount)
]