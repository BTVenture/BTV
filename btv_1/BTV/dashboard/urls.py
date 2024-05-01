from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard),
    path('logout/', logout_user_account)
]