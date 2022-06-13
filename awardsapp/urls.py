from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework import routers



urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('search/', views.search, name='search'),
    path('site/<post>', views.site, name='site'),
    path('profile/<username>/', views.profile, name='profile'),
    path('<username>/profile', views.user_profile, name='userprofile'),
    path('profile/<username>/settings', views.edit_profile, name='edit'),
]