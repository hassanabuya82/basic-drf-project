from django.contrib.auth.models import User
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', Register.as_view()),
    path('activate/', ActivateAccount.as_view()),
    path('resend_activate/', ResetActivate.as_view()),
    path('token/', CustomAuthToken.as_view()),
    path('reset/', pass_reset),
    path('reset-confirm/', reset_confirm),
    path('password/', password),
]
