from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import image_post


@reciever(m2m_changed,sender=image_post.likes.through)

def count_likes(sender,instance,**kwargs):
    instance.likes_count=instance.likes.count()
    instance.save()