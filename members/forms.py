from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms

from blog.models import Category, Post


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label="username",max_length=100,required=True)
    email = forms.CharField(label='Email',max_length = 100,required=True)
    password = forms.CharField(label='Password',max_length=100,required=True)
    password_confirm=forms.CharField(label='confirm password', max_length=100, required=True)

    class Meta:
        model=User
        fields = ['username','email','password']

    def clean(self): #inbuild function clean in forms hicreturns
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('passwords do not match')
        
class LoginForm(forms.Form):
    username = forms.CharField(label="username",max_length=100,required=True)
    password = forms.CharField(label="password",max_length=100,required=True)

    def clean(self):
        cleaned_data = super().clean()
        username =cleaned_data.get("username")
        password= cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username,password=password)
            if user is None:
                raise forms.ValidationError("Invalid username and password..")

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='email',max_length=100,required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
    
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No User Registered with this Email..")
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(label='new_password',min_length=8,required=True)
    confirm_password = forms.CharField(label='confirm_password',min_length=8,required=True)

    def clean(self):#for custom validation is the new,confirm password is same or not 
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match...")
class PostForm(forms.ModelForm):
    title = forms.CharField(label='title', max_length=200 , required=True)
    content = forms.CharField(label='content',required=True)
    category = forms.ModelChoiceField(label='category',required=True, queryset=Category.objects.all())
    image_url  = forms.ImageField(label='Image',required=False)

    class Meta:
        model = Post
        fields = ['title','content','category','img_url']
    
    def clean(self):
        cleaned_data =  super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        
        #custom validation
        if title and len(title)<5:
            raise forms.ValidationError("Title must be at least 5 characters long..")
        if content and len(content)<10:
            raise forms.ValidationError('Content must be at least 10 characters long..')
    
    def save(self, commit = ...):
        post = super().save(commit)  

        cleaned_data = super().clean()
        if cleaned_data.get('img_url'):
            post.img_url = cleaned_data.get('img_url')
        else:
            img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/300px-No_image_available.svg.png"
            post.img_url = img_url
        
        if commit:
            post.save()
        return post
        

'''class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name =forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name =forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    username =forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_login =forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_superuser =forms.CharField(max_length=100,widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    is_staff =forms.CharField(max_length=100,widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    is_active =forms.CharField(max_length=100,widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    date_joined =forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','last_login','is_superuser','is_staff','is_active','date_joined']'''


'''class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name =forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name =forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']'''
    #def __init__(self,*args,**kwargs):
    #        super(SignUpForm,self).__init__(self,*args,**kwargs)
    #
     #       self.fields['username'].widget.attrs['class']='form-control'
    #      self.fields['password1'].widget.attrs['class']='form-control'
    #        self.fields['password2'].widget.attrs['class']='form-control'


'''class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','type':'password'}))
    new_password1 =forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class': 'form-control','type':'password'}))
    new_password2=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class': 'form-control','type':'password'}))

    class Meta:
        model = User
        fields = ['old_password','new_password1','new_password2' ]'''
