from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/',views.Login,name="Login"),
    path('search/', views.search, name='search'),
    path('site/<post>', views.site, name='site'),
]