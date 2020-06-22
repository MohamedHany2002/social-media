from django.shortcuts import render,HttpResponse,redirect,reverse,get_object_or_404
from .forms import loginForm,UserRegistrationForm,ProfileEditForm,UserEditForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from common.decorators import ajax_required
from django.views.decorators.http import require_POST
from .models import contact
from actions.utils import create_action
from actions.models import Action



# Create your views here.
@login_required
def login_user(request):
    if request.method=='POST':
        loginform=loginForm(request.POST)
        if loginform.is_valid():
            print("ok")
            username=loginform.cleaned_data['username']
            password=loginform.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect("dashboard")
            else:
                return HttpResponse('user not exist')

    else:
        loginform=loginForm()
    return render(request,"login.html",{'form':loginForm})

def user_logout(request):
    logout(request)
    return render(request,"logout.html")

@login_required
def dashboard(request):
    actions=Action.objects.exclude(user=request.user)
    print(actions,"second")
    #values_list because we don't need to user these objects son we don't need to retrieve
    # or query all the objects but we need to filter by them
    following_ids=request.user.following.values_list('id',flat=True)
    print(request.user.following.all())
    if following_ids:
        actions=actions.filter(user_id__in=following_ids)
        print(actions,"second")
    actions=actions.select_related('user','user__profile').prefetch_related('content_object')[:10]
    return render(request,"dashboard.html",{'section':'new','actions':actions})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            newprofile=profile.objects.create(user=new_user)
            create_action(new_user,'created',newprofile)
            return render(request,'register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'register.html',{'user_form': user_form}) 

@login_required
def edit(request):
    if request.method=='POST':
        profileform=ProfileEditForm(request.POST,instance=request.user.profile,files=request.FILES)
        userform=UserRegistrationForm(request.POST,instance=request.user)
        if profileform.is_valid and userform.is_valid():
            userform=userform.save(commit=False)
            userform.set_password(request.POST['password'])
            userform.save()
            profileform.save(commit=False)
            profileform.user=userform
            user=User.objects.get(id=userform.id)
            login(request,user)
            messages.success(request,"profile edited succesfully")
            return redirect("dashboard")
    else:
        profileform=ProfileEditForm(request.POST,instance=request.user.profile,files=request.FILES)
        userform=UserRegistrationForm(request.POST,instance=request.user)
        return render(request,"edit.html",{'profileform':profileform,'userform':userform})

# @login_required
def user_list(request):
    users=User.objects.filter(is_active=True)
    print(users)
    return render(request,"user_list.html",{'users':users})
# @login_required
def user_detail(request,username):
    user=get_object_or_404(User,username=username)
    return render(request,"user_detail.html",{'user':user})


@ajax_required
@require_POST
@login_required
def follow_user(request):
    id=request.POST['id']
    action=request.POST['action']
    # try:
    user=get_object_or_404(User,id=id)


    if action=='follow':
        contact.objects.get_or_create(user_from=request.user,user_to=user)
        create_action(request.user,"fonnows",user)
        # Action.objects.create(user=request.user,verb="follows",content_object=user)

        return JsonResponse({'status':'ok'})

    elif action=='unfollow':
        contact.objects.filter(user_from=request.user,user_to=user).delete()
        Action.objects.create(user=request.user,verb="unfollows",content_object=user)

        return JsonResponse({'status':'ok'})
    # except:
        # pass
    return JsonResponse({'status':'ko'})
        
