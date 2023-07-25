from django.contrib import admin
from .views import *
from django.urls import path, include

urlpatterns = [
    path('my', MyProfile.as_view()),
    path('list_groups/', list_groups, name='list-groups'),
    path('group_user_list_view/', user_group_list_view,
         name='group_user_list_view'),
    path('user_list_create/', user_list_create, name='user_list_create'),
    path('technician_list/', technician_list, name='technician_list'),
]
