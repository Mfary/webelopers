from django.contrib import admin
from django.urls import path, include

from home.views import homepage

urlpatterns = [
    path('' , homepage)
]