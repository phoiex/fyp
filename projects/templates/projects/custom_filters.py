# 在您的应用程序下的templatetags目录中创建custom_filters.py文件
from django import template

register = template.Library()

@register.filter
def get(dictionary, key):
    return dictionary.get(key)