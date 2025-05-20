# Create a custom_filters.py file in the templatetags directory under your application
from django import template

register = template.Library()

@register.filter
def get(dictionary, key):
    return dictionary.get(key)