# frontend/templatetags/frontend_extras.py
from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply the arg and the value"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def dictvalue(dictionary, key):
    """Get value from dictionary by key"""
    if dictionary:
        for item in dictionary:
            if str(item.id) == str(key):
                return item
    return None

@register.filter
def get(obj, attr):
    """Get attribute value from object"""
    return getattr(obj, attr, '')