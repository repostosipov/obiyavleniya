from django import template
from ..models import Category
from users.models import Profile

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.simple_tag()
def get_city():
    return Profile.objects.values_list('city', flat=True)