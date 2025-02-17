from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from django.urls import reverse
import logging
from blog.models import Post,AboutUs
from django.core.paginator import Paginator
from .forms import ContactForm
from django.contrib import messages

#https://github.com//jvlcode/bootstrap-blog-templates
#https://github.com/jvlcode/django5-blog-tutorial/blob/main/blog/management/commands/populate_posts.py
#posts = [
#        {'id':1,'title': 'post 1','content' : 'content of post 1'},
#       {'id':2,'title': 'post 2','content' : 'content of post 2'},
#      {'id':3,'title': 'post 3','content' : 'content of post 3'},
#     {'id':4,'title': 'post 4','content' : 'content of post 4'},
#    {'id':5,'title': 'post 5','content' : 'content of post 5'}
#        ]

#request= this give parameter the user enter in browser.
def index(request):
    blog_title = 'latest posts'
    #getting data from Post model
    all_posts = Post.objects.filter(is_published= True)

    #paginate
    paginator = Paginator(all_posts,6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context ={
        'blog_title' :  blog_title,
        'page_obj'      :  page_obj,
        'all_posts' :all_posts,
                }

    return render(request,"blog/index.html",context)

def detail(request,slug):
    if request.user and not request.user.has_perm('blog.view_post'):
        messages.error(request,'You have no permission to view any post')
        return redirect('blog:index')
    #static data...
    #post=next((item for item in posts if item['id']==int(post_id)),None)
    try:
    #getting data from model by post_id....#pk = primary key in default as id...
        post=Post.objects.get(slug=slug)
        related_posts = Post.objects.filter(category=post.category).exclude(pk=post.id)
    except Post.DoesNotExist:
        raise Http404(" Page Does Not Exist! ")

    #logging method for debug,to identify error , trace the data....
    #logger = logging.getLogger("Testing")
    #logger.debug(f'post variable is {post}')
    context = {
            "post":post,
            "related_posts":related_posts    
            }
    return render(request,'blog/detail.html',context)


def contact(request):
    if request.method =='POST':
        form = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message =request.POST.get('message')
        


        logger = logging.getLogger("Testing")
        if form.is_valid():
            logger.debug(f' POST variable is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}')
            #send email or save in the database
            success_message = 'your Email has been sent!'
            return render(request,'blog/contact.html',{'form':form ,'success_message':success_message })
        else:
            logger.debug(f'Form Validation failure')   
        return render(request,'blog/contact.html',{'form':form , 'name':name ,'email':email,'message':message})
    return render(request,'blog/contact.html')


def about(request):
    about_content = AboutUs.objects.first()
    if about_content is None or not about_content.content:
        about_content = "Default content goes here..."

    else:
        about_content = about_content.content
    return render(request,'blog/about.html',{'about_content':about_content})




#redirecting & reverse and named URLs
def old_url_redirect(request):
    return redirect(reverse("blog:new_page_url"))

def new_url_view(request):
    return HttpResponse('this is a new URL')

def profile_page(request):
    return render(request,'blog/profile.html')