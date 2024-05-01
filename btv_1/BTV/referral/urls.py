from django.urls import path
from .views import *

urlpatterns = [
    path('', referrals_page)
]