from django import template
from urllib.parse import quote_plus

register=template.Library()
#You can use register.filter() as a decorator instead:
@register.filter
def urlify(value):
    return quote_plus(value)