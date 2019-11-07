from django.urls import path, include

from home.views import homepage, signup, logout_view, login_view

urlpatterns = [
    path('' , homepage),
    path('signup/', signup),
    path('logout/', logout_view),
    path('login/', login_view)
]
