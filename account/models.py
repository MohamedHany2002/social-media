from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here
class profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image= models.ImageField(upload_to='images/',blank=True,null=True)
    date_birth=models.DateField(blank=True,null=True)

    def get_absolute_url(self):
        return reverse('detail',kwargs={'username':self.user.username})



class contact(models.Model):
    user_from = models.ForeignKey(User,on_delete=models.CASCADE,related_name='rel_from_set')
    user_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True,db_index=True)


    # following = models.ManyToManyField('self',through=Contact,related_name='followers',symmetrical=False)
    # if we have a model but user and wanna avoid building custom user model

    # class Meta:
    #     unique_together=('user_from','user_to',)

class tags(models.Model):
    text=models.CharField(max_length=100)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE,related_name='tags')
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')

    def __str__(self):
        return self.text

# for user model only other approach for editable model use many to many above
User.add_to_class('following',models.ManyToManyField('self',through=contact,related_name='followers',symmetrical=False))



