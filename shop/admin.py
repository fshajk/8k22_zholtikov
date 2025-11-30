from django.contrib import admin
from shop.models import Product, CartItem, Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CartItem)
admin.site.register(Product)
