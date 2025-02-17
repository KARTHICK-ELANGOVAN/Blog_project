from django.shortcuts import get_object_or_404, render,redirect

from django.views import generic,View
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.http import HttpResponse

from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib import messages
from .forms import LoginForm, PostForm, RegisterForm,ForgotPasswordForm,ResetPasswordForm #EditProfileForm,PasswordChangingForm
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required,permission_required

from blog.models import Post,Category
from django.core.paginator import Paginator


#reset password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
'''def password_success(request):
    return render(request,'registration/password_success.html')'''

def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)    #user data created
            user.set_password(form.cleaned_data['password'])  #set_password is for to change the value to hash value to hide the password in the database
            user.save()
            readers_group,created = Group.objects.get_or_create(name = 'Readers')
            user.groups.add(readers_group)
            messages.success(request,"Registration Successfull.You can log in...")
            return redirect("/members/login") 
    return render(request,"registration/register.html",{'form':form})

def login(request):
    print("login request")
    form = LoginForm()
    print("kar")
    if request.method=="POST":
        form = LoginForm(request.POST)#login form
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                auth_login(request,user)
                print("LOGIN SUCCESS")
                return redirect("/members/dashboard") #redirect to dashboard.
            

    return render(request,'registration/login.html',{'form':form})

def dashboard(request):
    blog_title ='My Posts'
    all_posts = Post.objects.filter(user=request.user)
    #paginate
    paginator = Paginator(all_posts,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'registration/dashboard.html',{'blog_title':blog_title,'page_obj':page_obj})

@login_required
@permission_required('blog.add_post',raise_exception=True)
def new_post(request):
    categories = Category.objects.all()
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)  
            post.user = request.user
            post.save()         #commit =true
            return redirect('/members/dashboard')
    return render(request,'registration/new_post.html',{'categories':categories,'form':form})

@login_required
@permission_required('blog.change_post',raise_exception=True)
def edit_post(request,post_id):
    categories = Category.objects.all()
    form = PostForm()
    post = get_object_or_404(Post,id = post_id)
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES,instance=post)  #FILES---this is to update th image ,instance--is for update the exiting content.
        if form.is_valid():
            form.save()
            messages.success(request, 'Post Update Successfully..')
            return redirect('members:dashboard')
    return render(request,'registration/edit_post.html',{'categories':categories,'post':post,'form':form})

@login_required
@permission_required('blog.delete_post',raise_exception=True)
def delete_post(request,post_id):
    post = get_object_or_404(Post,id = post_id)
    post.delete()
    messages.success(request, 'Post Deleted Successfully..')
    return redirect('members:dashboard')

@login_required   
@permission_required('blog.can_publish',raise_exception=True)
def publish_post(request,post_id):
    post = get_object_or_404(Post,id = post_id)
    post.is_published =True
    post.save()
    messages.success(request, 'Post Published Successfully..')
    return redirect('members:dashboard')
    

def forgot_password(request):
    form = ForgotPasswordForm()
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            #send Email to reset password
            token = default_token_generator.make_token(user)     # it genarate a token for a user for resset the password
            uid = urlsafe_base64_encode(force_bytes(user.pk))          # to reset the password ,genarate the link by function
            #to get a domain for url                              # base64 link in url is genarated,to generate thids we have to send a nbytes data massage 
            current_site = get_current_site(request)
            subject="Reset Password Requested"
            domain = current_site.domain #it gives a current domain url like 127.0.0.1:8000
            #also require a reset password email template
            message = render_to_string('registration/reset_password_email.html',{
                'domain': domain,
                'uid': uid,
                'token' : token })       #render_to_string convert the template to string
            send_mail(subject,message,'noreply@karthi.com',[email])
            messages.success(request, 'Email has been sent..')
    return render(request,'registration/forgot_password.html',{'form':form})



def reset_password(request,uidbase64,token):
    form =ResetPasswordForm()
    if request.method == 'POST':
        #form
        form= ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            try:
                uid = urlsafe_base64_decode(uidbase64)      #base64 string to id
                user = User.objects.get(pk=uid)
            except(TypeError,ValueError,OverflowError,User.DoesNotExist):
                user = None
            if user is not None and default_token_generator.check_token(user,token):
                user.set_password(new_password)
                user.save()
                messages.success(request,"Your Password has been reset successfully..")
                return redirect('members:login')
            else:
                messages.error(request,'The password reset link is invalid..')

    return render(request,'registration/reset_password.html',{'form':form})

def logout(request):
    auth_logout(request)
    messages.success(request,("You have been logged out... Thanks...."))
    return redirect('/')

'''class UserRegisterView(View):
    def get(self,request):
        form = SignUpForm()
        return render(request,'registration/register.html',{'form':form})
    
    def post(self,request):
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            form.save()
            print("successfully")
            return redirect('login')
        
        return render(request,'registration/register.html',{'form' :form,})'''

'''class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('login')

class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('login')
    def get_object(self):
        return self.request.user
 

def userView(request):
    return HttpResponse("hello you have logged in...")'''

'''---def login_view(request):
    if request.user.is_authenticated:
        return redirect('register')
    else:
        return render(request,'login.html')---'''
    
'''def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username ,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You Have Been Logged in...")
            return  redirect('index')
        else:
            messages.success(request,"There was an error.....")
            return redirect('loginpage')
    else:
        return render(request,'login.html')'''
