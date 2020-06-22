from django import forms
from .models import image_post
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

class create_image(forms.ModelForm):
    # url=forms.URLField(widget=forms.HiddenInput,required=False)
    class Meta:
        model=image_post
        fields=['url','title','description']

    # def clean_url(self):
    #     url=self.cleaned_data['url']
    #     print(url,'kjmkj')
    #     extensions=['jpg','jpeg']
    #     extension=url.rsplit('.',1)[1].lower()
    #     if extension not in extensions:
    #         raise forms.ValidationError('not valid image')
    #     return url

    def save(self, commit=True):
        image = super(create_image, self).save(commit=False)
        print(image.title)
        image_url = image.url
        image_name = '{}.{}'.format(slugify(self.cleaned_data['title']),image_url.rsplit('.', 1)[1].lower())
        # download image from the given URL
        response = request.urlopen(image_url)
        image.image.save(image_name,ContentFile(response.read()),save=False)
        if commit:
            image.save()
        return image



# def save(self, commit=True):
#     image = super(create_image, self).save(commit=False)
#     image_url=self.cleaned_data['url']
#     response=request.urlopen('image_url')
#     image_name='{}{}'.format(slugify(self.cleaned_data['title']),image_url.rsplit('.',1)[1].lower())
#     image.image.save(image_name,ContentFile(response.read()),save=False)
#     # do custom stuff
#     if commit:
#         image.save()
#     return image


















        