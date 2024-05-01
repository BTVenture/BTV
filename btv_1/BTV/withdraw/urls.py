from django.urls import path
from .views import *

urlpatterns = [
    path('', withdraw, name='withdraw'),
    path('history/', history, name='history')
]