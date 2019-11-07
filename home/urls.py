from django.urls import path, include

from home.views import homepage, signup

urlpatterns = [
    path('' , homepage),
    path('signup/', signup)
]