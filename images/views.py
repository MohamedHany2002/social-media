from django.shortcuts import render,redirect,get_object_or_404
from .forms import create_image
from django.contrib import messages
from django.core.files.base import ContentFile
from django.utils.text import slugify
from urllib import request
from .models import image_post
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from common.decorators import ajax_required
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from actions.models import Action
from actions.utils import create_action
from django.db.models import Count
import redis
from django.conf import settings

r=redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)


# Create your views here.

def create(request):
    if request.method=='POST':
        create_form=create_image(request.POST)
        if create_form.is_valid():
            cd=create_form.save(commit=False)
            cd.user=request.user
            cd.save()
            messages.success(request,"success")
            create_action(request.user,"bookmarked",cd)
            return redirect('create')
    else:
        create_form=create_image(request.GET)
    return render(request,"create.html",{'form':create_form})

def detail(request,id=id):
    myimage= get_object_or_404(image_post,id=id)
    image_views = r.incr('image{}'.format(myimage.id))
    return render(request,"detail.html",{'image':myimage,'image_views':image_views})

@ajax_required
@require_POST
@login_required
def like(request):
    id=request.POST['id']
    action=request.POST['action']
    try:
        myimage=get_object_or_404(image_post,id=id)
        if action == 'like':
            myimage.likes.add(request.user)
            # create_action(request.user,"liked",myimage)
        elif action == 'unlike':
            myimage.likes.remove(request.user)
            # create_action(request.user,"unliked",myimage)

        return JsonResponse({'status':'ok'})
    except:
        pass
    return JsonResponse({'status':'ko'})

@login_required
def image_list(request):

    # that can cost the quries retrieved  
    # images=image_post.objects.annotate(total_likes=Count('likes')).order_by('-total_likes')
    # another way to make field that carry the count and order by count 
    # that count changes by signal or overriding save method
    images=image_post.objects.order_by('-likes_count')
    # this approach is less expensive sql query
    for image in images:
        print(image.title,image.likes.count())
    # paginator = Paginator(images, 1)
    # page = request.GET.get('page')
    # try:
    #     images = paginator.page(page)
    # except PageNotAnInteger:
    #     images = paginator.page(8)
    # except EmptyPage:
    #     if request.is_ajax():
    #         return HttpResponse('')
    #     images = paginator.page(paginator.num_pages)
    # if request.is_ajax():
    #     return render(request,'list_ajax.html',{'section': 'images', 'images': images})
    return render(request,'list.html',{'section': 'images', 'images': images})


