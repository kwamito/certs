from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_admin, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='cate/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='cate/logout.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
