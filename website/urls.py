
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.about,name = 'about'),
    path('user', views.user, name = 'user'),
    path('login', views.login, name = 'login'),
    path('agents', views.agents, name='agents'),
    path('home', views.home, name = 'home'),
    path('property', views.property, name = 'property'),
    path('logout', views.logout, name='logout'),
    path('property_img', views.property_img, name = 'property_img'),
    path('support', views.support, name='support'),
    path('property_registration', views.property_registration, name='property_registration')
    
]