from django import template 
from core.models import Order 

register = template.Library()

@register.filter
def cart_item_count():
    qs = Order.objects.filter(ordered=False)
    if qs.exists():
        return qs[0].items.count()
    return 0

