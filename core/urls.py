from django.urls import path
from .views import *

urlpatterns = [
    path('main/', index, name='index'),
    path('', login_view, name='login_view'),
]