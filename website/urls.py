from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls', namespace='users')),
    path('chat/', include('chat.urls')),
    path('profile/', include('profiles.urls', namespace='profiles')),
]

