from django.urls import path
from . import views

app_name= 'blog'
urlpatterns = [
    path('',views.index,name ='index'),
    path('old_url/',views.old_url_redirect,name='old_url'),
    path('new_welcome_url',views.new_url_view ,name = 'new_page_url'),
    path('detail/<str:slug>', views.detail,name='detail'),
    path('contact/',views.contact,name='contact'),
    path('about',views.about,name='about'),
    #path('profile',views.profile_page,name='profile'),
    
    
]