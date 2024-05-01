from django.urls import path
from .views import *

urlpatterns = [
    path('', account_page),
    path('add-bank-detail/', add_bank_account_information, name='add-bank-detail')
]