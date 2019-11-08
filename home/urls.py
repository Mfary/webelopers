from django.urls import path, include

from home.views import homepage, signup, logout_view, login_view, contact_us, success, profile, change, panel, \
    make_course, show_courses, register_course

urlpatterns = [
    path('' , homepage),
    path('signup/', signup),
    path('logout/', logout_view),
    path('login/', login_view),
    path('contactus/', contact_us),
    path('success/', success),
    path('profile/', profile),
    path('change/', change),
    path('panel/', panel),
    path('make_course/', make_course),
    path('courses/', show_courses),
    path(r'^add/(\d+)', register_course),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
