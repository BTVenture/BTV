from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_page, name='login'),
    path('sign-up/', sign_up, name='signup'),
    path('reset-password/', reset_password, name='reset-password'),
    path('verify-account/<str:param1>/<uuid:param2>/', verify_account),
    path('change-password/<str:param1>/<uuid:param2>/', change_password, name='change-password-with-params'),  # URL with parameters
    # path('change_password/', confirmation_password, name='confirm_password'),  # URL without parameters
    path('change-password/', confirm_password, name='change-password'),
    path('send-activation-link/', resend_activation_email, name='send-activation-link')
]
