from django.urls import path
#from .  views import UserEditView,PasswordsChangeView
from . import views
from django.contrib.auth import views as auth_views
#from .views import password_success
app_name= 'members'
urlpatterns = [ 
    path('register/',views.register,name='register'),
    path('login', views.login, name='login'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('forgot_password',views.forgot_password,name="forgot_password"),
    path('reset_password/<uidbase64>/<token>', views.reset_password , name='reset_password'),
    path('new_post',views.new_post, name ='new_post'),
    path('edit_post/<int:post_id>',views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>',views.delete_post, name='delete_post'), 
    path('publish_post/<int:post_id>',views.publish_post,name='publish_post'),
    #path('register/',UserRegisterView.as_view(),name='register'),
   # path('edit_profile/',UserEditView.as_view(),name='edit_profile'),
    #path('password/',auth_views.PasswordChangeView.as_view(template_name = 'registration/change-password.html')),
    #path('password/',PasswordsChangeView.as_view(template_name = 'registration/change-password.html')),
    #path('password_success', password_success,name="password_success"),
    #path('home/', views.userView, name='userView'), 
    #path('login/', views.login_user, name='loginpage'),
    path('logout', views.logout, name='logoutpage'),
    #path('login/',views.login_view,name='login'),
]