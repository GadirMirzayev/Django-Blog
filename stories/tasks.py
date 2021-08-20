from celery import shared_task
from stories.models import Subscriber, Recipe
from django.db.models import Count
from food_stories import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string



@shared_task
def send_emails():
    subscribers = Subscriber.objects.filter(is_active=True).values_list('email', flat=True)
    recipes = Recipe.objects.annotate(Count('comments__text')).order_by('-comments__text__count')[:3]
    subject = ('Latest popular recipes for you')
    context = {  
        'recipes':recipes,
        'SITE_ADRESS': settings.SITE_ADDRESS
      }
    body = render_to_string('emails/email-subscribers.html', context)    
    mail = EmailMessage(subject, to= subscribers, from_email=settings.EMAIL_HOST_USER, body=body)
    mail.content_subtype='html'
    mail.send()