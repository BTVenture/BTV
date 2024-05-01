from django.urls import path
from .views import *

urlpatterns = [
    path('', commission_history_page),
]