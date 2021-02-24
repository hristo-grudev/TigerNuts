from django.contrib import admin

from accounts.models import UserProfile, Subscribers
from common.models import Item, ItemImages, OrderItem, Address, WishList, Coupon, Order, Payment, PaymentStripe, Tags


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'shipping_address',
                    'payment',
                    'coupon'
                    ]


class SubscribersAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed', ]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'default'
    ]
    list_filter = ['default', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


admin.site.register(Item)
admin.site.register(ItemImages)
admin.site.register(UserProfile)
admin.site.register(Subscribers, SubscribersAdmin)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(WishList)
admin.site.register(Coupon)
admin.site.register(Payment)
admin.site.register(PaymentStripe)
admin.site.register(Tags)
