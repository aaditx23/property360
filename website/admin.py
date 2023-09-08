from django.contrib import admin

# Register your models here.

from .models import User, Employee, Agent, Property, Auction, Auction_Property, Admin, Support, Maintains, Hires, Seller, Session

admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Agent)
admin.site.register(Property)
admin.site.register(Auction)
admin.site.register(Auction_Property)
admin.site.register(Admin)

admin.site.register(Support)
admin.site.register(Maintains)

admin.site.register(Hires)
admin.site.register(Seller)

admin.site.register(Session)
