from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.


class Action(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    verb = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE,null=True,blank=True,related_name='actions')
    object_id=models.PositiveIntegerField(null=True,blank=True)
    content_object=GenericForeignKey('content_type','object_id')

    def __str__(self):
        return '{} {} {}'.format(self.user,self.verb,self.content_object)


    class Meta:
        ordering=('-created',)

