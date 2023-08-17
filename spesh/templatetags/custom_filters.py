from django import template
from django.utils.timesince import timesince
from datetime import datetime
from django.utils import timezone
register = template.Library()

@register.filter
def custom_timesince(value):
    now = timezone.now()
    if value < now:
        return timezone.timesince(value) + ' ago'
    return 'just now'