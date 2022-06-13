from django.urls import path
from . import views

urlpatterns = [
    path('prof/', views.getProfile),
    path('user/', views.getUser),
    path('projects/', views.getPost),
    path('add/', views.addItem),
]