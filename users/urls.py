from django.urls import path

from .views import home_view, signup, dashboard_view, slogin, logoutt, tlogin

app_name = "users"

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup, name='signup'),
    path('slogin/', slogin, name='slogin'),
    path('tlogin/', tlogin, name='tlogin'),
    path('logout/', logoutt, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
