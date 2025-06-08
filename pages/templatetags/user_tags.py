from django import template

from client.models import Barber

register = template.Library()

@register.filter
def is_barber(user):
    try:
        return Barber.objects.filter(user=user).exists()
    except:
        return False