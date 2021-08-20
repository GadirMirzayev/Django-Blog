# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from stories.models import Recipe,Comment
# from django.contrib.auth import get_user_model


# User = get_user_model()


# @receiver(post_save,sender=Recipe)
# def is_approved_recipe(sender,instance,**kwargs):
#     if instance.is_approved==False:
#         Comment.objects.create(recipe=instance,author=User.objects.filter(is_superuser=True).first(), message="Very Good Recipe!")
#         instance.is_approved=True
#         instance.save()