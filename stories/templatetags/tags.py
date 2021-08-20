from django.template import Library
from stories.models import *
from stories.forms import SubscriberForm
register = Library()


@register.simple_tag
def get_categories(n=None):
    return Category.objects.all()[:n]


@register.simple_tag
def get_subscriber():
    return SubscriberForm