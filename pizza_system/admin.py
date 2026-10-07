from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Pizza)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'pizza', 'address', 'order_time')
    exclude = ['user']

admin.site.register(Order, OrderAdmin)
admin.site.register(Topping)