
from django.urls import path,include
from . import views

urlpatterns = [
    path('login/',views.login_user,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('register/',views.register,name='register'),
    path('edit/',views.edit,name='edit'),
    path('user_list/',views.user_list,name='user_list'),
    path('user_detail/<username>',views.user_detail,name='user_detail'),
    path('follow/',views.follow_user,name='follow'),
    
]
