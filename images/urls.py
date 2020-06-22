
from django.urls import path
from . import views


urlpatterns = [
    path('create/',views.create,name='create'),
    path('detail/<int:id>',views.detail,name='detail'),
    path('like/',views.like,name='like'),
    path('',views.image_list,name='list'),

]


