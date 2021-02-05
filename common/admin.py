from django.contrib import admin

from accounts.models import UserProfile
from common.models import Item, ItemImages, OrderItem, Address, WishList, Coupon, Order

admin.site.register(Item)
admin.site.register(ItemImages)
admin.site.register(UserProfile)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(WishList)
admin.site.register(Coupon)
