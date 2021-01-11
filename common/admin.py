from django.contrib import admin

from accounts.models import RegistrationData
from common.models import Item, ItemImages

admin.site.register(Item)
admin.site.register(ItemImages)
admin.site.register(RegistrationData)
