from django import template
from django.urls import resolve

register = template.Library()


@register.filter
def is_current_page(request, param):
    return request.path[1:] == param
