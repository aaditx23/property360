
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.about,name = 'about'),
    path('user', views.user, name = 'user'),
    path('dashboard', views.dashboard, name='dashboard'),
    # path('agent_dashboard', views.agent_dashboard, name='agent_dashboard'),
    path('login', views.login, name = 'login'),
    path('agents', views.agents, name='agents'),
    path('home', views.home, name = 'home'),
    path('property', views.property, name = 'property'),
    path('logout', views.logout, name='logout'),
    path('support', views.support, name='support'),
    path('property_registration', views.property_registration, name='property_registration'),
    path('property_save', views.property_save, name='property_save'),
    path('hire_support', views.hire_support, name='hire_support'),
    path('auction', views.auction, name = 'auction'),
    path('join_auction', views.join_auction, name='join_auction'),
    path('leave_auction', views.leave_auction, name='leave_auction'),
    path('auction_property_submission', views.auction_property_submission, name='auction_property_submission'),
    path('user_edit_profile', views.user_edit_profile, name= 'user_edit_profile'),
    path('agent_edit_profile',views.user_edit_profile, name = 'agent_edit_profile'),
    path('agent_img',views.agent_img, name='agent_img'),
    path('user',views.dashboard, name='user'),
    path('property_edit_info', views.property_edit_info, name= 'property_edit_info'),
    path('fetch_property', views.fetch_property, name= 'fetch_property'),
    path('propertyId_submit', views.propertyId_submit, name='propertyId_submit'),
    path ('hire_agent', views.hire_agent , name='hire_agent'),
    path('delete_property',views.delete_property, name = 'delete_property'),
    path('add_auction_property', views.add_auction_property, name= 'add_auction_property'),

    
]