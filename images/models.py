from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.

class image_post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_images')
    slug=models.SlugField()
    title=models.CharField(max_length=100,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    url=models.URLField(null=True,blank=True)
    image=models.ImageField(upload_to='images/')
    created = models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(User,related_name='likes_images',blank=True)
    likes_count=models.PositiveIntegerField()

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super(image_post,self).save(*args,**kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail",kwargs={'id':self.id})


