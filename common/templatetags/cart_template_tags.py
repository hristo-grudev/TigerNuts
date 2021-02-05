from django import template
from common.models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
<<<<<<< HEAD
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
=======
    qs = Order.objects.filter(user=user, ordered=False)
    if qs.exists():
        return qs[0].items.count()
>>>>>>> 9998414 (change buy it now)
    return 0
