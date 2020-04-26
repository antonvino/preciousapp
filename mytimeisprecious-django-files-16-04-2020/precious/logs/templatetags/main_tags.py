# encoding: utf-8

from django import template
from django.conf import settings

register = template.Library()

@register.assignment_tag
def get_active_page(request):
    """
    Return page depending on the path
    """
    path = request.path
    print path

    if path == '/':
        return "home"
    elif path.startswith('/week/'):
        return 'week'
    elif path.startswith('/month/'):
        return 'month'
    elif path.startswith('/tags/'):
        return "tags"
