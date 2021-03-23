from .models import Basket, BasketProduct, Customer
from django.contrib import admin

admin.site.register(Customer)
admin.site.register(Basket)
admin.site.register(BasketProduct)
