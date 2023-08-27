
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.about,name = 'about'),
    path('login', views.login, name = 'login'),
    path('logout', views.logout, name='logout'),
    
    path('user', views.user, name = 'user'),
    path('user',views.dashboard, name='user'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('agents', views.agents, name='agents'),
    path('home', views.home, name = 'home'),
    path('property', views.property, name = 'property'),
    path('support', views.support, name='support'),
    
    path('property_registration', views.property_registration, name='property_registration'),
    path('property_save', views.property_save, name='property_save'),

    path('hire_support', views.hire_support, name='hire_support'),
    path('remove_support', views.remove_support, name= 'remove_support'),
    
    path('auction', views.auction, name = 'auction'),
    path('join_auction', views.join_auction, name='join_auction'),
    path('leave_auction', views.leave_auction, name='leave_auction'),
    
    path('auction_property_submission', views.auction_property_submission, name='auction_property_submission'),
    path('auction_property_removal', views.auction_property_removal, name='auction_property_removal'),
    
    path('user_edit_profile', views.user_edit_profile, name= 'user_edit_profile'),
    path('agent_edit_profile',views.user_edit_profile, name = 'agent_edit_profile'),
    path('admin_edit_profile',views.user_edit_profile, name = 'admin_edit_profile'),
    

    path('agent_img',views.agent_img, name='agent_img'),
    path('property_edit_info', views.property_edit_info, name= 'property_edit_info'),
    path('fetch_property', views.fetch_property, name= 'fetch_property'),
    path('propertyId_submit', views.propertyId_submit, name='propertyId_submit'),
    path ('hire_agent', views.hire_agent , name='hire_agent'),
    
    path('delete_from_market',views.delete_from_market, name = 'delete_from_market'),
    path('delete_property', views.delete_property, name = 'delete_property'),
    path('agent_remove', views.agent_remove , name="agent_remove"),
    path ('remove_propertyId_submission' , views.remove_propertyId_submission , name='remove_propertyId_submission'),
    
    path('add_auction_property', views.add_auction_property, name= 'add_auction_property'),
    path('remove_auction_property', views.remove_auction_property, name= 'remove_auction_property'),
    
    path('create_auction', views.create_auction, name= 'create_auction'),
    path('cancel_auction', views.cancel_auction, name= 'cancel_auction'),
    path('start_auction', views.start_auction, name= 'start_auction'),
    path('end_auction', views.end_auction, name= 'end_auction'),
    path('make_supervisor', views.make_supervisor, name= 'make_supervisor'),
    path('remove_supervisor', views.remove_supervisor, name= 'remove_supervisor'),
    path('set_supervisor', views.set_supervisor, name= 'remove_supervisor'),

    path('buy_property', views.buy_property, name = 'buys_prorperty')

    
]